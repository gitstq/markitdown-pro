"""
Core engine for MarkItDown-Pro
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import Optional, Dict, List, Any, Union
from dataclasses import dataclass, asdict
from enum import Enum


class ConversionStatus(Enum):
    """Conversion status enumeration"""
    PENDING = "pending"
    PROCESSING = "processing"
    SUCCESS = "success"
    FAILED = "failed"
    SKIPPED = "skipped"


@dataclass
class ConversionResult:
    """Conversion result data class"""
    source_path: str
    output_path: Optional[str] = None
    status: ConversionStatus = ConversionStatus.PENDING
    markdown_content: str = ""
    error_message: Optional[str] = None
    metadata: Dict[str, Any] = None
    processing_time: float = 0.0
    
    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary"""
        result = asdict(self)
        result['status'] = self.status.value
        return result
    
    def to_json(self, indent: int = 2) -> str:
        """Convert to JSON string"""
        return json.dumps(self.to_dict(), indent=indent, ensure_ascii=False)


class MarkItDownPro:
    """
    Main conversion engine for MarkItDown-Pro
    
    Features:
    - Multi-format document conversion
    - Batch processing support
    - Plugin-based converter architecture
    - Configurable output options
    """
    
    # Supported file extensions
    SUPPORTED_EXTENSIONS = {
        '.pdf': 'pdf',
        '.docx': 'docx',
        '.doc': 'doc',
        '.epub': 'epub',
        '.html': 'html',
        '.htm': 'html',
        '.txt': 'text',
        '.csv': 'csv',
        '.xlsx': 'xlsx',
        '.xls': 'xlsx',
        '.json': 'json',
        '.xml': 'xml',
        '.md': 'markdown',
        '.png': 'image',
        '.jpg': 'image',
        '.jpeg': 'image',
        '.gif': 'image',
        '.bmp': 'image',
        '.tiff': 'image',
    }
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Initialize MarkItDown-Pro engine
        
        Args:
            config: Optional configuration dictionary
        """
        self.config = config or {}
        self.converters: Dict[str, Any] = {}
        self._load_converters()
    
    def _load_converters(self):
        """Load all available converters"""
        # Import converters lazily to avoid loading unnecessary dependencies
        from .converters import (
            TextConverter, HTMLConverter, JSONConverter,
            XMLConverter, CSVConverter, MarkdownConverter
        )
        
        # Register built-in converters
        self.converters['text'] = TextConverter()
        self.converters['html'] = HTMLConverter()
        self.converters['json'] = JSONConverter()
        self.converters['xml'] = XMLConverter()
        self.converters['csv'] = CSVConverter()
        self.converters['markdown'] = MarkdownConverter()
        
        # Try to load optional converters
        try:
            from .converters import PDFConverter
            self.converters['pdf'] = PDFConverter()
        except ImportError:
            pass
        
        try:
            from .converters import DOCXConverter
            self.converters['docx'] = DOCXConverter()
        except ImportError:
            pass
        
        try:
            from .converters import EPUBConverter
            self.converters['epub'] = EPUBConverter()
        except ImportError:
            pass
        
        try:
            from .converters import XLSXConverter
            self.converters['xlsx'] = XLSXConverter()
        except ImportError:
            pass
    
    def get_file_type(self, file_path: str) -> Optional[str]:
        """
        Determine file type from extension
        
        Args:
            file_path: Path to the file
            
        Returns:
            File type string or None if unsupported
        """
        ext = Path(file_path).suffix.lower()
        return self.SUPPORTED_EXTENSIONS.get(ext)
    
    def is_supported(self, file_path: str) -> bool:
        """
        Check if file format is supported
        
        Args:
            file_path: Path to the file
            
        Returns:
            True if supported, False otherwise
        """
        return self.get_file_type(file_path) is not None
    
    def convert(
        self,
        input_path: str,
        output_path: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> ConversionResult:
        """
        Convert a single file to Markdown
        
        Args:
            input_path: Path to input file
            output_path: Optional output path (auto-generated if not provided)
            options: Conversion options
            
        Returns:
            ConversionResult object
        """
        import time
        
        start_time = time.time()
        input_path = str(Path(input_path).resolve())
        
        # Initialize result
        result = ConversionResult(
            source_path=input_path,
            status=ConversionStatus.PROCESSING
        )
        
        # Check if file exists
        if not os.path.exists(input_path):
            result.status = ConversionStatus.FAILED
            result.error_message = f"File not found: {input_path}"
            result.processing_time = time.time() - start_time
            return result
        
        # Determine file type
        file_type = self.get_file_type(input_path)
        if not file_type:
            result.status = ConversionStatus.FAILED
            result.error_message = f"Unsupported file format: {Path(input_path).suffix}"
            result.processing_time = time.time() - start_time
            return result
        
        # Check if converter is available
        if file_type not in self.converters:
            result.status = ConversionStatus.FAILED
            result.error_message = f"Converter not available for: {file_type}"
            result.processing_time = time.time() - start_time
            return result
        
        try:
            # Get converter
            converter = self.converters[file_type]
            
            # Perform conversion
            options = options or {}
            markdown_content = converter.convert(input_path, options)
            
            # Generate output path if not provided
            if not output_path:
                input_path_obj = Path(input_path)
                output_path = str(
                    input_path_obj.parent / f"{input_path_obj.stem}.md"
                )
            else:
                output_path = str(Path(output_path).resolve())
            
            # Write output file
            os.makedirs(os.path.dirname(output_path) or '.', exist_ok=True)
            with open(output_path, 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            # Update result
            result.output_path = output_path
            result.markdown_content = markdown_content
            result.status = ConversionStatus.SUCCESS
            result.metadata = converter.get_metadata(input_path) if hasattr(converter, 'get_metadata') else {}
            
        except Exception as e:
            result.status = ConversionStatus.FAILED
            result.error_message = str(e)
        
        result.processing_time = time.time() - start_time
        return result
    
    def convert_batch(
        self,
        input_paths: List[str],
        output_dir: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> List[ConversionResult]:
        """
        Convert multiple files to Markdown
        
        Args:
            input_paths: List of input file paths
            output_dir: Optional output directory
            options: Conversion options
            
        Returns:
            List of ConversionResult objects
        """
        results = []
        
        for input_path in input_paths:
            if output_dir:
                filename = Path(input_path).stem + '.md'
                output_path = str(Path(output_dir) / filename)
            else:
                output_path = None
            
            result = self.convert(input_path, output_path, options)
            results.append(result)
        
        return results
    
    def convert_directory(
        self,
        input_dir: str,
        output_dir: Optional[str] = None,
        recursive: bool = False,
        options: Optional[Dict[str, Any]] = None
    ) -> List[ConversionResult]:
        """
        Convert all supported files in a directory
        
        Args:
            input_dir: Input directory path
            output_dir: Optional output directory
            recursive: Whether to process subdirectories
            options: Conversion options
            
        Returns:
            List of ConversionResult objects
        """
        input_dir = Path(input_dir)
        
        if not input_dir.exists():
            return []
        
        # Collect files
        files = []
        pattern = '**/*' if recursive else '*'
        
        for file_path in input_dir.glob(pattern):
            if file_path.is_file() and self.is_supported(str(file_path)):
                files.append(str(file_path))
        
        # Convert files
        if output_dir:
            os.makedirs(output_dir, exist_ok=True)
        
        return self.convert_batch(files, output_dir, options)
    
    def get_supported_formats(self) -> Dict[str, List[str]]:
        """
        Get list of supported formats
        
        Returns:
            Dictionary mapping format names to extensions
        """
        formats = {}
        for ext, fmt in self.SUPPORTED_EXTENSIONS.items():
            if fmt not in formats:
                formats[fmt] = []
            formats[fmt].append(ext)
        return formats
