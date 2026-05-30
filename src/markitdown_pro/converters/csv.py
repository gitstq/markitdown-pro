"""
CSV converter for MarkItDown-Pro
"""

import csv
from typing import Dict, Any, Optional, List
from .base import BaseConverter


class CSVConverter(BaseConverter):
    """
    Converter for CSV files
    
    Converts CSV files to Markdown tables with statistics.
    """
    
    name = "csv"
    description = "CSV to Markdown converter"
    supported_extensions = ['.csv']
    
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert CSV file to Markdown
        
        Args:
            file_path: Path to CSV file
            options: Conversion options
            
        Returns:
            Markdown content
        """
        options = options or {}
        encoding = options.get('encoding', 'utf-8')
        delimiter = options.get('delimiter', ',')
        include_stats = options.get('include_stats', True)
        max_rows = options.get('max_rows', 1000)
        
        # Read CSV
        rows = self._read_csv(file_path, encoding, delimiter)
        
        if not rows:
            return "# CSV Document\n\n*Empty file*"
        
        headers = rows[0]
        data_rows = rows[1:]
        
        # Build Markdown
        lines = []
        lines.append("# CSV Document\n")
        
        # Add statistics
        if include_stats:
            lines.append("## Statistics\n")
            lines.append(f"- **Total Rows**: {len(data_rows)}")
            lines.append(f"- **Total Columns**: {len(headers)}")
            lines.append(f"- **Headers**: {', '.join(headers)}")
            lines.append("")
        
        # Add table
        lines.append("## Data\n")
        
        # Limit rows for display
        display_rows = data_rows[:max_rows]
        if len(data_rows) > max_rows:
            lines.append(f"*Showing first {max_rows} rows of {len(data_rows)} total*\n")
        
        lines.append(self.create_table(headers, display_rows))
        
        if len(data_rows) > max_rows:
            lines.append(f"\n*{len(data_rows) - max_rows} more rows not shown*")
        
        return '\n'.join(lines)
    
    def _read_csv(self, file_path: str, encoding: str, delimiter: str) -> List[List[str]]:
        """
        Read CSV file
        
        Args:
            file_path: Path to CSV file
            encoding: File encoding
            delimiter: Field delimiter
            
        Returns:
            List of rows
        """
        rows = []
        
        with open(file_path, 'r', encoding=encoding, errors='replace', newline='') as f:
            # Try to detect dialect
            sample = f.read(8192)
            f.seek(0)
            
            try:
                dialect = csv.Sniffer().sniff(sample, delimiters=delimiter)
                reader = csv.reader(f, dialect)
            except csv.Error:
                # Fall back to specified delimiter
                reader = csv.reader(f, delimiter=delimiter)
            
            for row in reader:
                rows.append(row)
        
        return rows
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from CSV file
        
        Args:
            file_path: Path to CSV file
            
        Returns:
            Dictionary of metadata
        """
        metadata = super().get_metadata(file_path)
        
        try:
            rows = self._read_csv(file_path, 'utf-8', ',')
            if rows:
                metadata['headers'] = rows[0]
                metadata['row_count'] = len(rows) - 1
                metadata['column_count'] = len(rows[0])
        except Exception:
            pass
        
        return metadata
