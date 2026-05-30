"""
Document converters for MarkItDown-Pro
"""

from .base import BaseConverter
from .text import TextConverter
from .html import HTMLConverter
from .json import JSONConverter
from .xml import XMLConverter
from .csv import CSVConverter
from .markdown import MarkdownConverter

__all__ = [
    "BaseConverter",
    "TextConverter",
    "HTMLConverter",
    "JSONConverter",
    "XMLConverter",
    "CSVConverter",
    "MarkdownConverter",
]

# Optional converters (require additional dependencies)
try:
    from .pdf import PDFConverter
    __all__.append("PDFConverter")
except ImportError:
    pass

try:
    from .docx import DOCXConverter
    __all__.append("DOCXConverter")
except ImportError:
    pass

try:
    from .epub import EPUBConverter
    __all__.append("EPUBConverter")
except ImportError:
    pass

try:
    from .xlsx import XLSXConverter
    __all__.append("XLSXConverter")
except ImportError:
    pass
