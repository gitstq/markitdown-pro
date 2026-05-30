"""
MarkItDown-Pro - Lightweight Document to Markdown Conversion Engine
轻量级文档转Markdown转换引擎

A zero-dependency CLI tool for converting various document formats to Markdown.
支持PDF、DOCX、EPUB、HTML、图片OCR、CSV、XLSX等多种格式。

Author: MarkItDown-Pro Team
Version: 1.0.0
License: MIT
"""

__version__ = "1.0.0"
__author__ = "MarkItDown-Pro Team"
__license__ = "MIT"

from .core import MarkItDownPro
from .converters import BaseConverter

__all__ = ["MarkItDownPro", "BaseConverter"]
