"""
Plain text converter for MarkItDown-Pro
"""

from typing import Dict, Any, Optional
from .base import BaseConverter


class TextConverter(BaseConverter):
    """
    Converter for plain text files
    
    Converts .txt files to Markdown with basic formatting detection.
    """
    
    name = "text"
    description = "Plain text converter"
    supported_extensions = ['.txt', '.text']
    
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert text file to Markdown
        
        Args:
            file_path: Path to text file
            options: Conversion options
            
        Returns:
            Markdown content
        """
        options = options or {}
        encoding = options.get('encoding', 'utf-8')
        detect_structure = options.get('detect_structure', True)
        
        # Read file
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        
        # Normalize content
        content = self.normalize_text(content)
        
        if detect_structure:
            content = self._detect_structure(content)
        
        return content
    
    def _detect_structure(self, content: str) -> str:
        """
        Detect and format structure in text
        
        Args:
            content: Raw text content
            
        Returns:
            Formatted Markdown content
        """
        lines = content.split('\n')
        result_lines = []
        
        for line in lines:
            stripped = line.strip()
            
            # Skip empty lines
            if not stripped:
                result_lines.append('')
                continue
            
            # Detect headings (ALL CAPS or underlined)
            if stripped.isupper() and len(stripped) < 100:
                result_lines.append(f"## {stripped}")
                continue
            
            # Detect bullet points
            if stripped.startswith(('•', '-', '*', '·')):
                result_lines.append(f"- {stripped[1:].strip()}")
                continue
            
            # Detect numbered lists
            if len(stripped) > 2 and stripped[0].isdigit() and stripped[1] in '.)':
                result_lines.append(line)
                continue
            
            # Detect URLs and convert to links
            line = self._convert_urls(line)
            
            result_lines.append(line)
        
        return '\n'.join(result_lines)
    
    def _convert_urls(self, text: str) -> str:
        """
        Convert URLs in text to Markdown links
        
        Args:
            text: Input text
            
        Returns:
            Text with URLs converted to links
        """
        import re
        
        # URL pattern
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        
        def replace_url(match):
            url = match.group(0)
            # Remove trailing punctuation
            while url and url[-1] in '.,;:!?)':
                url = url[:-1]
            return f"[{url}]({url})"
        
        return re.sub(url_pattern, replace_url, text)
