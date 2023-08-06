from typing import Any

from attr import dataclass

from hansken_extraction_plugin.api.author import Author
from hansken_extraction_plugin.api.maturity_level import MaturityLevel


@dataclass
class PluginInfo:
    plugin: Any  # noqa
    name: str
    version: str
    description: str
    author: Author
    maturity: MaturityLevel
    matcher: str
    webpage_url: str
