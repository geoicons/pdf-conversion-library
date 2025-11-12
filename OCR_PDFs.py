import pytesseract
import fitz  # PyMuPDF
from PIL import Image
import io
import os
import platform

def find_tesseract_path():
    """
    Try to find Tesseract installation path on Windows.
    Returns the path to tesseract.exe if found, None otherwise.
    """
    if platform.system() != "Windows":
        return None
    
    # Common installation paths for Tesseract on Windows
    possible_paths = [
        r"C:\Program Files\Tesseract-OCR\tesseract.exe",
        r"C:\Program Files (x86)\Tesseract-OCR\tesseract.exe",
        r"C:\Tesseract-OCR\tesseract.exe",
        os.path.join(os.path.expanduser("~"), "AppData", "Local", "Tesseract-OCR", "tesseract.exe"),
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return path
    
    return None

def ocr_pdf(pdf_path, output_txt_path=None, dpi=300, tesseract_cmd=None):
    """
    Extract text from a PDF file using OCR.
    Uses PyMuPDF (fitz) to convert PDF pages to images - no Poppler required!
    
    Args:
        pdf_path (str): Path to the input PDF file
        output_txt_path (str, optional): Path to save the extracted text.
                                        If None, saves as <pdf_name>_OCR.txt
        dpi (int): Resolution for rendering PDF pages (default: 300)
                  Higher DPI = better quality but slower processing
        tesseract_cmd (str, optional): Path to tesseract.exe.
                                      If None, will try to auto-detect on Windows.
    """
    
    # Check if PDF file exists
    if not os.path.exists(pdf_path):
        print(f"Error: The file '{pdf_path}' does not exist.")
        return
    
    # Set output text file path
    if output_txt_path is None:
        base_name = os.path.splitext(pdf_path)[0]
        output_txt_path = f"{base_name}_OCR.txt"
    
    # Try to find Tesseract path if not provided
    if tesseract_cmd is None:
        tesseract_cmd = find_tesseract_path()
        if tesseract_cmd:
            pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
            print(f"Found Tesseract at: {tesseract_cmd}")
        else:
            print("Warning: Tesseract not found in common locations.")
            print("If you get an error, set tesseract_cmd parameter or add Tesseract to PATH.")
    else:
        pytesseract.pytesseract.tesseract_cmd = tesseract_cmd
    
    print(f"Processing PDF: {pdf_path}")
    print(f"Output will be saved to: {output_txt_path}")
    print(f"Rendering at {dpi} DPI")
    print()
    
    try:
        # Open PDF with PyMuPDF
        print("Opening PDF file...")
        pdf_document = fitz.open(pdf_path)
        num_pages = len(pdf_document)
        print(f"Found {num_pages} page(s)")
        print()
        
        # Extract text from each page using OCR
        all_text = []
        for page_num in range(num_pages):
            print(f"Processing page {page_num + 1}/{num_pages}...")
            
            # Get the page
            page = pdf_document[page_num]
            
            # Render page to an image (pixmap)
            # Matrix controls the zoom/scale (dpi/72 gives us the desired DPI)
            zoom = dpi / 72.0
            mat = fitz.Matrix(zoom, zoom)
            pix = page.get_pixmap(matrix=mat)
            
            # Convert pixmap to PIL Image
            img_data = pix.tobytes("png")
            image = Image.open(io.BytesIO(img_data))
            
            # Perform OCR on the image
            text = pytesseract.image_to_string(image)
            all_text.append(f"--- Page {page_num + 1} ---\n{text}\n")
        
        # Close the PDF document
        pdf_document.close()
        
        # Combine all text
        full_text = "\n".join(all_text)
        
        # Save to text file
        with open(output_txt_path, 'w', encoding='utf-8') as f:
            f.write(full_text)
        
        print(f"\nSuccessfully extracted text from PDF!")
        print(f"Text saved to: {output_txt_path}")
        print(f"Total characters extracted: {len(full_text):,}")
        
        # Display first 500 characters as preview
        preview = full_text[:500].replace('\n', ' ')
        print(f"\nPreview (first 500 characters):")
        print(f"{preview}...")
        
    except ImportError as e:
        print(f"Error: Missing required library - {str(e)}")
        print("\nPlease install the required packages:")
        print("  pip install PyMuPDF pytesseract Pillow")
        print("\nAlso make sure Tesseract OCR is installed on your system:")
        print("  Windows: https://github.com/UB-Mannheim/tesseract/wiki")
    except Exception as e:
        error_msg = str(e).lower()
        print(f"Error processing PDF: {str(e)}")
        print()
        
        if "tesseract" in error_msg or "path" in error_msg:
            print("=" * 60)
            print("TESSERACT NOT FOUND")
            print("=" * 60)
            print("\nTesseract OCR is required to extract text from images.")
            print("\nTo install Tesseract on Windows:")
            print("  1. Download from: https://github.com/UB-Mannheim/tesseract/wiki")
            print("  2. Run the installer")
            print("  3. Add Tesseract to your system PATH, OR")
            print("  4. Update this script to specify the tesseract_cmd parameter")
            print("\nExample: ocr_pdf(pdf_file, tesseract_cmd=r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe')")
            print("\nAlternatively, you can set the tesseract_cmd in the main section below.")
        else:
            print("\nNote: Make sure you have:")
            print("  1. Tesseract OCR installed on your system")
            print("  2. PyMuPDF (pip install PyMuPDF)")
            print("  3. pytesseract (pip install pytesseract)")
            print("  4. Pillow (pip install Pillow)")


if __name__ == "__main__":
    print("PDF OCR Text Extraction Script")
    print("==============================")
    print("(No Poppler required - uses PyMuPDF)")
    print()
    
    # Process the specified PDF file
    pdf_file = "Memorandum.pdf"
    
    # If Tesseract is not in PATH, uncomment and set the path below:
    # tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"  # Update this to your Tesseract installation path
    tesseract_cmd = None  # Set to None to auto-detect, or specify path if needed
    
    # You can adjust DPI for quality/speed tradeoff
    # Higher DPI = better OCR accuracy but slower (default: 300)
    ocr_pdf(pdf_file, dpi=300, tesseract_cmd=tesseract_cmd)
