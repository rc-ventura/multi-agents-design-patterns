import re
import os

def pdf_parser(file_path: str) -> str:
    """
    Parses a PDF file and extracts its text content.
    
    Args:
        file_path: Path to the PDF file.
        
    Returns:
        The extracted text from the PDF.
    """
    # Simple mock implementation for demonstration
    # In a real scenario, you would use libraries like pypdf or PyMuPDF
    # Example:
    # import pypdf
    # reader = pypdf.PdfReader(file_path)
    # text = ""
    # for page in reader.pages:
    #     text += page.extract_text() + "\n"
    # return text
    
    if not os.path.exists(file_path):
        return f"Error: File {file_path} not found."
    
    # Returning mock text for the "simple" request so it runs without extra deps immediately
    return f"Mock content extracted from {file_path}:\nInvoice #12345\nDate: 2023-10-27\nTotal: $500.00\nItems: Service A, Service B"

def regex_extractor(text: str) -> dict:
    """
    Extracts structured data (Invoice No, Date, Total) from text using Regex.
    
    Args:
        text: The raw text to extract data from.
        
    Returns:
        A dictionary containing the extracted fields.
    """
    invoice_pattern = r"Invoice #(\d+)"
    date_pattern = r"Date: (\d{4}-\d{2}-\d{2})"
    total_pattern = r"Total: \$(\d+\.\d{2})"
    
    invoice_match = re.search(invoice_pattern, text)
    date_match = re.search(date_pattern, text)
    total_match = re.search(total_pattern, text)
    
    return {
        "invoice_number": invoice_match.group(1) if invoice_match else None,
        "date": date_match.group(1) if date_match else None,
        "total": total_match.group(1) if total_match else None
    }

def summary_engine(structured_data: dict) -> str:
    """
    Generates a human-readable summary from structured data.
    
    Args:
        structured_data: The dictionary of extracted data.
        
    Returns:
        A summary string.
    """
    
    if not isinstance(structured_data, dict):
        return "Error: Invalid input data for summary."
        
    invoice = structured_data.get("invoice_number", "Unknown")
    date = structured_data.get("date", "Unknown")
    total = structured_data.get("total", "0.00")
    
    return f"Summary: Invoice {invoice} was issued on {date} with a total amount of ${total}."
