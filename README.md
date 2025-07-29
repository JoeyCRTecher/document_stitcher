# PDF Stitcher

A simple Python tool to combine multiple PDF files into a single document.

## Features

- ✅ Combine multiple PDFs into one document
- ✅ Process entire directories or specific files
- ✅ Command-line interface with progress indicators
- ✅ Error handling for corrupted or encrypted PDFs
- ✅ Customizable output filename and file patterns
- ✅ Verbose mode for detailed processing information
- ✅ **NEW**: Source filename tracking - adds source filename pages to stitched PDFs by default

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Examples

1. **Stitch all PDFs in current directory:**
```bash
python pdf_stitcher.py
```

2. **Stitch all PDFs in a specific directory:**
```bash
python pdf_stitcher.py -i "C:\path\to\pdfs" -o combined.pdf
```

3. **Stitch specific files:**
```bash
python pdf_stitcher.py -f file1.pdf -f file2.pdf -f file3.pdf -o result.pdf
```

4. **Stitch PDFs with a specific pattern:**
```bash
python pdf_stitcher.py -i "C:\documents" -p "chapter_*.pdf" -o book.pdf
```

5. **Enable verbose output:**
```bash
python pdf_stitcher.py -i "C:\pdfs" -v -o detailed_output.pdf
```

6. **Disable source filename pages (revert to original behavior):**
```bash
python pdf_stitcher.py -i "C:\pdfs" --no_source -o traditional_output.pdf
```

### Command Line Options

- `-i, --input-dir`: Directory containing PDF files to stitch
- `-f, --files`: Specific PDF files to stitch (can be used multiple times)
- `-o, --output`: Output filename for the stitched PDF (default: stitched_document.pdf)
- `-p, --pattern`: File pattern to match in input directory (default: *.pdf)
- `-v, --verbose`: Enable verbose output
- `--no_source`: Disable adding source filename to the PDF content (default: source filenames are included)
- `--help`: Show help message

## How It Works

1. **File Discovery**: The program finds PDF files either from:
   - A specified directory (with optional file pattern matching)
   - Specific files provided via command line
   - Current directory (if no input specified)

2. **Processing**: Each PDF is processed in alphabetical order:
   - Opens and validates each PDF file
   - Skips encrypted or corrupted files with appropriate warnings
   - Adds all pages from valid PDFs to the output document

3. **Output**: Creates a single stitched PDF with:
   - **Source filename pages** showing the origin file for each section (new feature - can be disabled with `--no_source`)
   - All pages from source PDFs in order
   - Progress indication during processing
   - Summary statistics upon completion

## Error Handling

The program handles various error conditions:
- Missing or non-existent files
- Corrupted PDF files
- Encrypted PDF files (skipped with warning)
- File permission issues
- Invalid output paths

## Source Filename Tracking

**NEW FEATURE**: By default, the PDF Stitcher now adds a source page before each PDF's content, showing the original filename. This makes it easy to identify which file each section came from in the final stitched document.

### Example Output
When stitching `document1.pdf` and `document2.pdf`, the result will contain:
1. **Source page**: "Source: document1.pdf"
2. All pages from document1.pdf
3. **Source page**: "Source: document2.pdf"  
4. All pages from document2.pdf

### Controlling Source Pages
- **Default behavior**: Source pages are included automatically
- **Disable source pages**: Use the `--no_source` flag to revert to the original behavior (no source pages)

```bash
# With source pages (default)
python pdf_stitcher.py -f file1.pdf -f file2.pdf -o with_sources.pdf

# Without source pages (original behavior)
python pdf_stitcher.py -f file1.pdf -f file2.pdf -o without_sources.pdf --no_source
```

## Requirements

- Python 3.6+
- pypdf (for PDF manipulation)
- click (for command-line interface)
- reportlab (for creating source filename pages)

## Examples of Common Use Cases

### Merging Invoice PDFs
```bash
python pdf_stitcher.py -i "C:\invoices\2024" -p "invoice_*.pdf" -o "2024_invoices.pdf"
```

### Combining Report Chapters
```bash
python pdf_stitcher.py -f intro.pdf -f chapter1.pdf -f chapter2.pdf -f conclusion.pdf -o complete_report.pdf
```

### Processing Scanned Documents
```bash
python pdf_stitcher.py -i "C:\scanned_docs" -o "combined_documents.pdf" -v
```

## Output

The program provides clear feedback:
- ✅ Successfully processed files
- ⚠️ Warnings for encrypted files
- ❌ Errors for corrupted or inaccessible files
- 📊 Final statistics (files processed, failed, total pages)
