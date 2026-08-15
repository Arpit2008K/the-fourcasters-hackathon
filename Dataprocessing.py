# Import PyMuPDF for opening PDF files and extracting text
import pymupdf

# Import re for cleaning and processing extracted text
import re

# Import Path for working with file paths
from pathlib import Path


# Function to clean extracted text
def clean_text(text):

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)         # Replace multiple spaces and tabs with a single space

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)   # Replace multiple blank lines with a single blank line

    # Fix spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)   # Remove spaces before punctuation marks

    # Remove spaces from the beginning and end
    return text.strip()                         # Remove leading and trailing spaces from the text


# Function to extract text from a PDF file
def extract_text_from_the_pdf(pdf_path):                # Function to extract text from a PDF file

    # Open the PDF file
    doc = pymupdf.open(pdf_path)                   # Open the PDF file using PyMuPDF

    # Create an empty list to store text from each page
    pages = []

    # Loop through every page in the PDF
    for page_number, page in enumerate(doc, start=1):   # Enumerate through each page in the PDF starting from page 1

        # Extract text from the current page
        text = page.get_text()                         # Extract text from the current page using PyMuPDF's get_text() method

        # Clean the extracted text
        text = clean_text(text)                        # Clean the extracted text using the clean_text function

        # Store the page number and extracted text
        pages.append({
            "page": page_number,   # Page Number
            "text": text            # Text
        })

    # Close the PDF file
    doc.close()             # Close File After Extraction

    # Return the extracted text
    return pages


# Function to create chunks of text
def create_chunks(text, chunk_size=1000, overlap=200):   # Function to create chunks of text with specified size and overlap

    words = text.split()   # Split the text into individual words

    chunks = []             # Empty list to store the chunks of text

    start = 0               # Initialize the starting index for chunking

    while start < len(words):   # Loop until all words are processed

        end = start + chunk_size   # Calculate the ending index for the current chunk

        chunk = " ".join(words[start:end])   # Join the words from the starting index to the ending index to form a chunk of text

        chunks.append(chunk)   # Add the current chunk to the list of chunks

        start += chunk_size - overlap   # Move the starting index forward by the chunk size minus the overlap to maintain context

    return chunks


# Function to process the complete PDF
def process_pdf(pdf_path):       # Function to process a PDF

    # Extract text from the PDF
    pages = extract_text_from_the_pdf(pdf_path)

    # Create an empty list to store processed chunks
    processed_chunks = []

    # Loop through every page
    for page in pages:

        # Get the cleaned text from the current page
        cleaned = page["text"]

        # Skip the page if no text is available
        if not cleaned:
            continue

        # Create chunks from the cleaned text
        chunks = create_chunks(cleaned)

        # Loop through every chunk
        for chunk_number, chunk in enumerate(chunks, start=1):

            # Store the source, page number, chunk number, and text
            processed_chunks.append({
                "source": Path(pdf_path).name,   # PDF file name
                "page": page["page"],             # Page Number
                "chunk": chunk_number,           # Chunk Number
                "text": chunk                     # Chunk Text
            })

    # Return all processed chunks
    return processed_chunks


# Temporary File Path
pdf_path = "C:\\Users\\yadao\\Downloads\\FTH-Quaterly-Insight-Sep-2025.pdf"   # Temporary File Path


# Process the complete PDF
processed_chunks = process_pdf(pdf_path)   # Process the PDF using the complete processing pipeline


# Print the number of processed chunks
print("Number of processed chunks:", len(processed_chunks))   # This prints the number of processed chunks


# Print the first processed chunk
print("\nFirst processed chunk:")   # Print the first processed chunk

print(processed_chunks[0])   # Display the first processed chunk


# Print the second processed chunk
print("\nSecond processed chunk:")   # Print the second processed chunk

print(processed_chunks[1])   # Display the second processed chunk

# Test the PDF processing function temporarily with a specific PDF file path

pdf_file = "C:\\Users\\yadao\\Downloads\\FTH-Quaterly-Insight-Sep-2025.pdf"      

chunks = process_pdf(pdf_file)        # Process the PDF file and create chunks of text

print("Total chunks:", len(chunks))   # Print the total number of chunks created from the PDF

for item in chunks[:3]:
    print("\n------------------------")      
    print("Source:", item["source"])             # Print the source of the chunk
    print("Page:", item["page"])                # Print the page number
    print("Chunk:", item["chunk"])              # Print the chunk number
    print(item["text"][:500])                   # Print the first 500 characters of the chunk



    #-------------------------------------------------------PDF PROCESSING OVER ------------------------------------------------------------------#

    