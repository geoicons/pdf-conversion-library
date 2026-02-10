# pdf-conversion-library

A collection of Python tools for conversion and transformation of PDF data.

## Contents

| Script | Purpose |
|--------|---------|
| **CombinePDFs.py** | Merge multiple PDFs into one |
| **OCR_PDFs.py** | Extract text from PDFs via OCR (Tesseract) |
| **PDF_To_Base64.py** | Encode a PDF as a base64 string payload |

## Requirements

- **Python 3**
- Script-specific dependencies (see each section below). **PDF_To_Base64.py** uses only the standard library.

---

## CombinePDFs.py

Merges multiple PDF files into a single PDF in order.

1. Edit the `pdf_files` list and `output_filename` at the top of the script.
2. Run the script.

**Dependencies:** PyPDF2

```bash
pip install PyPDF2
python CombinePDFs.py
```

---

## OCR_PDFs.py

Extracts text from a PDF using OCR. Renders each page to an image with PyMuPDF, then runs Tesseract. No Poppler required.

1. Edit `pdf_file` (and optionally `tesseract_cmd`) in the `if __name__ == "__main__"` block.
2. Run the script.

**Dependencies:** PyMuPDF (fitz), pytesseract, Pillow. **Tesseract OCR** must be installed on your system ([Windows](https://github.com/UB-Mannheim/tesseract/wiki)).

```bash
pip install PyMuPDF pytesseract Pillow
python OCR_PDFs.py
```

- Output is saved as `<pdf_name>_OCR.txt`.
- Optional parameters: `output_txt_path`, `dpi` (default 300), `tesseract_cmd`.

---

## PDF_To_Base64.py

Converts a PDF file to a base64-encoded string payload (e.g. for APIs or embedding). No extra dependencies.

```bash
python PDF_To_Base64.py <path_to_pdf>
```

**Example:**

```bash
python PDF_To_Base64.py document.pdf
```

Prints the base64 payload to stdout. As a module: `from PDF_To_Base64 import pdf_to_base64_payload` then `pdf_to_base64_payload(pdf_path)`.
