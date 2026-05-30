"""
PDF converter for MarkItDown-Pro

Note: This converter requires PyPDF2 or pdfplumber to be installed.
Install with: pip install PyPDF2
"""

from typing import Dict, Any, Optional
from .base import BaseConverter


class PDFConverter(BaseConverter):
    """
    Converter for PDF files
    
    Converts PDF documents to Markdown with text extraction.
    Requires PyPDF2: pip install PyPDF2
    """
    
    name = "pdf"
    description = "PDF to Markdown converter"
    supported_extensions = ['.pdf']
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize PDF converter
        
        Args:
            config: Optional configuration
        """
        super().__init__(config)
        
        # Try to import PyPDF2
        try:
            import PyPDF2
            self.PyPDF2 = PyPDF2
        except ImportError:
            raise ImportError(
                "PyPDF2 is required for PDF conversion. "
                "Install with: pip install PyPDF2"
            )
    
    def convert(self, file_path: str, options: Optional[Dict[str, Any]] = None) -> str:
        """
        Convert PDF file to Markdown
        
        Args:
            file_path: Path to PDF file
            options: Conversion options
            
        Returns:
            Markdown content
        """
        options = options or {}
        preserve_layout = options.get('preserve_layout', True)
        page_separator = options.get('page_separator', '\n\n---\n\n')
        
        lines = []
        lines.append("# PDF Document\n")
        
        # Extract text from PDF
        try:
            with open(file_path, 'rb') as f:
                pdf_reader = self.PyPDF2.PdfReader(f)
                num_pages = len(pdf_reader.pages)
                
                lines.append(f"**Total Pages**: {num_pages}\n")
                lines.append("## Content\n")
                
                for page_num in range(num_pages):
                    page = pdf_reader.pages[page_num]
                    text = page.extract_text()
                    
                    if text.strip():
                        lines.append(f"### Page {page_num + 1}\n")
                        
                        if preserve_layout:
                            # Try to preserve paragraph structure
                            paragraphs = self._split_paragraphs(text)
                            for para in paragraphs:
                                if para.strip():
                                    lines.append(para.strip())
                                    lines.append("")
                        else:
                            lines.append(text.strip())
                        
                        if page_num < num_pages - 1:
                            lines.append(page_separator)
                
        except Exception as e:
            lines.append(f"**Error extracting PDF**: {str(e)}")
        
        return '\n'.join(lines)
    
    def _split_paragraphs(self, text: str) -> list:
        """
        Split text into paragraphs
        
        Args:
            text: Raw text
            
        Returns:
            List of paragraphs
        """
        # Split on multiple newlines
        paragraphs = text.split('\n\n')
        
        # Further split on lines that look like new paragraphs
        result = []
        for para in paragraphs:
            # Split lines that start with capital letters after a period
            lines = para.split('\n')
            current_para = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Check if this looks like a new paragraph
                if current_para and line[0].isupper() and current_para[-1].endswith('.'):
                    result.append(' '.join(current_para))
                    current_para = [line]
                else:
                    current_para.append(line)
            
            if current_para:
                result.append(' '.join(current_para))
        
        return result
    
    def get_metadata(self, file_path: str) -> Dict[str, Any]:
        """
        Extract metadata from PDF file
        
        Args:
            file_path: Path to PDF file
            
        Returns:
            Dictionary of metadata
        """
        metadata = super().get_metadata(file_path)
        
        try:
            with open(file_path, 'rb') as f:
                pdf_reader = self.PyPDF2.PdfReader(f)
                
                metadata['page_count'] = len(pdf_reader.pages)
                
                # Extract PDF metadata
                if pdf_reader.metadata:
                    pdf_meta = pdf_reader.metadata
                    if pdf_meta.title:
                        metadata['title'] = pdf_meta.title
                    if pdf_meta.author:
                        metadata['author'] = pdf_meta.author
                    if pdf_meta.subject:
                        metadata['subject'] = pdf_meta.subject
                    if pdf_meta.creator:
                        metadata['creator'] = pdf_meta.creator
                    if pdf_meta.producer:
                        metadata['producer'] = pdf_meta.producer
                
        except Exception:
            pass
        
        return metadata
