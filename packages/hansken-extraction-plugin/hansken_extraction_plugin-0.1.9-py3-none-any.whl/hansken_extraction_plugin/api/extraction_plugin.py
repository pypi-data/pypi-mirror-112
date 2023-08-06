from abc import ABC, abstractmethod

from hansken_extraction_plugin.api.extraction_context import ExtractionContext
from hansken_extraction_plugin.api.extraction_trace import ExtractionTrace, MetaExtractionTrace
from hansken_extraction_plugin.api.plugin_info import PluginInfo
from hansken_extraction_plugin.api.trace_searcher import TraceSearcher


class BaseExtractionPlugin(ABC):
    @abstractmethod
    def plugin_info(self) -> PluginInfo:
        """
        Implement this method to return information about the implemented plugin
        """


class ExtractionPlugin(BaseExtractionPlugin):
    @abstractmethod
    def process(self, trace: ExtractionTrace, context: ExtractionContext):
        """
        Method that is called for each trace that will be processed by this tool
        :param trace: Trace that is being processed
        :param context: Context describing the current extraction run
        """


class MetaExtractionPlugin(BaseExtractionPlugin):
    @abstractmethod
    def process(self, trace: MetaExtractionTrace):
        """
        Method that is called for each trace that will be processed by this tool
        :param trace: Trace that is being processed
        """


class DeferredExtractionPlugin(BaseExtractionPlugin):
    @abstractmethod
    def process(self, trace: ExtractionTrace, context: ExtractionContext, searcher: TraceSearcher):
        """
        Method that is called for each trace that will be processed by this tool
        :param trace: Trace that is being processed
        :param context: Context describing the current extraction run
        :param searcher: TraceSearcher that can be used to obtain more traces
        """
