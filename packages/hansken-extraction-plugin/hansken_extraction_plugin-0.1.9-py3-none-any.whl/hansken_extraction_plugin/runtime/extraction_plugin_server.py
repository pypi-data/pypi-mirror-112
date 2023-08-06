# create grpc server using generated grpc code
from concurrent import futures
from contextlib import contextmanager
from io import BufferedReader
from queue import Queue
from signal import SIGINT, signal, SIGTERM
import threading
from typing import Any, Callable, cast, Dict, Generator, Iterator, List, Mapping, Optional, Set, Tuple, Type, Union

from google.protobuf.any_pb2 import Any as GrpcAny
import grpc
from logbook import Logger  # type: ignore

from hansken_extraction_plugin.api.extraction_context import ExtractionContext
from hansken_extraction_plugin.api.extraction_plugin import BaseExtractionPlugin, DeferredExtractionPlugin, \
    ExtractionPlugin, MetaExtractionPlugin
from hansken_extraction_plugin.api.extraction_trace import \
    ExtractionTrace, ExtractionTraceBuilder, Tracelet, validate_update_arguments
from hansken_extraction_plugin.api.trace_searcher import TraceSearcher
from hansken_extraction_plugin.framework.DataMessages_pb2 import RpcPluginInfo, RpcTrace
from hansken_extraction_plugin.framework.ExtractionPluginService_pb2_grpc import \
    add_ExtractionPluginServiceServicer_to_server, ExtractionPluginServiceServicer
from hansken_extraction_plugin.framework.RpcCallMessages_pb2 import RpcFinish, RpcRead, RpcStart
from hansken_extraction_plugin.runtime.constants import MAX_CHUNK_SIZE, MAX_MESSAGE_SIZE
from hansken_extraction_plugin.runtime.grpc_raw_io import _GrpcRawIO
import hansken_extraction_plugin.runtime.pack as pack
import hansken_extraction_plugin.runtime.unpack as unpack

log = Logger(__name__)


class GrpcExtractionTraceBuilder(ExtractionTraceBuilder):

    def __init__(self, grpc_handler: 'ProcessHandler', trace_id: str, name: Optional[str]):
        self._grpc_handler = grpc_handler
        self._trace_id = trace_id
        self._next_child_id = 0
        self._types: Set[str] = set()
        self._properties: Dict[str, object] = {}
        self._tracelets: List[Tracelet] = []
        self._has_been_built = False
        self._datas: Dict[str, bytes] = {}

        if name:
            self.update('name', name)

    def get(self, key: str, default=None):
        return self._properties[key] if key in self._properties else default

    def update(self, key_or_updates=None, value=None, data=None) -> ExtractionTraceBuilder:
        if key_or_updates is not None:
            types, properties = _extract_types_and_properties(self._properties, key_or_updates, value)
            self._types.update(types)
            self._properties.update(properties)
        if data is not None:
            for data_type in data:
                if data_type in self._datas:
                    raise RuntimeError(f'data with type {data_type} already exists on this trace')
            self._datas = data
        return self

    def add_tracelet(self, value: Tracelet) -> 'ExtractionTraceBuilder':
        if value is not None:
            self._tracelets.append(value)
        return self

    def child_builder(self, name: str = None) -> ExtractionTraceBuilder:
        if not self._has_been_built:
            raise RuntimeError('parent trace has not been built before creating a child')
        return GrpcExtractionTraceBuilder(self._grpc_handler, self._get_next_child_id(), name)

    def build(self) -> str:
        self._grpc_handler.begin_child(self._trace_id, self.get('name'))
        self._flush()
        self._grpc_handler.write_datas(self._trace_id, self._datas)
        self._grpc_handler.finish_child(self._trace_id)
        self._has_been_built = True
        return self._trace_id

    def _get_next_child_id(self):
        next_id = self._trace_id + '-' + str(self._next_child_id)
        self._next_child_id = self._next_child_id + 1
        return next_id

    def _flush(self):
        log.debug('Flushing trace builder {}', self._trace_id)
        # remove name property as it was already given through self._grpc_handler#begin_child
        # and the properties are cleared anyway (and flush is only called when the child is built)
        del self._properties['name']
        self._grpc_handler.enrich_trace(self._trace_id, self._types, self._properties, self._tracelets)
        self._types.clear()
        self._properties.clear()


