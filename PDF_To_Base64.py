"""
Convert a PDF file to a base64-encoded payload (PDF contents as a single string).
"""

import base64
import os
import sys


def pdf_to_base64_payload(pdf_path: str) -> str:
    """
    Read a PDF file and return its contents as a base64-encoded string payload.

    Args:
        pdf_path: Path to the PDF file.

    Returns:
        Base64-encoded string of the PDF binary content.

    Raises:
        FileNotFoundError: If the PDF file does not exist.
    """
    if not os.path.exists(pdf_path):
        raise FileNotFoundError(f"PDF file not found: {pdf_path}")

    with open(pdf_path, "rb") as f:
        pdf_bytes = f.read()

    return base64.b64encode(pdf_bytes).decode("ascii")


def main():
    if len(sys.argv) < 2:
        print("Usage: python PDF_To_Base64.py <path_to_pdf>")
        print("Example: python PDF_To_Base64.py document.pdf")
        sys.exit(1)

    pdf_path = sys.argv[1]
    try:
        payload = pdf_to_base64_payload(pdf_path)
        print(payload)
    except FileNotFoundError as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
