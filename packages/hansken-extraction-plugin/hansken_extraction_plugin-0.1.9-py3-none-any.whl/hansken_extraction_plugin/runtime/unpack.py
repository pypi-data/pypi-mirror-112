from datetime import datetime
from typing import Any, Callable, Dict, List, Type, Union

from google.protobuf.any_pb2 import Any as GrpcAny
from google.protobuf.message import Message
from hansken.util import GeographicLocation
import pytz

from hansken_extraction_plugin.framework.DataMessages_pb2 import RpcTrace
from hansken_extraction_plugin.framework.PrimitiveMessages_pb2 import RpcBoolean, RpcBytes, RpcDouble, RpcEmptyList, \
    RpcEmptyMap, RpcInteger, RpcIsoDateString, RpcLatLong, RpcLong, RpcLongList, RpcMap, RpcNull, RpcString, \
    RpcStringList, RpcStringMap, RpcUnixTime, RpcZonedDateTime
from hansken_extraction_plugin.runtime.constants import NANO_SECOND_PRECISION


def any(message: GrpcAny, unpacker: Callable[[], Message]):
    """Unwraps an Any and returns the message"""
    unpacked = unpacker()
    message.Unpack(unpacked)
    return unpacked


def _rpc_zoned_date_time(zdt: RpcZonedDateTime) -> datetime:
    epoch_with_nanos = (zdt.epochSecond * NANO_SECOND_PRECISION + zdt.nanoOfSecond)
    epoch_float: float = epoch_with_nanos / NANO_SECOND_PRECISION
    timezone = pytz.timezone(zdt.zoneId)

    return datetime.fromtimestamp(epoch_float, timezone)


def _rpc_unix_time(ut: RpcUnixTime) -> datetime:
    epoch_float: float = ut.value / NANO_SECOND_PRECISION

    return datetime.fromtimestamp(epoch_float, pytz.utc)


def _map(rpc_map: RpcMap) -> Dict[str, Any]:
    converted_map: Dict[str, Any] = {}
    for key, value in rpc_map.entries.items():
        converted_map[key] = _primitive(value)
    return converted_map


_primitive_matchers: Dict[
    Type[Union[
        RpcNull,
        RpcBytes,
        RpcBoolean,
        RpcInteger,
        RpcLong,
        RpcDouble,
        RpcString,
        RpcEmptyList,
        RpcStringList,
        RpcLongList,
        RpcEmptyMap,
        RpcMap,
        RpcStringMap,
        RpcUnixTime,
        RpcZonedDateTime,
        RpcIsoDateString,
        RpcLatLong
    ]],
    Callable[[Any], Any]
] = {
    RpcNull: lambda value: None,
    RpcBytes: lambda value: value.value,
    RpcBoolean: lambda value: value.value,
    RpcInteger: lambda value: value.value,
    RpcLong: lambda value: value.value,
    RpcDouble: lambda value: value.value,
    RpcString: lambda value: value.value,
    RpcEmptyList: lambda value: [],
    RpcStringList: lambda value: value.values,
    RpcLongList: lambda value: value.values,
    RpcEmptyMap: lambda value: {},
    RpcMap: lambda value: _map(value),
    RpcStringMap: lambda value: value.entries,
    RpcUnixTime: lambda value: _rpc_unix_time(value),
    RpcZonedDateTime: lambda value: _rpc_zoned_date_time(value),
    RpcIsoDateString: lambda value: datetime.strptime(value.value, '%Y-%m-%dT%H:%M:%S%z'),
    RpcLatLong: lambda value: GeographicLocation(value.latitude, value.longitude)
}


def _primitive(value: GrpcAny):
    # unpacks a primitive value that is wrapped inside an (Grpc)Any
    for matchertype, unpacker in _primitive_matchers.items():
        if value.Is(matchertype.DESCRIPTOR):
            return unpacker(any(value, matchertype))

    raise RuntimeError('unable to unpack primitive value of type {} '.format(value))


def trace(trace: RpcTrace):
    """
    Converts a RpcTrace to a triplet, containing the id, types, and properties
    of the trace.

    param trace: the trace to convert

    Returns: triplet with id, types, and properties
    """
    id: str = trace.id
    types: List[str] = list(trace.types)
    properties: Dict[str, Any] = {prop.name: _primitive(prop.value) for prop in trace.properties}
    return id, types, properties


def bytez(bites: GrpcAny) -> bytes:
    """
    Converts GrpcAny to a primitive bytes() stream
    @param bites: trace to convert
    @return: primitive bytes()
    """
    return _primitive(bites)
