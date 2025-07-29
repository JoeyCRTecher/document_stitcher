#!/usr/bin/env python3
"""
Example script demonstrating how to use the PDFStitcher class programmatically.
"""

from pdf_stitcher import PDFStitcher
import os

def example_basic_stitching():
    """Basic example of stitching PDFs programmatically."""
    print("Example: Basic PDF Stitching with Source Information")
    print("=" * 60)
    
    # Create a stitcher instance with source information enabled (default)
    stitcher = PDFStitcher(show_source=True)
    
    # Example PDF files (you would replace these with actual file paths)
    pdf_files = [
        "document1.pdf",
        "document2.pdf", 
        "document3.pdf"
    ]
    
    # Add each PDF to the stitcher
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            success = stitcher.add_pdf(pdf_file)
            if success:
                print(f"✅ Added {pdf_file}")
            else:
                print(f"❌ Failed to add {pdf_file}")
        else:
            print(f"⚠️  File not found: {pdf_file}")
    
    # Save the stitched result
    output_file = "stitched_with_source.pdf"
    if stitcher.save_stitched_pdf(output_file):
        stats = stitcher.get_stats()
        print(f"\n✅ Successfully created {output_file}")
        print(f"📊 Files processed: {stats['processed']}")
        print(f"📊 Total pages: {stats['total_pages']}")
    else:
        print("❌ Failed to save stitched PDF")

def example_without_source():
    """Example of stitching PDFs without source information."""
    print("\nExample: PDF Stitching without Source Information")
    print("=" * 60)
    
    # Create a stitcher instance with source information disabled
    stitcher = PDFStitcher(show_source=False)
    
    # Example PDF files (you would replace these with actual file paths)
    pdf_files = [
        "document1.pdf",
        "document2.pdf", 
        "document3.pdf"
    ]
    
    # Add each PDF to the stitcher
    for pdf_file in pdf_files:
        if os.path.exists(pdf_file):
            success = stitcher.add_pdf(pdf_file)
            if success:
                print(f"✅ Added {pdf_file}")
            else:
                print(f"❌ Failed to add {pdf_file}")
        else:
            print(f"⚠️  File not found: {pdf_file}")
    
    # Save the stitched result
    output_file = "stitched_without_source.pdf"
    if stitcher.save_stitched_pdf(output_file):
        stats = stitcher.get_stats()
        print(f"\n✅ Successfully created {output_file}")
        print(f"📊 Files processed: {stats['processed']}")
        print(f"📊 Total pages: {stats['total_pages']}")
    else:
        print("❌ Failed to save stitched PDF")

def example_directory_processing():
    """Example of processing all PDFs in a directory."""
    print("\nExample: Directory Processing")
    print("=" * 40)
    
    # Directory containing PDFs
    pdf_directory = "sample_pdfs"  # Replace with actual directory
    
    if not os.path.exists(pdf_directory):
        print(f"⚠️  Directory {pdf_directory} not found")
        return
    
    # Find all PDF files in directory
    pdf_files = []
    for file in os.listdir(pdf_directory):
        if file.lower().endswith('.pdf'):
            pdf_files.append(os.path.join(pdf_directory, file))
    
    # Sort files alphabetically
    pdf_files.sort()
    
    print(f"Found {len(pdf_files)} PDF files")
    
    # Create stitcher and process files
    stitcher = PDFStitcher(show_source=True)  # Show source filenames by default
    
    for pdf_file in pdf_files:
        stitcher.add_pdf(pdf_file)
    
    # Save result
    output_file = "directory_stitched.pdf"
    if stitcher.save_stitched_pdf(output_file):
        stats = stitcher.get_stats()
        print(f"\n✅ Created {output_file}")
        print(f"📊 Statistics: {stats}")

if __name__ == "__main__":
    # Run examples
    example_basic_stitching()
    example_without_source()
    example_directory_processing()
    
    print("\n" + "=" * 50)
    print("These are examples - replace file paths with your actual PDFs!")
    print("For command-line usage, run: python pdf_stitcher.py --help")
    print("Use --no-source flag to disable source filename display")