class GrpcExtractionTrace(ExtractionTrace):
    """
    Helper class that exposes a trace that was exchanged with the gRPC
    protocol.
    """

    def __init__(self, grpc_handler: 'ProcessHandler', trace_id: str, properties: Dict[str, Any],
                 context: ExtractionContext):
        self._properties = properties
        self._grpc_handler = grpc_handler
        self._trace_id = trace_id
        self._next_child_id = 0
        self._new_types: Set[str] = set()
        self._new_properties: Dict[str, object] = {}
        self._tracelets: List[Tracelet] = []
        self._context = context

    def get(self, key: str, default=None):
        return self._properties[key] if key in self._properties else default

    def update(self, key_or_updates=None, value=None, data=None) -> None:
        if key_or_updates is not None:
            types, properties = _extract_types_and_properties(self._properties, key_or_updates, value)
            self._new_types.update(types)
            self._new_properties.update(properties)
            self._properties.update(properties)
        if data is not None:
            self._grpc_handler.write_datas(self._trace_id, data)

    def add_tracelet(self, value: Tracelet) -> None:
        if value is not None:
            self._tracelets.append(value)

    def open(self, offset=0, size=None) -> BufferedReader:
        data_size = self._context.data_size()
        first_bytes = self._context.first_bytes()
        if offset < 0 or offset > data_size:
            raise ValueError('Invalid value for offset')
        if size is None:
            size = data_size
        return BufferedReader(_GrpcRawIO(self._grpc_handler.read, offset, size, first_bytes), buffer_size=1024 * 1024)

    def child_builder(self, name: str = None) -> ExtractionTraceBuilder:
        return GrpcExtractionTraceBuilder(self._grpc_handler, self._get_next_child_id(), name)

    def _get_next_child_id(self):
        next_id = self._trace_id + '-' + str(self._next_child_id)
        self._next_child_id = self._next_child_id + 1
        return next_id

    def _flush(self):
        """
        Send all new updates on this trace to the client side.
        """
        log.debug('Flushing trace builder {}', self._trace_id)
        if len(self._new_types) == 0 and len(self._new_properties) == 0:
            return
        # TODO: use trace id
        self._grpc_handler.enrich_trace(self._trace_id, self._new_types,
                                        self._new_properties, self._tracelets)
        self._new_types = []
        self._new_properties = {}

    def __eq__(self, other):
        if not isinstance(other, GrpcExtractionTrace):
            return False

        return self._properties == other._properties


def _extract_types_and_properties(existing_properties: Union[Mapping, str], key_or_updates: Union[Mapping, str],
                                  value=None) -> Tuple[set, dict]:
    """
    Get the new types and properties defined by given 'key_or_updates' and 'value' properties
    (see `api.ExtractionTrace.update` for more information about their format).

    If a property was already set, an error is thrown (validated against 'existing_properties')

    :param existing_properties: the properties which were already set
    :param key_or_updates: the update key or mapping
    :param value: the update value in case 'key_or_updates' was a str
    :return: a tuple of a set of the types, and a mapping of the properties
    """

    validate_update_arguments(key_or_updates, value)

    types = set()
    properties = {}

    updates: Mapping[Any, Any]
    if isinstance(key_or_updates, str):
        updates = {key_or_updates: value}
    else:
        updates = key_or_updates

    for name, value in updates.items():
        if name in existing_properties:
            raise RuntimeError("""property '{}' has already been set""".format(name))
        if name == 'name':
            properties[name] = value
        else:
            # determine type from property name
            type = name[0:name.find('.')]

            # add type and property to list of new types
            types.add(type)
            properties[name] = value

    return types, properties


def _create_trace(grpc_handler: 'ProcessHandler', rpc_trace: RpcTrace, context: ExtractionContext) -> \
        GrpcExtractionTrace:
    id, types, properties = unpack.trace(rpc_trace)
    return GrpcExtractionTrace(grpc_handler=grpc_handler, trace_id=id, properties=properties, context=context)


