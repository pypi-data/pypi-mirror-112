from io import BufferedReader
from typing import Any, Callable, Dict, List, Tuple

from hansken.abstract_trace import AbstractTrace
from hansken.tool import run
from hansken.trace import TraceBuilder
from logbook import Logger  # type: ignore

from hansken_extraction_plugin.api.extraction_context import ExtractionContext
from hansken_extraction_plugin.api.extraction_plugin import ExtractionPlugin
from hansken_extraction_plugin.api.extraction_trace import \
    ExtractionTrace, ExtractionTraceBuilder, Tracelet, validate_update_arguments

log = Logger(__name__)


class HanskenPyExtractionTraceBuilder(ExtractionTraceBuilder):

    def __init__(self, builder: TraceBuilder):
        self._hanskenpy_trace_builder = builder
        self._tracelet_properties: List[Tracelet] = []

    def update(self, key_or_updates=None, value=None, data=None) -> ExtractionTraceBuilder:
        if data is not None:
            for stream_name in data:
                self._hanskenpy_trace_builder.add_data(stream=stream_name, data=data[stream_name])

        if key_or_updates is not None or value is not None:
            validate_update_arguments(key_or_updates, value)
            self._hanskenpy_trace_builder.update(key_or_updates, value)

        return self

    def add_tracelet(self, value: Tracelet) -> 'ExtractionTraceBuilder':
        # TODO HANSKEN-15372 Extraction plugin tracelet support FVT via REST API
        log.error(f"PluginRunner doesn't support add_tracelet over REST API, Tracelet is dropped {value.name}")
        if value is not None:
            self._tracelet_properties.append(value)
        return self

    def child_builder(self, name: str = None) -> 'ExtractionTraceBuilder':
        return HanskenPyExtractionTraceBuilder(self._hanskenpy_trace_builder.child_builder(name))

    def build(self) -> str:
        return self._hanskenpy_trace_builder.build()


class HanskenPyExtractionTrace(ExtractionTrace):
    """
    Helper class that wraps a trace from Hansken.py in a ExtractionTrace,
    so that Hansken.Py traces can be used in Extraction plugins.

    We delegate all calls of the abstract class Mapping to the Hansken.py trace,
    since Hansken.py does a lot of tricks to get things working.
    """

    def __init__(self, trace: AbstractTrace, context: ExtractionContext):
        """
        Constructor.

        trace: a trace exposed from Hansken.py
        data_stream_type: the type of data stream that this plugin can process.  default value is 'raw'
        """
        self._hanskenpy_trace = trace
        self._new_properties: Dict[str, Any] = {}
        self._tracelet_properties: List[Tracelet] = []
        self._context = context

    def update(self, key_or_updates=None, value=None, data=None) -> None:
        if data is not None:
            self._hanskenpy_trace.update(data=data)

        if key_or_updates is not None or value is not None:
            validate_update_arguments(key_or_updates, value)
            self._hanskenpy_trace.update(key_or_updates, value, overwrite=True)
            updates = key_or_updates

            if isinstance(key_or_updates, str):
                updates = {key_or_updates: value}

            # update does not add the new properties to the trace _source, so
            # keep track of them here, so that we can return them when someone calls get(new_property)
            for name, value in updates.items():
                self._new_properties[name] = value

    def add_tracelet(self, value: Tracelet) -> None:
        # TODO HANSKEN-15372 Extraction plugin tracelet support FVT via REST API
        log.error(f"PluginRunner doesn't support add_tracelet over REST API, Tracelet is dropped {value.name}")
        if value is not None:
            self._tracelet_properties.append(value)

    def open(self, offset=0, size=None) -> BufferedReader:
        return self._hanskenpy_trace.open(stream=self._context.data_type(), offset=offset, size=size)

    def child_builder(self, name: str = None) -> ExtractionTraceBuilder:
        return HanskenPyExtractionTraceBuilder(self._hanskenpy_trace.child_builder(name))

    def get(self, key, default=None):
        return self._new_properties[key] if key in self._new_properties else self._hanskenpy_trace.get(key, default)


class _PluginRunner:
    """
    Helper class that allows an Extraction Plugin to be executed with Hansken.py.
    """
    def __init__(self, extraction_plugin_class: Callable[[], ExtractionPlugin]):
        self._extraction_plugin_class = extraction_plugin_class

    def run(self, context):
        log.info('PluginRunner is running plugin class {}', self._extraction_plugin_class.__name__)
        plugin = self._extraction_plugin_class()

        query, data_stream_type = _split_matcher(plugin.plugin_info().matcher)

        with context:
            for trace in context.search(query):
                context = ExtractionContext(data_size=trace.get('data.{}.size'.format(data_stream_type)),
                                            data_type=data_stream_type)
                plugin.process(HanskenPyExtractionTrace(trace, context), context)


def _split_matcher(matcher: str) -> Tuple[str, str]:
    """
    This method splits a matcher string into the HQL portion, and the data stream type portion.
    It requires the data stream type to be at the END of the string.
    Example:
        'A AND B AND C AND $data.type=raw'
    @param matcher: the HQL matcher of this plugin + the $data.type suffix
    @return: query: the HQL query
             data_stream_type: the type value of the '$data.type=value' argument
    """
    data_type_prefix = 'and $data.type='
    error_message = 'a matcher should end with "$data.type=value"'
    matcher = matcher.strip()

    # starts with $data.type or contains more than 1
    if matcher.lower().count(data_type_prefix) != 1:
        raise TypeError(error_message)

    index = matcher.lower().index(data_type_prefix)

    # $data.type not at end of line. the substring 'and $data.type=value' should contain exactly 1 space.
    if matcher[index:].count(' ') != 1:
        raise TypeError(error_message)

    query = matcher[:index]
    data_stream_type = matcher[index + len(data_type_prefix):]
    return query, data_stream_type


def run_with_hanskenpy(extraction_plugin_class: Callable[[], ExtractionPlugin], **defaults):
    """
    Runs an Extraction Plugin as a script on a specific project,  using Hansken.py.
    An Extraction Plugin as scripts is executed against a Hansken server, on a
    project that already has been extracted.

    extraction_plugin_class: Class of the extraction plugin implementation
    """
    runner = _PluginRunner(extraction_plugin_class)
    run(with_context=runner.run, **defaults)
