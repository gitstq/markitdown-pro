"""
Base converter class for MarkItDown-Pro
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional


class BaseConverter(ABC):
    """
    Abstract base class for all document converters
    
    All converters must inherit from this class and implement
    the convert method.
    """
    
    # Converter metadata
    name: str = "base"
    description: str = "Base converter"
    supported_extensions: list = []
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize converter
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
    
    @abstractmethod
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert a file to Markdown
        
        Args:
            file_path: Path to the input file
            options: Conversion options
            
        Returns:
            Markdown content as string
        """
        pass
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from file
        
        Args:
            file_path: Path to the file
            
        Returns:
            Dictionary of metadata
        """
        import os
        from pathlib import Path
        
        path = Path(file_path)
        stat = os.stat(file_path)
        
        return {
            'filename': path.name,
            'extension': path.suffix,
            'size_bytes': stat.st_size,
            'converter': self.name,
        }
    
    def is_supported(self, file_path: str) -> bool:
        """
        Check if file is supported by this converter
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if supported, False otherwise
        """
        from pathlib import Path
        ext = Path(file_path).suffix.lower()
        return ext in self.supported_extensions
    
    def escape_markdown(self, text: str) -> str:
        """
        Escape special Markdown characters
        
        Args:
            text: Input text
            
        Returns:
            Escaped text
        """
        # Characters that need escaping in Markdown
        special_chars = ['\\', '`', '*', '_', '{', '}', '[', ']', '(', ')', '#', '+', '-', '.', '!', '|']
        
        for char in special_chars:
            text = text.replace(char, '\\' + char)
        
        return text
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text content
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Remove null bytes
        text = text.replace('\x00', '')
        
        # Normalize line endings
        text = text.replace('\r\n', '\n').replace('\r', '\n')
        
        # Remove excessive blank lines
        lines = text.split('\n')
        normalized_lines = []
        prev_blank = False
        
        for line in lines:
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue
            normalized_lines.append(line)
            prev_blank = is_blank
        
        return '\n'.join(normalized_lines)
    
    def create_table(self, headers: list, rows: list) -> str:
        """
        Create Markdown table
        
        Args:
            headers: List of column headers
            rows: List of row data (each row is a list)
            
        Returns:
            Markdown table string
        """
        if not headers:
            return ""
        
        # Escape pipe characters in data
        headers = [str(h).replace('|', '\\|') for h in headers]
        rows = [[str(cell).replace('|', '\\|') for cell in row] for row in rows]
        
        # Build table
        lines = []
        lines.append('| ' + ' | '.join(headers) + ' |')
        lines.append('|' + '|'.join(['---' for _ in headers]) + '|')
        
        for row in rows:
            # Pad row if needed
            while len(row) < len(headers):
                row.append('')
            lines.append('| ' + ' | '.join(row[:len(headers)]) + ' |')
        
        return '\n'.join(lines)
    
    def create_code_block(self, code: str, language: str = "") -> str:
        """
        Create Markdown code block
        
        Args:
            code: Code content
            language: Programming language
            
        Returns:
            Markdown code block
        """
        return f"```{language}\n{code}\n```"
    
    def create_heading(self, text: str, level: int = 1) -> str:
        """
        Create Markdown heading
        
        Args:
            text: Heading text
            level: Heading level (1-6)
            
        Returns:
            Markdown heading
        """
        level = max(1, min(6, level))
        return f"{'#' * level} {text}"
    
    def create_link(self, text: str, url: str) -> str:
        """
        Create Markdown link
        
        Args:
            text: Link text
            url: URL
            
        Returns:
            Markdown link
        """
        return f"[{text}]({url})"
    
    def create_image(self, alt_text: str, url: str) -> str:
        """
        Create Markdown image
        
        Args:
            alt_text: Alternative text
            url: Image URL
            
        Returns:
            Markdown image
        """
        return f"![{alt_text}]({url})"
