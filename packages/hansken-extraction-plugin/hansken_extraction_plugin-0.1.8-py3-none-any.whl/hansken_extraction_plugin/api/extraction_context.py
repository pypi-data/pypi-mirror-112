class ExtractionContext:
    def __init__(self, data_type: str = None, data_size: int = None):
        self._data_type = data_type
        self._data_size = data_size

    def data_type(self):
        """

        :return: The data type of the data currently being processed
        """
        return self._data_type

    def data_size(self):
        """

        :return: The total size of the data stream currently being processed
        """
        return self._data_size

    def __eq__(self, other):
        if not isinstance(other, ExtractionContext):
            return False

        return self._data_size == other._data_size and self._data_type == other._data_type
