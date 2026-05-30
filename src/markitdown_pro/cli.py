"""
Command-line interface for MarkItDown-Pro
"""

import sys
import os
import argparse
from pathlib import Path
from typing import Optional, List

from .core import MarkItDownPro, ConversionStatus
from .version import __version__


def create_parser() -> argparse.ArgumentParser:
    """Create argument parser"""
    parser = argparse.ArgumentParser(
        prog='markitdown-pro',
        description='MarkItDown-Pro - Lightweight Document to Markdown Conversion Engine',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  markitdown-pro input.pdf                    Convert PDF to Markdown
  markitdown-pro input.docx -o output.md      Convert DOCX to specific output
  markitdown-pro *.csv                        Convert multiple CSV files
  markitdown-pro docs/ --recursive            Convert all files in directory
  markitdown-pro --list-formats               Show supported formats
        """
    )
    
    parser.add_argument(
        'input',
        nargs='*',
        help='Input file(s) or directory'
    )
    
    parser.add_argument(
        '-o', '--output',
        help='Output file or directory'
    )
    
    parser.add_argument(
        '-r', '--recursive',
        action='store_true',
        help='Process directories recursively'
    )
    
    parser.add_argument(
        '-f', '--format',
        help='Specify output format (default: markdown)'
    )
    
    parser.add_argument(
        '--encoding',
        default='utf-8',
        help='Input file encoding (default: utf-8)'
    )
    
    parser.add_argument(
        '--list-formats',
        action='store_true',
        help='List supported file formats'
    )
    
    parser.add_argument(
        '--version',
        action='version',
        version=f'%(prog)s {__version__}'
    )
    
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '-q', '--quiet',
        action='store_true',
        help='Suppress non-error output'
    )
    
    parser.add_argument(
        '--json',
        action='store_true',
        help='Output results as JSON'
    )
    
    return parser


def list_formats(converter: MarkItDownPro) -> None:
    """List supported formats"""
    formats = converter.get_supported_formats()
    
    print("Supported File Formats:")
    print("=" * 50)
    
    for fmt, extensions in sorted(formats.items()):
        ext_str = ', '.join(sorted(extensions))
        print(f"  {fmt:15} {ext_str}")
    
    print()
    print(f"Total: {len(formats)} formats")


def convert_files(args) -> int:
    """
    Convert files based on arguments
    
    Returns:
        Exit code (0 for success, 1 for failure)
    """
    converter = MarkItDownPro()
    
    # Collect input files
    input_paths = []
    
    for pattern in args.input:
        path = Path(pattern)
        
        if path.is_dir():
            # Process directory
            results = converter.convert_directory(
                str(path),
                args.output,
                args.recursive,
                {'encoding': args.encoding}
            )
            input_paths.extend([r.source_path for r in results])
        elif path.exists():
            input_paths.append(str(path))
        else:
            # Try glob pattern
            import glob
            matched = glob.glob(pattern)
            if matched:
                input_paths.extend(matched)
            elif not args.quiet:
                print(f"Warning: File not found: {pattern}", file=sys.stderr)
    
    if not input_paths:
        if not args.quiet:
            print("No input files found.", file=sys.stderr)
        return 1
    
    # Remove duplicates while preserving order
    seen = set()
    input_paths = [p for p in input_paths if not (p in seen or seen.add(p))]
    
    # Convert files
    options = {'encoding': args.encoding}
    results = converter.convert_batch(input_paths, args.output, options)
    
    # Output results
    if args.json:
        import json
        output = [r.to_dict() for r in results]
        print(json.dumps(output, indent=2, ensure_ascii=False))
    else:
        success_count = 0
        fail_count = 0
        
        for result in results:
            if result.status == ConversionStatus.SUCCESS:
                success_count += 1
                if args.verbose:
                    print(f"✓ {result.source_path}")
                    print(f"  → {result.output_path}")
                    print(f"  Time: {result.processing_time:.2f}s")
                    print()
                elif not args.quiet:
                    print(f"✓ {Path(result.source_path).name} → {Path(result.output_path).name}")
            else:
                fail_count += 1
                if not args.quiet:
                    print(f"✗ {result.source_path}")
                    print(f"  Error: {result.error_message}")
                    print()
        
        if not args.quiet:
            print()
            print(f"Conversion complete: {success_count} succeeded, {fail_count} failed")
    
    return 0 if fail_count == 0 else 1


def main(args: Optional[List[str]] = None) -> int:
    """
    Main entry point
    
    Args:
        args: Command-line arguments
        
    Returns:
        Exit code
    """
    parser = create_parser()
    parsed_args = parser.parse_args(args)
    
    converter = MarkItDownPro()
    
    # Handle --list-formats
    if parsed_args.list_formats:
        list_formats(converter)
        return 0
    
    # Check for input files
    if not parsed_args.input:
        parser.print_help()
        return 1
    
    # Convert files
    return convert_files(parsed_args)


if __name__ == '__main__':
    sys.exit(main())