class GrpcWriter:
    """
    Class that writes data to a grpc connection. Can be used with the with keyword:

    with GrpcWriter(trace_id, data_type, handler) as writer:
        write(bytes('test_string', 'UTF_8')
    """

    def __init__(self, trace_id: str, data_type: str, handler: 'ProcessHandler'):
        self.trace_id = trace_id
        self.data_type = data_type
        self.handler = handler

    def __enter__(self):
        start_message = pack.begin_writing(self.trace_id, self.data_type)
        self.handler.handle_message(start_message)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        finish_message = pack.finish_writing(self.trace_id, self.data_type)
        self.handler.handle_message(finish_message)

    def write(self, data: bytes):
        """
        Writes data to grpc stream. Sends data in separate chunks if it does not fit in one message
        """
        size = len(data)
        offset = 0
        while offset < size:
            data_message = pack.write_data(self.trace_id, self.data_type, data[offset: offset + MAX_CHUNK_SIZE])
            self.handler.handle_message(data_message)
            offset += MAX_CHUNK_SIZE


class ProcessHandler:
    """
    Handles the bidirectional grpc stream returned by the process method.
    The response iterator allows reading responses sent by the hansken client
    """

    # if the request queue contains this sentinel, it indicates that no more items can be expected
    _sentinel = object()

    def __init__(self, response_iterator: Iterator[GrpcAny]):
        log.debug('Creating a new GRPC process handler')
        # requests is a simple queue, all messages added to this queue are
        # sent to the client over gRPC. The zero indicates that this is an unbound queue
        self._requests: Queue[GrpcAny] = Queue(0)

        # gRPC responses are returned to this iterator
        self._response_iterator = response_iterator

        # stack trace ids, representing the current depth first pre-order scope, in order to translate it to in-order
        # the reason for this is that traces are not sent as soon as one is built (using TraceBuilder#build),
        # because the python API expects each parent trace to be built before their children
        # whereas the gRPC API expects a child to be finished before the parent
        self._trace_stack: List[str] = []

    def _handle_request(self, request) -> GrpcAny:
        """Block call, send a message to the client, and returns it's reply."""
        self.handle_message(request)
        return next(self._response_iterator)

    def handle_message(self, message: Any):
        self._requests.put_nowait(pack.any(message))

    def write_datas(self, trace_id: str, data: Mapping[str, bytes]):
        for data_type in data:
            self.write_data(trace_id, data_type, data[data_type])

    def write_data(self, trace_id: str, data_type: str, data: bytes):
        with GrpcWriter(trace_id, data_type, self) as writer:
            writer.write(data)

    def enrich_trace(self, trace_id, types, properties, tracelet_properties):
        log.debug('Process handler enriches trace {} with properties {}', trace_id, properties)
        self._assert_correct_trace(trace_id)
        request = pack.trace_enrichment(trace_id, types, properties, tracelet_properties)
        self.handle_message(request)

    def read(self, offset: int = 0, size: int = 1):
        log.debug('Reading trace with offset {} and size {}', offset, size)
        rpc_read: RpcRead = pack.rpc_read(offset, size)
        return self._handle_request(rpc_read)

    def begin_child(self, trace_id: str, name: str) -> None:
        log.debug('Process handler is beginning child trace {}', trace_id)
        while self._trace_stack and not self._is_direct_parent(self._trace_stack[-1], trace_id):
            # finish all out of scope traces
            self.handle_message(pack.finish_child(self._trace_stack.pop()))

        request = pack.begin_child(trace_id, name)
        self.handle_message(request)
        self._trace_stack.append(trace_id)

    def finish_child(self, trace_id: str) -> None:
        log.debug('Process handler is finishing child trace {}', trace_id)
        self._assert_correct_trace(trace_id)
        # not yet flushing here, because the python API stores parent before child (pre-order),
        # but the client expects the other way around (in-order)

    def finish(self):
        """
        Let the client know the server has finished processing this trace.
        :return:
        """
        log.debug('Process handler is finishing processing.')
        request = RpcFinish()
        self.handle_message(request)
        self._finish()

    def finish_with_error(self, exception):
        """
        Let the client know an exception occurred while processing this trace.
        :return:
        """
        log.warning('Finishing processing with an exception:', exc_info=True)
        try:
            rpc_partial_finish = pack.partial_finish_with_error(exception)
            self.handle_message(rpc_partial_finish)
        except Exception:
            # nothing more we can do now...  this is a last-resort catch to (hopefully) get the word out we're done
            log.warning('An exception occurred while reporting an error to the client')
            log.debug('with the following exception', exc_info=True)
        finally:
            # but do try to finish and let the client know it's over
            self._finish()

    def _finish(self):
        """
        Always try to finish with the sentinel.
        :return:
        """
        log.debug('Finish by putting the sentinel on the request queue')
        self._requests.put_nowait(self._sentinel)

    def iter(self) -> Iterator[GrpcAny]:
        """
        Returns iterator object to which new messages are pushed, that can be
        returned to gRPC.
        """
        return iter(self._requests.get, self._sentinel)

    def _flush_traces(self) -> None:
        """
        Send all remaining finish messages for the trace ids on the id stack.
        """
        while self._trace_stack:
            self.handle_message(pack.finish_child(self._trace_stack.pop()))

    def _assert_correct_trace(self, trace_id: str) -> None:
        """
        Assert that the id passed (which should be the id of te trace currently
        working on) is the one currently in scope based on the id stack.
        """
        if not self._trace_stack:
            # if no trace on the stack, assert that we are working on the root
            if '-' not in trace_id:
                return
            raise RuntimeError('trying to update trace {} before initializing it'.format(trace_id))
        # assert that the current trace on the top of the stack is the one we are working on
        if self._trace_stack[-1] != trace_id:
            raise RuntimeError(
                'trying to update trace {} before building trace {}'.format(trace_id, self._trace_stack[-1])
            )

    @staticmethod
    def _is_direct_parent(parent_id: str, child_id: str) -> bool:
        return child_id.startswith(parent_id) and len(parent_id) == child_id.rfind('-')


