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


# Temporary testing code to demonstrate the function
pdf_path = "C:\\Users\\yadao\\Downloads\\FTH-Quaterly-Insight-Sep-2025.pdf"  # Demo path for testing

# Open the PDF
doc = pymupdf.open(pdf_path)     # Specifying what to open

# Print the number of pages
print("Number of pages:", doc.page_count)  # Print the number of pages in the PDF

# Print the size of the first page
print("Page size:", doc[0].rect)

# Print the size of the second page
print("Page size:", doc[1].rect)

# Print the text of the first page
print("Text of the first page:", doc[0].get_text())

# Print the width of the first page
print("Width of the first page:", doc[0].rect.width)

# Print the author of the PDF
print("The author of the PDF:", doc.metadata["author"])

# Close the PDF
doc.close()             # Close File After Testing


# Extract text from the entire PDF
pages = extract_text_from_the_pdf(pdf_path)

# Create an empty string to store total text
total_text = ""

# Loop through every page
for page in pages:

    # Add the text of each page
    total_text += page["text"] + "\n"


# Print the total cleaned text
print("Total Text in the PDF:")
print(total_text)