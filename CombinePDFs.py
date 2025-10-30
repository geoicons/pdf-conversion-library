import PyPDF2
import os

def combine_pdfs():
    """
    Combine two PDF files into one:
    """
    
    # Define the input PDF files
    pdf_files = [
        "File1.pdf",
        "File2.pdf"
    ]
    
    # Output filename
    output_filename = "Combined_Files.pdf"
    
    # Check if all input files exist
    missing_files = []
    for pdf_file in pdf_files:
        if not os.path.exists(pdf_file):
            missing_files.append(pdf_file)
    
    if missing_files:
        print(f"Error: The following files are missing:")
        for file in missing_files:
            print(f"  - {file}")
        return
    
    # Create a PDF merger object
    pdf_merger = PyPDF2.PdfMerger()
    
    try:
        # Add each PDF to the merger
        for pdf_file in pdf_files:
            print(f"Adding {pdf_file}...")
            pdf_merger.append(pdf_file)
        
        # Write the combined PDF to output file
        with open(output_filename, 'wb') as output_file:
            pdf_merger.write(output_file)
        
        print(f"\nSuccessfully combined PDFs into: {output_filename}")
        
        # Get file sizes for confirmation
        total_size = 0
        for pdf_file in pdf_files:
            size = os.path.getsize(pdf_file)
            total_size += size
            print(f"  {pdf_file}: {size:,} bytes")
        
        output_size = os.path.getsize(output_filename)
        print(f"  {output_filename}: {output_size:,} bytes")
        
    except Exception as e:
        print(f"Error combining PDFs: {str(e)}")
    
    finally:
        # Close the merger
        pdf_merger.close()

if __name__ == "__main__":
    print("PDF Combiner Script")
    print("==================")
    print("Combining the following PDFs:")
    print("1. File1.pdf")
    print("2. File2.pdf")
    print()
    
    combine_pdfs()
