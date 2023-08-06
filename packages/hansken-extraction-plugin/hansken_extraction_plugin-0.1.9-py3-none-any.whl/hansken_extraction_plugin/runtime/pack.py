from datetime import datetime
import traceback
from typing import Any, Dict, List

from google.protobuf.any_pb2 import Any as GrpcAny
import grpc
from hansken import util
from hansken.util import GeographicLocation

from hansken_extraction_plugin.api.author import Author
from hansken_extraction_plugin.api.extraction_plugin import BaseExtractionPlugin, DeferredExtractionPlugin, \
    ExtractionPlugin, MetaExtractionPlugin
from hansken_extraction_plugin.api.extraction_trace import Tracelet
from hansken_extraction_plugin.api.plugin_info import PluginInfo
from hansken_extraction_plugin.framework.DataMessages_pb2 import \
    RpcAuthor, RpcPluginInfo, RpcPluginType, RpcTrace, RpcTracelet, RpcTraceProperty
from hansken_extraction_plugin.framework.PrimitiveMessages_pb2 import RpcBoolean, RpcBytes, RpcDouble, RpcEmptyList, \
    RpcEmptyMap, RpcIsoDateString, RpcLatLong, RpcLong, RpcLongList, RpcMap, RpcString, RpcStringList, RpcStringMap, \
    RpcZonedDateTime
from hansken_extraction_plugin.framework.RpcCallMessages_pb2 import RpcBeginChild, RpcBeginDataStream, RpcFinishChild, \
    RpcFinishDataStream, RpcSearchRequest, RpcWriteDataStream
from hansken_extraction_plugin.framework.RpcCallMessages_pb2 import RpcEnrichTrace, RpcPartialFinishWithError, RpcRead
from hansken_extraction_plugin.runtime.constants import NANO_SECOND_PRECISION


def any(message: Any) -> GrpcAny:
    """
    Wraps a message in an Any

    message: the message to wrap in an any

    Returns: the wrapped message in an Any"""
    any_request = GrpcAny()
    any_request.Pack(message)
    return any_request


def _list(list):
    if not list:
        return RpcEmptyList()

    if all(type(value) == str for value in list):
        return RpcStringList(values=list)

    if all(type(value) == int for value in list):
        return RpcLongList(values=list)

    raise RuntimeError('currently only homogeneous lists of type str or int are supported')


def _map(map):
    if not map:
        return RpcEmptyMap()

    if all(type(key) == str and type(value) == str for key, value in map.items()):
        msg = RpcStringMap()
        msg.entries.update(map)
        return msg

    rpc_map: Dict[str, Any] = {}
    for key, value in map.items():
        primitive: GrpcAny = any(_primitive(value))
        rpc_map[key] = primitive
    return RpcMap(entries=rpc_map)


def _to_rpc_iso_date_string(dt: datetime) -> RpcIsoDateString:
    return RpcIsoDateString(value=util.format_datetime(dt))


def _to_rpc_zoned_date_time(dt: datetime):
    # 123456.123456789 becomes 123456
    epoch_second = int(dt.timestamp())
    # (123456.123456789 - 123456 = .123456789) * NANO_SECOND_PRECISION = 123456789.0
    nano_of_second = int((dt.timestamp() - epoch_second) * NANO_SECOND_PRECISION)
    zone_offset = dt.strftime('%z')
    zone_id = str(dt.tzinfo)

    return RpcZonedDateTime(epochSecond=epoch_second, nanoOfSecond=nano_of_second,
                            zoneOffset=zone_offset, zoneId=zone_id)


_primitive_matchers = {
    bool: lambda value: RpcBoolean(value=value),
    int: lambda value: RpcLong(value=value),
    float: lambda value: RpcDouble(value=value),
    str: lambda value: RpcString(value=value),
    list: lambda value: _list(value),
    bytes: lambda value: RpcBytes(value=value),
    bytearray: lambda value: RpcBytes(value=bytes(value)),
    datetime: lambda value: _to_rpc_zoned_date_time(value),
    dict: lambda value: _map(value),
    GeographicLocation: lambda value: RpcLatLong(latitude=value[0], longitude=value[1])
}


def _primitive(value: Any):
    valuetype = type(value)
    if valuetype not in _primitive_matchers:
        raise RuntimeError('unable to pack value of type {} '.format(valuetype))

    return _primitive_matchers[valuetype](value)


def _property(name: str, value: Any) -> RpcTraceProperty:
    return RpcTraceProperty(
        name=name,
        value=any(_primitive(value)))


def author(author: Author) -> RpcAuthor:
    """
    Convert given Author to their RpcAuthor counterpart.

    author: the author to convert

    Returns: the converted author
    """
    return RpcAuthor(
        name=author.name,
        email=author.email,
        organisation=author.organisation)


