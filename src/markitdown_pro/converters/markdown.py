"""
Markdown converter for MarkItDown-Pro
"""

from typing import Dict, Any, Optional
from .base import BaseConverter


class MarkdownConverter(BaseConverter):
    """
    Converter for Markdown files
    
    Passes through Markdown files with optional normalization.
    """
    
    name = "markdown"
    description = "Markdown file handler"
    supported_extensions = ['.md', '.markdown', '.mdown', '.mkd']
    
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Process Markdown file
        
        Args:
            file_path: Path to Markdown file
            options: Processing options
            
        Returns:
            Markdown content
        """
        options = options or {}
        encoding = options.get('encoding', 'utf-8')
        normalize = options.get('normalize', True)
        add_toc = options.get('add_toc', False)
        
        # Read file
        with open(file_path, 'r', encoding=encoding, errors='replace') as f:
            content = f.read()
        
        if normalize:
            content = self._normalize_markdown(content)
        
        if add_toc:
            content = self._add_table_of_contents(content)
        
        return content
    
    def _normalize_markdown(self, content: str) -> str:
        """
        Normalize Markdown content
        
        Args:
            content: Markdown content
            
        Returns:
            Normalized content
        """
        import re
        
        # Normalize line endings
        content = content.replace('\r\n', '\n').replace('\r', '\n')
        
        # Ensure single newline at end of file
        content = content.rstrip() + '\n'
        
        # Normalize heading syntax (ensure space after #)
        content = re.sub(r'^(#{1,6})([^#\s])', r'\1 \2', content, flags=re.MULTILINE)
        
        # Normalize code block syntax
        content = re.sub(r'^```(\w+)\s*$', r'```\1', content, flags=re.MULTILINE)
        
        # Remove excessive blank lines (more than 2)
        content = re.sub(r'\n{4,}', '\n\n\n', content)
        
        return content
    
    def _add_table_of_contents(self, content: str) -> str:
        """
        Add table of contents to Markdown
        
        Args:
            content: Markdown content
            
        Returns:
            Content with TOC
        """
        import re
        
        # Find all headings
        headings = re.findall(r'^(#{1,6})\s+(.+)$', content, flags=re.MULTILINE)
        
        if not headings:
            return content
        
        # Build TOC
        toc_lines = ['# Table of Contents\n']
        
        for level, title in headings:
            depth = len(level) - 1
            # Create anchor link
            anchor = re.sub(r'[^\w\s-]', '', title.lower())
            anchor = re.sub(r'[-\s]+', '-', anchor).strip('-')
            
            indent = '  ' * depth
            toc_lines.append(f"{indent}- [{title}](#{anchor})")
        
        toc_lines.append('')
        
        # Insert TOC at the beginning or after first heading
        toc = '\n'.join(toc_lines)
        
        # Check if there's already a title
        first_heading = re.search(r'^#\s+(.+)$', content, flags=re.MULTILINE)
        if first_heading:
            # Insert after first heading
            pos = first_heading.end()
            return content[:pos] + '\n\n' + toc + content[pos:]
        else:
            # Insert at beginning
            return toc + '\n' + content
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from Markdown file
        
        Args:
            file_path: Path to Markdown file
            
        Returns:
            Dictionary of metadata
        """
        import re
        
        metadata = super().get_metadata(file_path)
        
        try:
            with open(file_path, 'r', encoding='utf-8', errors='replace') as f:
                content = f.read()
            
            # Count headings
            h1_count = len(re.findall(r'^#\s+', content, flags=re.MULTILINE))
            h2_count = len(re.findall(r'^##\s+', content, flags=re.MULTILINE))
            h3_count = len(re.findall(r'^###\s+', content, flags=re.MULTILINE))
            
            metadata['headings'] = {
                'h1': h1_count,
                'h2': h2_count,
                'h3': h3_count,
            }
            
            # Count code blocks
            code_blocks = len(re.findall(r'^```', content, flags=re.MULTILINE)) // 2
            metadata['code_blocks'] = code_blocks
            
            # Count links
            links = len(re.findall(r'\[([^\]]+)\]\(([^)]+)\)', content))
            metadata['links'] = links
            
            # Count images
            images = len(re.findall(r'!\[([^\]]*)\]\(([^)]+)\)', content))
            metadata['images'] = images
            
            # Extract title (first h1)
            title_match = re.search(r'^#\s+(.+)$', content, flags=re.MULTILINE)
            if title_match:
                metadata['title'] = title_match.group(1)
            
        except Exception:
            pass
        
        return metadata
