# Import pathlib for working with files and folder paths
import pathlib

# Import PyMuPDF for opening PDF files and extracting text
import pymupdf

# Import re for cleaning and processing extracted text
import re


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

        # Store the page number and extracted text
        pages.append({
            "page": page_number,   # Page Number 
            "text": text      # Text
        })

    # Close the PDF file
    doc.close()             # Close File After Extraction 

    # Return the extracted text
    return pages         

# Temporary testing code to demonstrate the function
pdf_path = "C:\\Users\\yadao\\Downloads\\FTH-Quaterly-Insight-Sep-2025.pdf"  # Demo path for testing

# Open the PDF
doc = pymupdf.open(pdf_path)     # Specifying what to open

# Print the number of pages
print("Number of pages:", doc.page_count)  # Print the number of pages In the PDF
print("Page size:", doc[0].rect)  # Print the size of the first page
print("Page size:", doc[1].rect)  # Print the size of the second page
print("Text of the first page:", doc[0].get_text())  # Print the text of the first page
print("Width of the first page:", doc[0].rect.width)  # Print the width of the first page
print("The author of the PDF:", doc.metadata['author'])  # Print the author of the PDF

# Close the PDF
doc.close()             # Close File After Extraction 