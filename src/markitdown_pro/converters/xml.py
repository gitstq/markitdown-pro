"""
XML converter for MarkItDown-Pro
"""

import re
from typing import Dict, Any, Optional
from html import unescape
from .base import BaseConverter


class XMLConverter(BaseConverter):
    """
    Converter for XML files
    
    Converts XML documents to Markdown with structured formatting.
    """
    
    name = "xml"
    description = "XML to Markdown converter"
    supported_extensions = ['.xml']
    
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert XML file to Markdown
        
        Args:
            file_path: Path to XML file
            options: Conversion options
            
        Returns:
            Markdown content
        """
        options = options or {}
        encoding = options.get('encoding', 'utf-8')
        
        # Read file
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            xml_content = f.read()
        
        return self._xml_to_markdown(xml_content)
    
    def _xml_to_markdown(self, xml: str) -> str:
        """
        Convert XML string to Markdown
        
        Args:
            xml: XML content
            
        Returns:
            Markdown content
        """
        lines = []
        lines.append("# XML Document\n")
        
        # Extract root element
        root_match = re.search(r'<(\w+)[^>]*>', xml)
        if root_match:
            root_name = root_match.group(1)
            lines.append(f"**Root Element**: `{root_name}`\n")
        
        # Parse and format structure
        lines.append("## Structure\n")
        lines.append(self._parse_structure(xml))
        
        lines.append("")
        lines.append("## Raw XML\n")
        lines.append("```xml")
        lines.append(xml.strip())
        lines.append("```")
        
        return '\n'.join(lines)
    
    def _parse_structure(self, xml: str, depth: int = 0) -> str:
        """
        Parse XML structure recursively
        
        Args:
            xml: XML content
            depth: Current depth level
            
        Returns:
            Formatted Markdown string
        """
        lines = []
        indent = "  " * depth
        
        # Find all top-level elements
        pattern = r'<(\w+)([^>]*)>(.*?)</\1>'
        matches = list(re.finditer(pattern, xml, re.DOTALL))
        
        if not matches:
            # Try self-closing tags
            pattern = r'<(\w+)([^>]*)/>'
            matches = list(re.finditer(pattern, xml))
            
            for match in matches:
                tag_name = match.group(1)
                attrs = self._parse_attributes(match.group(2))
                attr_str = f" ({', '.join(f'{k}={v}' for k, v in attrs.items())})" if attrs else ""
                lines.append(f"{indent}- **{tag_name}**{attr_str} (self-closing)")
        else:
            for match in matches:
                tag_name = match.group(1)
                attrs = self._parse_attributes(match.group(2))
                content = match.group(3).strip()
                
                attr_str = f" ({', '.join(f'{k}={v}' for k, v in attrs.items())})" if attrs else ""
                
                # Check if content has nested elements
                if re.search(r'<\w+', content):
                    lines.append(f"{indent}- **{tag_name}**{attr_str}")
                    nested = self._parse_structure(content, depth + 1)
                    if nested:
                        lines.append(nested)
                else:
                    # Leaf element with text content
                    text = unescape(content).strip()
                    if text:
                        # Truncate long text
                        if len(text) > 100:
                            text = text[:100] + "..."
                        lines.append(f"{indent}- **{tag_name}**{attr_str}: `{text}`")
                    else:
                        lines.append(f"{indent}- **{tag_name}**{attr_str}")
        
        return '\n'.join(lines)
    
    def _parse_attributes(self, attr_string: str) -> Dict[str, str]:
        """
        Parse XML attributes
        
        Args:
            attr_string: Attribute string
            
        Returns:
            Dictionary of attributes
        """
        attrs = {}
        # Match attribute="value" or attribute='value'
        pattern = r'(\w+)=["\']([^"\']*)["\']'
        for match in re.finditer(pattern, attr_string):
            attrs[match.group(1)] = match.group(2)
        return attrs
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from XML file
        
        Args:
            file_path: Path to XML file
            
        Returns:
            Dictionary of metadata
        """
        metadata = super().get_metadata(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Extract root element
            root_match = re.search(r'<(\w+)[^>]*>', content)
            if root_match:
                metadata['root_element'] = root_match.group(1)
            
            # Count elements
            elements = re.findall(r'<(\w+)[^>]*>', content)
            metadata['element_count'] = len(elements)
            metadata['unique_elements'] = list(set(elements))
            
        except Exception:
            pass
        
        return metadata
