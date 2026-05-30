"""
EPUB converter for MarkItDown-Pro

Note: This converter requires ebooklib to be installed.
Install with: pip install ebooklib
"""

import os
import tempfile
from typing import Dict, Any, Optional
from .base import BaseConverter


class EPUBConverter(BaseConverter):
    """
    Converter for EPUB files
    
    Converts EPUB e-books to Markdown with chapter structure preservation.
    Requires ebooklib: pip install ebooklib
    """
    
    name = "epub"
    description = "EPUB to Markdown converter"
    supported_extensions = ['.epub']
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize EPUB converter
        
        Args:
            config: Optional configuration
        """
        super().__init__(config)
        
        # Try to import ebooklib
        try:
            import ebooklib
            from ebooklib import epub
            self.ebooklib = ebooklib
            self.epub = epub
        except ImportError:
            raise ImportError(
                "ebooklib is required for EPUB conversion. "
                "Install with: pip install ebooklib"
            )
    
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert EPUB file to Markdown
        
        Args:
            file_path: Path to EPUB file
            options: Conversion options
            
        Returns:
            Markdown content
        """
        options = options or {}
        include_toc = options.get('include_toc', True)
        preserve_chapters = options.get('preserve_chapters', True)
        
        lines = []
        
        try:
            # Read EPUB
            book = self.epub.read_epub(file_path)
            
            # Add title
            title = book.get_metadata('DC', 'title')
            if title:
                lines.append(f"# {title[0][0]}\n")
            else:
                lines.append("# EPUB Document\n")
            
            # Add metadata
            lines.append("## Metadata\n")
            
            author = book.get_metadata('DC', 'creator')
            if author:
                lines.append(f"**Author**: {author[0][0]}")
            
            language = book.get_metadata('DC', 'language')
            if language:
                lines.append(f"**Language**: {language[0][0]}")
            
            publisher = book.get_metadata('DC', 'publisher')
            if publisher:
                lines.append(f"**Publisher**: {publisher[0][0]}")
            
            lines.append("")
            
            # Process chapters
            lines.append("## Content\n")
            
            # Get all HTML items
            html_items = list(book.get_items_of_type(self.ebooklib.ITEM_DOCUMENT))
            
            for i, item in enumerate(html_items):
                content = item.get_content().decode('utf-8', errors='replace')
                
                # Convert HTML to Markdown
                md_content = self._html_to_markdown(content)
                
                if preserve_chapters:
                    lines.append(f"### Chapter {i + 1}\n")
                
                lines.append(md_content)
                lines.append("")
            
        except Exception as e:
            lines.append(f"**Error converting EPUB**: {str(e)}")
        
        return '\n'.join(lines)
    
    def _html_to_markdown(self, html: str) -> str:
        """
        Convert HTML content to Markdown
        
        Args:
            html: HTML content
            
        Returns:
            Markdown content
        """
        import re
        from html import unescape
        
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert headings
        for i in range(6, 0, -1):
            pattern = rf'<h{i}[^>]*>(.*?)</h{i}>'
            replacement = rf'{"#" * (i + 2)} \1\n\n'  # Offset by 2 (book title and content header)
            html = re.sub(pattern, replacement, html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert paragraphs
        html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert line breaks
        html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
        
        # Convert bold and strong
        html = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert italic and em
        html = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert links
        html = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert images
        html = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)', html, flags=re.IGNORECASE)
        
        # Remove remaining tags
        html = re.sub(r'<[^>]+>', '', html)
        
        # Unescape HTML entities
        html = unescape(html)
        
        # Clean up whitespace
        html = re.sub(r'\n{3,}', '\n\n', html)
        
        return html.strip()
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from EPUB file
        
        Args:
            file_path: Path to EPUB file
            
        Returns:
            Dictionary of metadata
        """
        metadata = super().get_metadata(file_path)
        
        try:
            book = self.epub.read_epub(file_path)
            
            # Extract metadata
            title = book.get_metadata('DC', 'title')
            if title:
                metadata['title'] = title[0][0]
            
            author = book.get_metadata('DC', 'creator')
            if author:
                metadata['author'] = author[0][0]
            
            language = book.get_metadata('DC', 'language')
            if language:
                metadata['language'] = language[0][0]
            
            publisher = book.get_metadata('DC', 'publisher')
            if publisher:
                metadata['publisher'] = publisher[0][0]
            
            # Count items
            metadata['document_count'] = len(list(book.get_items_of_type(self.ebooklib.ITEM_DOCUMENT)))
            metadata['image_count'] = len(list(book.get_items_of_type(self.ebooklib.ITEM_IMAGE)))
            
        except Exception:
            pass
        
        return metadata