def partial_finish_with_error(exception: Exception) -> RpcPartialFinishWithError:
    """
    Convert an exception into the grpc RpcPartialFinishWithError message

    :param exception: the exception to convert

    :return: the converted exception
    """
    return RpcPartialFinishWithError(
        actions=[],  # pending actions have not been implemented yet
        statusCode=grpc.StatusCode.CANCELLED.name,
        errorDescription=traceback.format_exc()
    )


def plugin_info(plugin_info: PluginInfo) -> RpcPluginInfo:
    """
    Convert given PluginInfo to their RpcPluginInfo counterpart.

    plugin_info: the info to convert

    Returns: the converted info
    """
    return RpcPluginInfo(
        type=_plugin_type(plugin_info.plugin),
        name=plugin_info.name,
        version=plugin_info.version,
        description=plugin_info.description,
        author=author(plugin_info.author),
        matcher=plugin_info.matcher,
        webpageUrl=plugin_info.webpage_url,
        maturity=plugin_info.maturity.value,
        deferredIterations=plugin_info.deferred_iterations)


def _plugin_type(plugin: BaseExtractionPlugin) -> Any:  # noqa
    if isinstance(plugin, MetaExtractionPlugin):
        return RpcPluginType.MetaExtractionPlugin
    if isinstance(plugin, ExtractionPlugin):
        return RpcPluginType.ExtractionPlugin
    if isinstance(plugin, DeferredExtractionPlugin):
        return RpcPluginType.DeferredExtractionPlugin
    raise RuntimeError(f'unsupported type of plugin: {plugin.__class__.__name__}')


def trace(id: str, types: List[str], properties: Dict[str, Any],
          all_tracelets: List[Tracelet]) -> RpcTrace:
    """
    Create a RpcTrace from a given set of types and prop

    :param id: the id of the trace
    :param types: the types of the trace
    :param properties: the properties of the trace
    :param all_tracelets: the Tracelet properties of the traceerties, together with
    the other necessary metadata for a trace.

    Returns: the created message
    """
    rpc_properties = []
    for name, value in properties.items():
        rpc_properties.append(_property(name, value))

    rcp_all_tracelets = []
    for tracelet_properties in all_tracelets:
        rpc_tracelet_properties = []
        for name, value in tracelet_properties.value.items():
            rpc_tracelet_properties.append(_property(name, value))
        rcp_all_tracelets.append(RpcTracelet(name=tracelet_properties.name,
                                             properties=rpc_tracelet_properties))

    return RpcTrace(
        id=id,
        types=types,
        properties=rpc_properties,
        tracelets=rcp_all_tracelets)


def trace_enrichment(trace_id: str, types: List[str], properties: Dict[str, Any],
                     all_tracelets: List[Tracelet]) -> RpcEnrichTrace:
    """
    Create a RpcEnrichTrace message which contains given set of types and
    properties to send to the client and used to enrich the currently processed
    trace with.

    :param trace_id: the id of the trace given to it by gRPC
    :param types: the types of the trace
    :param properties: the properties of the trace
    :param all_tracelets: the Tracelet properties of the trace

    :return: the created message
    """
    return RpcEnrichTrace(trace=trace(trace_id, types, properties, all_tracelets))


def begin_child(trace_id: str, name: str) -> RpcBeginChild:
    """
    Create an RpcBeginChild message which contains the id and name of the
    new child trace to create.

    :param trace_id: the id of the new child trace
    :param name: the name of the new child trace
    """
    return RpcBeginChild(id=trace_id, name=name)


def finish_child(trace_id: str) -> RpcFinishChild:
    """
    Create an RpcFinishChild message which contains the id of the
    child trace to store.

    :param trace_id: the id of the child trace to store
    """
    return RpcFinishChild(id=trace_id)


def rpc_read(position: int = 0, size: int = 1, trace_id: str = '0') -> RpcRead:
    """
    TODO: Fake it until you make it (HANSKEN-15274)
    Create an RpcRead message which contains the offset and size of the data we want to read.
    And the trace ID of the trace we want to read the data from.

    position: the position to read at
    size: the amount of bytes to read
    trace_id: the id of the trace to read data from

    Returns: the created message
    """
    return RpcRead(position=position, count=size, traceId=trace_id)


def rpc_bytes(value: bytes) -> RpcBytes:
    """
    Create an RpcBytes message which contains the supplied byte array.

    value: the byte array

    Returns: the created message
    """
    return _primitive(value)


def begin_writing(trace_id: str, data_type: str) -> RpcBeginDataStream:
    return RpcBeginDataStream(traceId=trace_id, dataType=data_type)


def write_data(trace_id: str, data_type: str, data: bytes) -> RpcWriteDataStream:
    return RpcWriteDataStream(traceId=trace_id, dataType=data_type, data=data)


def finish_writing(trace_id: str, data_type: str) -> RpcFinishDataStream:
    return RpcFinishDataStream(traceId=trace_id, dataType=data_type)


def search_request(query: str, count: int) -> RpcSearchRequest:
    return RpcSearchRequest(query=query, count=count)
