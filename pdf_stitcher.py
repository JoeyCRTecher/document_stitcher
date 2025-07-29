#!/usr/bin/env python3
"""
PDF Stitcher - A simple tool to combine multiple PDF files into one.
"""

import os
import sys
import glob
from pathlib import Path
from typing import List, Optional
import click
from pypdf import PdfWriter, PdfReader
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io


class PDFStitcher:
    """A class to handle PDF stitching operations."""
    
    def __init__(self, show_source: bool = True):
        self.writer = PdfWriter()
        self.processed_files = []
        self.failed_files = []
        self.show_source = show_source
    
    def create_source_page(self, filename: str) -> PdfReader:
        """
        Create a PDF page with source filename information.
        
        Args:
            filename: The source filename to display
            
        Returns:
            PdfReader: A reader for the created source page
        """
        # Create a BytesIO buffer to hold the PDF
        buffer = io.BytesIO()
        
        # Create a canvas for the source page
        c = canvas.Canvas(buffer, pagesize=letter)
        width, height = letter
        
        # Add source filename text
        source_text = f"source: {os.path.basename(filename)}"
        c.setFont("Helvetica-Bold", 14)
        c.drawString(72, height - 72, source_text)
        
        # Save the canvas
        c.save()
        
        # Reset buffer position and create reader
        buffer.seek(0)
        return PdfReader(buffer)
    
    def add_pdf(self, pdf_path: str) -> bool:
        """
        Add a PDF file to the stitcher.
        
        Args:
            pdf_path: Path to the PDF file
            
        Returns:
            bool: True if successfully added, False otherwise
        """
        try:
            with open(pdf_path, 'rb') as file:
                reader = PdfReader(file)
                
                # Check if PDF is encrypted
                if reader.is_encrypted:
                    click.echo(f"⚠️  Warning: '{pdf_path}' is encrypted and will be skipped")
                    self.failed_files.append(pdf_path)
                    return False
                
                # Add source page if show_source is enabled
                if self.show_source:
                    source_reader = self.create_source_page(pdf_path)
                    for page in source_reader.pages:
                        self.writer.add_page(page)
                
                # Add all pages from the PDF
                for page in reader.pages:
                    self.writer.add_page(page)
                
                self.processed_files.append(pdf_path)
                click.echo(f"✅ Added: {os.path.basename(pdf_path)} ({len(reader.pages)} pages)")
                return True
                
        except Exception as e:
            click.echo(f"❌ Error processing '{pdf_path}': {str(e)}")
            self.failed_files.append(pdf_path)
            return False
    
    def save_stitched_pdf(self, output_path: str) -> bool:
        """
        Save the stitched PDF to the specified path.
        
        Args:
            output_path: Path where the stitched PDF will be saved
            
        Returns:
            bool: True if successfully saved, False otherwise
        """
        try:
            with open(output_path, 'wb') as output_file:
                self.writer.write(output_file)
            return True
        except Exception as e:
            click.echo(f"❌ Error saving stitched PDF: {str(e)}")
            return False
    
    def get_stats(self) -> dict:
        """Get statistics about the stitching operation."""
        return {
            'processed': len(self.processed_files),
            'failed': len(self.failed_files),
            'total_pages': len(self.writer.pages)
        }


def find_pdf_files(directory: str, pattern: str = "*.pdf") -> List[str]:
    """
    Find all PDF files in a directory.
    
    Args:
        directory: Directory to search for PDF files
        pattern: File pattern to match (default: "*.pdf")
        
    Returns:
        List of PDF file paths sorted alphabetically
    """
    search_path = os.path.join(directory, pattern)
    pdf_files = glob.glob(search_path)
    return sorted(pdf_files)


@click.command()
@click.option('--input-dir', '-i', 
              help='Directory containing PDF files to stitch')
@click.option('--files', '-f', multiple=True,
              help='Specific PDF files to stitch (can be used multiple times)')
@click.option('--output', '-o', default='stitched_document.pdf',
              help='Output filename for the stitched PDF (default: stitched_document.pdf)')
@click.option('--pattern', '-p', default='*.pdf',
              help='File pattern to match in input directory (default: *.pdf)')
@click.option('--verbose', '-v', is_flag=True,
              help='Enable verbose output')
@click.option('--no-source', is_flag=True,
              help='Disable adding source filename before each PDF content')
def main(input_dir: Optional[str], files: tuple, output: str, pattern: str, verbose: bool, no_source: bool):
    """
    PDF Stitcher - Combine multiple PDF files into a single document.
    
    Examples:
        # Stitch all PDFs in a directory
        python pdf_stitcher.py -i /path/to/pdfs -o combined.pdf
        
        # Stitch specific files
        python pdf_stitcher.py -f file1.pdf -f file2.pdf -o result.pdf
        
        # Stitch PDFs with a specific pattern
        python pdf_stitcher.py -i /path/to/pdfs -p "chapter_*.pdf" -o book.pdf
    """
    
    click.echo("🔗 PDF Stitcher v1.0")
    click.echo("=" * 50)
    
    # Determine which files to process
    pdf_files = []
    
    if files:
        # Use specific files provided
        pdf_files = list(files)
        click.echo(f"📁 Processing {len(pdf_files)} specified files...")
    elif input_dir:
        # Find PDFs in directory
        if not os.path.isdir(input_dir):
            click.echo(f"❌ Error: Directory '{input_dir}' does not exist")
            sys.exit(1)
        
        pdf_files = find_pdf_files(input_dir, pattern)
        click.echo(f"📁 Found {len(pdf_files)} PDF files in '{input_dir}'")
    else:
        # No input specified, look in current directory
        current_dir = os.getcwd()
        pdf_files = find_pdf_files(current_dir, pattern)
        click.echo(f"📁 Found {len(pdf_files)} PDF files in current directory")
    
    if not pdf_files:
        click.echo("❌ No PDF files found to process")
        sys.exit(1)
    
    # Validate that all files exist
    for pdf_file in pdf_files:
        if not os.path.isfile(pdf_file):
            click.echo(f"❌ Error: File '{pdf_file}' does not exist")
            sys.exit(1)
    
    if verbose:
        click.echo("\n📋 Files to process:")
        for i, pdf_file in enumerate(pdf_files, 1):
            click.echo(f"  {i}. {pdf_file}")
        click.echo()
    
    # Create stitcher and process files
    stitcher = PDFStitcher(show_source=not no_source)
    
    click.echo("🔄 Processing PDF files...")
    with click.progressbar(pdf_files, label='Stitching PDFs') as bar:
        for pdf_file in bar:
            stitcher.add_pdf(pdf_file)
    
    # Save the result
    click.echo(f"\n💾 Saving stitched PDF as '{output}'...")
    if stitcher.save_stitched_pdf(output):
        stats = stitcher.get_stats()
        click.echo(f"✅ Successfully created '{output}'!")
        click.echo(f"📊 Statistics:")
        click.echo(f"   • Files processed: {stats['processed']}")
        click.echo(f"   • Files failed: {stats['failed']}")
        click.echo(f"   • Total pages: {stats['total_pages']}")
        
        if stats['failed'] > 0:
            click.echo(f"\n⚠️  {stats['failed']} files failed to process:")
            for failed_file in stitcher.failed_files:
                click.echo(f"   • {failed_file}")
    else:
        click.echo("❌ Failed to save stitched PDF")
        sys.exit(1)


if __name__ == '__main__':
    main()
