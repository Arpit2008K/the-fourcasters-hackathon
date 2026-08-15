# Import PyMuPDF for opening PDF files and extracting text
import pymupdf

# Import re for cleaning and processing extracted text
import re


# Function to clean extracted text
def clean_text(text):

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)

    # Fix spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)

    # Remove spaces from the beginning and end
    return text.strip()


# Function to extract text from a PDF file
def extract_text_from_the_pdf(pdf_path):

    # Open the PDF file
    doc = pymupdf.open(pdf_path)

    # Create an empty list to store text from each page
    pages = []


    # Loop through every page in the PDF
    for page_number, page in enumerate(doc, start=1):

        # Extract text from the current page
        text = page.get_text()

        # Clean the extracted text
        text = clean_text(text)

        # Store the page number and extracted text
        pages.append({
            "page": page_number,   # Page Number
            "text": text            # Text
        })

    # Close the PDF file
    doc.close()             # Close File After Extraction

    # Return the extracted text
    return pages

