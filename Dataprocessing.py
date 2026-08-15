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

    