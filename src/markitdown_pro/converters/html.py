"""
HTML converter for MarkItDown-Pro
"""

import re
from typing import Dict, Any, Optional
from html import unescape
from .base import BaseConverter


class HTMLConverter(BaseConverter):
    """
    Converter for HTML files
    
    Converts HTML documents to Markdown using regex-based parsing.
    """
    
    name = "html"
    description = "HTML to Markdown converter"
    supported_extensions = ['.html', '.htm']
    
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert HTML file to Markdown
        
        Args:
            file_path: Path to HTML file
            options: Conversion options
            
        Returns:
            Markdown content
        """
        options = options or {}
        encoding = options.get('encoding', 'utf-8')
        
        # Read file
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            html = f.read()
        
        return self._html_to_markdown(html)
    
    def _html_to_markdown(self, html: str) -> str:
        """
        Convert HTML string to Markdown
        
        Args:
            html: HTML content
            
        Returns:
            Markdown content
        """
        # Remove script and style tags
        html = re.sub(r'<script[^>]*>.*?</script>', '', html, flags=re.DOTALL | re.IGNORECASE)
        html = re.sub(r'<style[^>]*>.*?</style>', '', html, flags=re.DOTALL | re.IGNORECASE)
        
        # Convert headings
        for i in range(6, 0, -1):
            pattern = rf'<h{i}[^>]*>(.*?)</h{i}>'
            replacement = rf'{"#" * i} \1\n\n'
            html = re.sub(pattern, replacement, html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert paragraphs
        html = re.sub(r'<p[^>]*>(.*?)</p>', r'\1\n\n', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert line breaks
        html = re.sub(r'<br\s*/?>', '\n', html, flags=re.IGNORECASE)
        
        # Convert bold and strong
        html = re.sub(r'<(strong|b)[^>]*>(.*?)</\1>', r'**\2**', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert italic and em
        html = re.sub(r'<(em|i)[^>]*>(.*?)</\1>', r'*\2*', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert code
        html = re.sub(r'<code[^>]*>(.*?)</code>', r'`\1`', html, flags=re.IGNORECASE | re.DOTALL)
        html = re.sub(r'<pre[^>]*>(.*?)</pre>', r'\n```\n\1\n```\n', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert links
        html = re.sub(r'<a[^>]+href=["\']([^"\']+)["\'][^>]*>(.*?)</a>', r'[\2](\1)', html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert images
        html = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*alt=["\']([^"\']*)["\'][^>]*/?>', r'![\2](\1)', html, flags=re.IGNORECASE)
        html = re.sub(r'<img[^>]+alt=["\']([^"\']*)["\'][^>]*src=["\']([^"\']+)["\'][^>]*/?>', r'![\1](\2)', html, flags=re.IGNORECASE)
        html = re.sub(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*/?>', r'![](\1)', html, flags=re.IGNORECASE)
        
        # Convert unordered lists
        html = self._convert_lists(html)
        
        # Convert blockquotes
        html = re.sub(r'<blockquote[^>]*>(.*?)</blockquote>', lambda m: self._convert_blockquote(m.group(1)), html, flags=re.IGNORECASE | re.DOTALL)
        
        # Convert horizontal rules
        html = re.sub(r'<hr\s*/?>', '\n---\n', html, flags=re.IGNORECASE)
        
        # Convert tables
        html = self._convert_tables(html)
        
        # Remove remaining tags
        html = re.sub(r'<[^>]+>', '', html)
        
        # Unescape HTML entities
        html = unescape(html)
        
        # Clean up whitespace
        html = self._clean_whitespace(html)
        
        return html.strip()
    
    def _convert_lists(self, html: str) -> str:
        """Convert HTML lists to Markdown"""
        # Handle unordered lists
        def convert_ul(match):
            content = match.group(1)
            items = re.findall(r'<li[^>]*>(.*?)</li>', content, flags=re.IGNORECASE | re.DOTALL)
            return '\n'.join(f"- {item.strip()}" for item in items) + '\n'
        
        html = re.sub(r'<ul[^>]*>(.*?)</ul>', convert_ul, html, flags=re.IGNORECASE | re.DOTALL)
        
        # Handle ordered lists
        def convert_ol(match):
            content = match.group(1)
            items = re.findall(r'<li[^>]*>(.*?)</li>', content, flags=re.IGNORECASE | re.DOTALL)
            return '\n'.join(f"{i+1}. {item.strip()}" for i, item in enumerate(items)) + '\n'
        
        html = re.sub(r'<ol[^>]*>(.*?)</ol>', convert_ol, html, flags=re.IGNORECASE | re.DOTALL)
        
        return html
    
    def _convert_blockquote(self, content: str) -> str:
        """Convert blockquote content"""
        lines = content.strip().split('\n')
        quoted_lines = ['> ' + line.strip() for line in lines if line.strip()]
        return '\n' + '\n'.join(quoted_lines) + '\n'
    
    def _convert_tables(self, html: str) -> str:
        """Convert HTML tables to Markdown"""
        def convert_table(match):
            table_html = match.group(0)
            
            # Extract headers
            headers = re.findall(r'<th[^>]*>(.*?)</th>', table_html, flags=re.IGNORECASE | re.DOTALL)
            if not headers:
                headers = re.findall(r'<td[^>]*>(.*?)</td>', table_html, flags=re.IGNORECASE | re.DOTALL)
            
            headers = [re.sub(r'<[^>]+>', '', h).strip() for h in headers]
            
            # Extract rows
            rows = []
            for tr_match in re.finditer(r'<tr[^>]*>(.*?)</tr>', table_html, flags=re.IGNORECASE | re.DOTALL):
                cells = re.findall(r'<td[^>]*>(.*?)</td>', tr_match.group(1), flags=re.IGNORECASE | re.DOTALL)
                if cells:
                    cells = [re.sub(r'<[^>]+>', '', c).strip() for c in cells]
                    rows.append(cells)
            
            if not headers and not rows:
                return ''
            
            # Build Markdown table
            result = []
            if headers:
                result.append('| ' + ' | '.join(headers) + ' |')
                result.append('|' + '|'.join(['---' for _ in headers]) + '|')
            
            for row in rows:
                result.append('| ' + ' | '.join(row) + ' |')
            
            return '\n' + '\n'.join(result) + '\n'
        
        return re.sub(r'<table[^>]*>.*?</table>', convert_table, html, flags=re.IGNORECASE | re.DOTALL)
    
    def _clean_whitespace(self, text: str) -> str:
        """Clean up excessive whitespace"""
        # Remove excessive blank lines
        lines = text.split('\n')
        result = []
        prev_blank = False
        
        for line in lines:
            is_blank = not line.strip()
            if is_blank and prev_blank:
                continue
            result.append(line)
            prev_blank = is_blank
        
        return '\n'.join(result)
