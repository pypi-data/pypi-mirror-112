from array import array
from io import RawIOBase, SEEK_CUR, SEEK_END, SEEK_SET
from mmap import mmap
from typing import Callable, Union

from hansken_extraction_plugin.runtime import unpack
from hansken_extraction_plugin.runtime.constants import MAX_CHUNK_SIZE


# inspo:https://stackoverflow.com/questions/58702442/wrap-an-io-bufferediobase-such-that-it-becomes-seek-able
class _GrpcRawIO(RawIOBase):
    """
    RawIOBase implementation that retrieves data using grpc calls.
    """
    def __init__(self, grpc_handler_read: Callable, stream_offset: int, size: int):
        """
        @param grpc_handler_read: callable that can be used to perform a grpc read request: e.g.
            hansken_extraction_plugin.runtime.extraction_plugin_server.ProcessHandler.read
        @param stream_offset: start of the stream
        @param size: total size of the stream
        """
        self._grpc_handler_read = grpc_handler_read
        self._size = size
        self._byte_array = bytes()
        self._position = 0
        if stream_offset is not None:
            self.seek(stream_offset)

    def seekable(self):
        return True

    def readable(self):
        return True

    def writable(self):
        return False

    def _read_chunks(self, size: int):
        """
        This method divides the requested data into chunks of the maximum allowed size per gRPC message.
        @param size: length of the requested data
        @return: a bytes() representation of the RpcBytes response from the server
        """
        offset = self._position
        # just one chunk
        if size <= MAX_CHUNK_SIZE:
            self._byte_array = unpack.bytez(self._grpc_handler_read(offset=offset, size=size))
        else:
            # multiple chunks
            no_of_chunks = size // MAX_CHUNK_SIZE
            for i in range(no_of_chunks):
                chunk_offset = offset + (i * MAX_CHUNK_SIZE)
                self._byte_array += \
                    unpack.bytez(self._grpc_handler_read(offset=chunk_offset, size=MAX_CHUNK_SIZE))
            last_offset = offset + no_of_chunks * MAX_CHUNK_SIZE
            last_size = size - last_offset
            if last_size > 0:
                self._byte_array += unpack.bytez(self._grpc_handler_read(offset=last_offset, size=last_size))

    def _clear_buffer(self):
        self._byte_array = bytes()

    def readinto(self, __buffer: Union[bytearray, memoryview, array, mmap]) -> int:
        __size = len(__buffer)
        if __size + self._position > self._size:
            __size = self._size - self._position

        self._clear_buffer()
        self._read_chunks(__size)
        # ignore mypy error because of mistake in typeshed: https://github.com/python/typeshed/issues/4991
        __buffer[:len(self._byte_array)] = self._byte_array  # type: ignore

        self._position += len(self._byte_array)
        return len(self._byte_array)

    def tell(self) -> int:
        return self._position

    def seek(self, position: int, whence: int = SEEK_SET) -> int:
        relative_to = {
            SEEK_SET: 0,
            SEEK_CUR: self._position,
            SEEK_END: self._size,
        }.get(whence, 0)

        if relative_to + position < 0:
            raise ValueError('Invalid argument, cannot seek to a position before start of stream')

        self._position = relative_to + position
        return self._position

    def close(self):
        super().close()