class ExtractionPluginServicer(ExtractionPluginServiceServicer):
    def __init__(self, extraction_plugin_class: Callable[[], BaseExtractionPlugin]):
        self._plugin = extraction_plugin_class()

    def pluginInfo(self, request, context: grpc.RpcContext) -> RpcPluginInfo:  # noqa: N802
        """
        Converts Extraction Plugin plugin info to gRPC plugininfo
        and returns it to the requester.
        """
        return pack.plugin_info(self._plugin.plugin_info())

    def process(self, response_iterator: Iterator[GrpcAny], context: grpc.RpcContext) -> Iterator[GrpcAny]:
        """
        Asynchronous process method. This is where the plugin process method gets called
        in a new thread. This call will return immediately. The process thread will do the processing of the trace.
        After the thread completes, a finish message is sent to the client.

        :param response_iterator: The GRPC handler's queue iterator
        :param context: The trace context
        """
        grpc_handler = ProcessHandler(response_iterator)
        try:
            log.debug('Plugin servicer process started.')
            self._process(response_iterator, context, grpc_handler)
        except Exception as exception:
            log.error('An exception occurred during processing')
            grpc_handler.finish_with_error(exception)
        finally:
            # Return the iterator to get the next message or the sentinel, which marks the last entry.
            log.debug('Plugin servicer process finished.')
            return grpc_handler.iter()

    def _start_message_to_context(self, start_message: RpcStart):
        return ExtractionContext(data_type=start_message.context.dataType,
                                 data_size=start_message.context.data.size)

    def _process(self, response_iterator, grpc_context, grpc_handler):
        first_message = response_iterator.next()
        if not first_message.Is(RpcStart.DESCRIPTOR):
            log.warning('Expecting RpcStart, but received unexpected message: {}', first_message)
            raise RuntimeError('Expecting RpcStart message')

        start_message = unpack.any(first_message, RpcStart)

        # process in a different thread, so that we can keep this thread to send messages to the client (Hansken)
        if isinstance(self._plugin, ExtractionPlugin):
            extraction_context = ExtractionContext(data_type=start_message.context.dataType,
                                                   data_size=start_message.context.data.size,
                                                   first_bytes=start_message.context.data.firstBytes)
            trace = _create_trace(grpc_handler=grpc_handler, rpc_trace=start_message.trace, context=extraction_context)
            def run_process(): cast(ExtractionPlugin, self._plugin).process(trace, extraction_context)
            threading.Thread(target=self._process_trace,
                             args=(run_process, trace, grpc_handler, extraction_context),
                             daemon=True).start()

        elif isinstance(self._plugin, MetaExtractionPlugin):
            trace = _create_trace(grpc_handler=grpc_handler, rpc_trace=start_message.trace, context=None)
            def run_process(): cast(MetaExtractionPlugin, self._plugin).process(trace)
            threading.Thread(target=self._process_trace,
                             args=(run_process, trace, grpc_handler, None),
                             daemon=True).start()

        elif isinstance(self._plugin, DeferredExtractionPlugin):
            extraction_context = ExtractionContext(data_type=start_message.context.dataType,
                                                   data_size=start_message.context.data.size,
                                                   first_bytes=start_message.context.data.firstBytes)
            trace = _create_trace(grpc_handler=grpc_handler, rpc_trace=start_message.trace, context=extraction_context)
            searcher = TraceSearcher()
            def run_process(): cast(DeferredExtractionPlugin, self._plugin).process(trace, extraction_context, searcher)
            threading.Thread(target=self._process_trace,
                             args=(run_process, trace, grpc_handler, extraction_context),
                             daemon=True).start()

        else:
            raise RuntimeError('Unsupported type of plugin: {}', str(type(self._plugin)))

    def _process_trace(self, run_process: Callable[[], None],
                       trace: GrpcExtractionTrace,
                       grpc_handler: ProcessHandler,
                       context: ExtractionContext):
        try:
            self._log_start_processing(trace, context)
            run_process()
            self._flush_trace_tree(grpc_handler, trace)
            grpc_handler.finish()
            log.info('Finished processing trace with id: {}', trace._trace_id)
        except Exception as exception:
            log.exception('Error during processing trace with id: {}', trace._trace_id)
            try:
                self._flush_trace_tree(grpc_handler, trace)
            finally:
                grpc_handler.finish_with_error(exception)

    def _log_start_processing(self, trace: GrpcExtractionTrace, context: ExtractionContext):
        # meta context has no associated data stream
        if context is None:
            log.info('Started processing trace with id: {}, data type: meta', trace._trace_id)
        else:
            log.info('Started processing trace with id: {}, data type: {}, size: {}',
                     trace._trace_id,
                     context.data_type(),
                     context.data_size())

    def _flush_trace_tree(self, grpc_handler: ProcessHandler, trace: GrpcExtractionTrace):
        # flush cached child traces
        grpc_handler._flush_traces()
        # flush updated information on root trace
        trace._flush()


