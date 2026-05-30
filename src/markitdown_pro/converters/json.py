"""
JSON converter for MarkItDown-Pro
"""

import json
from typing import Dict, Any, Optional
from .base import BaseConverter


class JSONConverter(BaseConverter):
    """
    Converter for JSON files
    
    Converts JSON documents to Markdown with formatted code blocks and tables.
    """
    
    name = "json"
    description = "JSON to Markdown converter"
    supported_extensions = ['.json']
    
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert JSON file to Markdown
        
        Args:
            file_path: Path to JSON file
            options: Conversion options
            
        Returns:
            Markdown content
        """
        options = options or {}
        encoding = options.get('encoding', 'utf-8')
        format_as_table = options.get('format_as_table', True)
        max_depth = options.get('max_depth', 3)
        
        # Read and parse JSON
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            data = json.load(f)
        
        # Build Markdown content
        lines = []
        lines.append("# JSON Document\n")
        
        # Add metadata section
        lines.append("## Metadata\n")
        lines.append(f"- **Type**: {type(data).__name__}")
        if isinstance(data, list):
            lines.append(f"- **Item Count**: {len(data)}")
        elif isinstance(data, dict):
            lines.append(f"- **Key Count**: {len(data)}")
        lines.append("")
        
        # Add content section
        lines.append("## Content\n")
        
        if isinstance(data, list) and format_as_table and len(data) > 0:
            # Try to format as table if all items are dicts with same keys
            if all(isinstance(item, dict) for item in data):
                lines.append(self._format_list_as_table(data))
            else:
                lines.append(self._format_list(data, max_depth))
        elif isinstance(data, dict):
            lines.append(self._format_dict(data, max_depth))
        else:
            # Primitive value
            lines.append(f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```")
        
        lines.append("")
        lines.append("## Raw JSON\n")
        lines.append("```json")
        lines.append(json.dumps(data, indent=2, ensure_ascii=False))
        lines.append("```")
        
        return '\n'.join(lines)
    
    def _format_dict(self, data: dict, max_depth: int, current_depth: int = 0) -> str:
        """
        Format dictionary as Markdown
        
        Args:
            data: Dictionary to format
            max_depth: Maximum nesting depth
            current_depth: Current nesting depth
            
        Returns:
            Formatted Markdown string
        """
        if current_depth >= max_depth:
            return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
        
        lines = []
        
        for key, value in data.items():
            heading_level = min(current_depth + 3, 6)  # Start at h3
            
            if isinstance(value, dict):
                lines.append(f"{'#' * heading_level} {key}\n")
                lines.append(self._format_dict(value, max_depth, current_depth + 1))
            elif isinstance(value, list):
                lines.append(f"{'#' * heading_level} {key}\n")
                lines.append(self._format_list(value, max_depth, current_depth + 1))
            else:
                # Primitive value
                lines.append(f"**{key}**: `{self._format_value(value)}`\n")
        
        return '\n'.join(lines)
    
    def _format_list(self, data: list, max_depth: int, current_depth: int = 0) -> str:
        """
        Format list as Markdown
        
        Args:
            data: List to format
            max_depth: Maximum nesting depth
            current_depth: Current nesting depth
            
        Returns:
            Formatted Markdown string
        """
        if current_depth >= max_depth:
            return f"```json\n{json.dumps(data, indent=2, ensure_ascii=False)}\n```"
        
        lines = []
        
        for i, item in enumerate(data):
            if isinstance(item, dict):
                lines.append(f"### Item {i + 1}\n")
                lines.append(self._format_dict(item, max_depth, current_depth + 1))
            elif isinstance(item, list):
                lines.append(f"- Nested list ({len(item)} items)\n")
                lines.append(self._format_list(item, max_depth, current_depth + 1))
            else:
                lines.append(f"- {self._format_value(item)}")
        
        return '\n'.join(lines)
    
    def _format_list_as_table(self, data: list) -> str:
        """
        Format list of dictionaries as Markdown table
        
        Args:
            data: List of dictionaries
            
        Returns:
            Markdown table string
        """
        if not data or not all(isinstance(item, dict) for item in data):
            return self._format_list(data, 3)
        
        # Get all unique keys
        all_keys = set()
        for item in data:
            all_keys.update(item.keys())
        
        # Prioritize common keys
        priority_keys = ['name', 'title', 'id', 'key', 'type', 'value', 'description', 'url', 'link']
        headers = []
        
        for key in priority_keys:
            if key in all_keys:
                headers.append(key)
                all_keys.discard(key)
        
        # Add remaining keys
        headers.extend(sorted(all_keys))
        
        # Limit columns to avoid too wide tables
        max_columns = 8
        if len(headers) > max_columns:
            headers = headers[:max_columns]
        
        # Build rows
        rows = []
        for item in data[:100]:  # Limit to 100 rows
            row = []
            for key in headers:
                value = item.get(key, '')
                row.append(self._format_cell_value(value))
            rows.append(row)
        
        # Create table
        return self.create_table(headers, rows)
    
    def _format_value(self, value: Any) -> str:
        """
        Format a value for display
        
        Args:
            value: Value to format
            
        Returns:
            Formatted string
        """
        if value is None:
            return "null"
        elif isinstance(value, bool):
            return str(value).lower()
        elif isinstance(value, (int, float)):
            return str(value)
        elif isinstance(value, str):
            # Truncate long strings
            if len(value) > 100:
                return value[:100] + "..."
            return value
        else:
            return str(value)
    
    def _format_cell_value(self, value: Any) -> str:
        """
        Format a value for table cell
        
        Args:
            value: Value to format
            
        Returns:
            Formatted string
        """
        if value is None:
            return ""
        elif isinstance(value, bool):
            return "✓" if value else "✗"
        elif isinstance(value, (list, dict)):
            return f"({type(value).__name__})"
        else:
            text = self._format_value(value)
            # Escape pipe characters
            return text.replace('|', '\\|')
