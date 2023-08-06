from abc import ABC, abstractmethod
from io import BufferedReader
from typing import Any, Mapping, Union


class Tracelet:
    def __init__(self, name: str, value: Mapping):
        self.name = name
        self.value = value


class ExtractionTraceBuilder(ABC):

    @abstractmethod
    def update(self, key_or_updates: Union[Mapping, str] = None, value: Any = None,
               data: Mapping[str, bytes] = None) -> 'ExtractionTraceBuilder':
        """
        Updates or add metadata properties for this `.ExtractionTraceBuilder`.
        Can be used to update the name of the Trace represented by this builder,
        if not already set.

        :param key_or_updates: either a `str` (the metadata property to be
            updated) or a mapping supplying both keys and values to be updated
        :param value: the value to update metadata property *key* to (used
            only when *key_or_updates* is a `str`, an exception will be thrown
            if *key_or_updates* is a mapping)
        :param data: a `dict` mapping data type / stream name to bytes to be
            added to the trace
        :return: this `.ExtractionTraceBuilder`
        """

    @abstractmethod
    def add_tracelet(self, value: Tracelet) -> 'ExtractionTraceBuilder':
        """
        Updates or add metadata properties for this `.ExtractionTraceBuilder`.
        Can be used to update the name of the Trace represented by this builder,
        if not already set.

        :param value: the Tracelet to add
        :return: this `.ExtractionTraceBuilder`
        """

    @abstractmethod
    def child_builder(self, name: str = None) -> 'ExtractionTraceBuilder':
        """
        Creates a new `.TraceBuilder` to build a child trace to the trace to be
        represented by this builder.

        .. note::
            Traces should be created and built in depth first order,
            parent before child (pre-order).
        :return: a `.TraceBuilder` set up to save a new trace as the child
            trace of this builder
        """

    def add_data(self, stream: str, data: bytes) -> 'ExtractionTraceBuilder':
        """
        Add data to this trace as a named stream.

        :param stream: name of the data stream to be added
        :param data: data to be attached
        :return: this `.ExtractionTraceBuilder`
        """
        return self.update(data={stream: data})

    @abstractmethod
    def build(self) -> str:
        """
        Save the trace being built by this builder to remote.

        .. note::
            Building more than once will result in an error being raised.
        :return: the new trace' id
        """


class MetaExtractionTrace(ABC):
    """
       ExtractionTrace definition. ExtractionTraces represent traces during the
       extraction of an extraction plugin.
       """

    @abstractmethod
    def get(self, key: str, default: Any = None) -> Any:
        """
        Returns metadata properties for this `.ExtractionTrace`.

        :param key: the metadata property to be retrieved
        :param default: value returned if property is not set
        :return: the value of the requested metadata property
        """

    @abstractmethod
    def update(self, key_or_updates: Union[Mapping, str] = None, value: Any = None,
               data: Mapping[str, bytes] = None) -> None:
        """
        Updates or add metadata properties for this `.ExtractionTrace`.

        :param key_or_updates: either a `str` (the metadata property to be
            updated) or a mapping supplying both keys and values to be updated
        :param value: the value to update metadata property *key* to (used
            only when *key_or_updates* is a `str`, an exception will be thrown
            if *key_or_updates* is a mapping)
        :param data: a `dict` mapping data type / stream name to bytes to be
            added to the trace
        """

    @abstractmethod
    def add_tracelet(self, value: Tracelet) -> None:
        """
        Updates or add metadata properties for this `.ExtractionTraceBuilder`.
        Can be used to update the name of the Trace represented by this builder,
        if not already set.

        :param value: the Tracelet to add
        """

    @abstractmethod
    def child_builder(self, name: str = None) -> ExtractionTraceBuilder:
        """
        Create a `.TraceBuilder` to build a trace to be saved as a child of
        this `.Trace`.
        A new trace will only be added to the index once explicitly saved (e.g.
        through `.TraceBuilder.build`).

        .. note::
            Traces should be created and built in depth first order,
            parent before child (pre-order).
        :param name: the name for the trace being built
        :return: a `.TraceBuilder` set up to create a child trace of this
            `.ExtractionTrace`
        """


class ExtractionTrace(MetaExtractionTrace):
    @abstractmethod
    def open(self, offset: int = 0, size: int = None) -> BufferedReader:
        """
        Open a data stream of the data stream that is being processed.

        :param offset: byte offset to start the stream on
        :param size: the number of bytes to make available
        :return: a file-like object to read bytes from the named stream
        """


def validate_update_arguments(key_or_updates, value):
    """
    Helper method that validates the arguments for update(...).
    """
    if not isinstance(key_or_updates, str) and not isinstance(key_or_updates, Mapping):
        raise TypeError('argument `key_or_updates` should be either a str or mapping')

    if isinstance(key_or_updates, str) and value is None:
        raise TypeError('update with key missing value')

    if isinstance(key_or_updates, Mapping) and value is not None:
        raise TypeError('update with Mapping should not have argument value set')