def _start_server(extraction_plugin_class: Type[BaseExtractionPlugin], address: str) -> grpc.Server:
    """
    Starts extraction plugin server.

    extraction_plugin_class: Class of the extraction plugin implementation
    address: Address serving this server

    Returns: GRPC server object
    """
    options = (('grpc.max_send_message_length', MAX_MESSAGE_SIZE),
               ('grpc.max_receive_message_length', MAX_MESSAGE_SIZE))
    # TODO Is 16 the correct number? Make configurable or investigate
    num_workers = 16
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=num_workers), options=options)
    add_ExtractionPluginServiceServicer_to_server(ExtractionPluginServicer(extraction_plugin_class), server)
    server.add_insecure_port(address)
    log.info('Starting GRPC Extraction Plugin server with {} workers. Listening on {}.', num_workers, address)
    server.start()
    return server


@contextmanager
def serve(extraction_plugin_class: Type[BaseExtractionPlugin], address: str) -> Generator[grpc.Server, None, None]:
    """
    Returns context manager to start a server, so a server can be started using the with keyword.

    extraction_plugin_class: Class of the extraction plugin implementation
    address: Address serving this server

    Returns: contextmanager of extraction plugin server
    """
    server = _start_server(extraction_plugin_class, address)
    yield server
    server.stop(None)


def serve_indefinitely(extraction_plugin_class: Type[BaseExtractionPlugin], address: str):
    """
    Starts extraction plugin server that runs until it is explicitly killed.

    This method installs a SIGTERM handler, so the extraction plugin server
    will be stopped gracefully when the server(container) is requested to stop.
    Therefore, this method can only be called from the main-thread.

    extraction_plugin_class: Class of the extraction plugin implementation
    address: Address serving this server
    """
    server = _start_server(extraction_plugin_class, address)

    def handle_signal(*_):
        log.info('Received SIGTERM, stopping the plugin server now')
        log.info('Waiting max 5 seconds for requests to complete')
        server.stop(5).wait(5)
        log.info('Shut down gracefully')

    signal(SIGTERM, handle_signal)
    signal(SIGINT, handle_signal)

    server.wait_for_termination()
    log.info('Server terminated')
