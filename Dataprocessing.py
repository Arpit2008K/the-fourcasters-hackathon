# Import PyMuPDF for opening PDF files and extracting text
import pymupdf

# Import re for cleaning and processing extracted text
import re

# Import Path for working with file paths
from pathlib import Path

# Import python-docx for opening DOCX files and extracting text
from docx import Document


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


# Function to extract text from a DOCX file
def extract_text_from_docx(file_path):                # Function to extract text from a DOCX file

    # Open the DOCX file
    doc = Document(file_path)                         # Open the DOCX file using python-docx

    # Create an empty list to store text from each paragraph
    paragraphs = []

    # Loop through every paragraph in the DOCX file
    for paragraph_number, paragraph in enumerate(doc.paragraphs, start=1):   # Enumerate through each paragraph starting from paragraph 1

        # Extract text from the current paragraph
        text = paragraph.text                         # Extract text from the current paragraph

        # Clean the extracted text
        text = clean_text(text)                       # Clean the extracted text using the clean_text function

        # Skip empty paragraphs
        if not text:
            continue

        # Store the paragraph number and extracted text
        paragraphs.append({
            "paragraph": paragraph_number,   # Paragraph Number
            "text": text                     # Text
        })

    # Return the extracted paragraphs
    return paragraphs


# Function to extract text from a TXT file
def extract_text_from_txt(file_path):                # Function to extract text from a TXT file

    # Open the TXT file
    with open(file_path, "r", encoding="utf-8", errors="ignore") as txt_file:   # Open the TXT file and ignore encoding issues

        # Read the text from the TXT file
        text = txt_file.read()                        # Read all the text from the TXT file

    # Clean the extracted text
    text = clean_text(text)                           # Clean the extracted text using the clean_text function

    # Create an empty list to store text paragraphs
    paragraphs = []

    # Loop through every paragraph in the text
    for paragraph_number, paragraph in enumerate(re.split(r"\n\s*\n+", text), start=1):   # Split the text by blank lines

        # Clean the paragraph text
        paragraph = clean_text(paragraph)              # Clean the paragraph text

        # Skip the paragraph if no text is available
        if not paragraph:
            continue

        # Store the paragraph number and extracted text
        paragraphs.append({
            "paragraph": paragraph_number,   # Paragraph Number
            "text": paragraph                # Paragraph Text
        })

    # Return the extracted paragraphs
    return paragraphs


# Function to create chunks of text
def create_chunks(text, chunk_size=1000, overlap=200):   # Function to create chunks of text with specified size and overlap

    # Split the text into individual words
    words = text.split()   # Split the text into a list of individual words

    # Create an empty list to store the chunks of text
    chunks = []             # Empty list to store the chunks of text

    # Initialize the starting index for chunking
    start = 0               # Initialize the starting index for chunking

    # Loop until all words are processed
    while start < len(words):   # Loop until all words are processed

        # Calculate the ending index for the current chunk
        end = start + chunk_size   # Calculate the ending index for the current chunk

        # Join the words from the starting index to the ending index
        chunk = " ".join(words[start:end])   # Join the selected words to form a chunk of text

        # Add the current chunk to the list of chunks
        chunks.append(chunk)   # Add the current chunk to the list of chunks

        # Move the starting index forward while maintaining overlap
        start += chunk_size - overlap   # Move forward by the chunk size minus the overlap to maintain context

    # Return the created chunks
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
                "chunk": chunk_number,            # Chunk Number
                "text": chunk                     # Chunk Text
            })

    # Return all processed chunks
    return processed_chunks


# Function to process the complete DOCX file
def process_docx(file_path):       # Function to process a DOCX file

    # Extract text from the DOCX file
    paragraphs = extract_text_from_docx(file_path)

    # Create an empty list to store processed chunks
    processed_chunks = []

    # Loop through every paragraph
    for paragraph in paragraphs:

        # Get the cleaned text from the current paragraph
        cleaned = paragraph["text"]

        # Skip the paragraph if no text is available
        if not cleaned:
            continue

        # Create chunks from the cleaned text
        chunks = create_chunks(cleaned)

        # Loop through every chunk
        for chunk_number, chunk in enumerate(chunks, start=1):

            # Store the source, paragraph number, chunk number, and text
            processed_chunks.append({
                "source": Path(file_path).name,       # DOCX file name
                "paragraph": paragraph["paragraph"],  # Paragraph Number
                "chunk": chunk_number,                # Chunk Number
                "text": chunk                         # Chunk Text
            })

    # Return all processed chunks
    return processed_chunks


# Function to process the complete TXT file
def process_txt(file_path):       # Function to process a TXT file

    # Extract text from the TXT file
    paragraphs = extract_text_from_txt(file_path)

    # Create an empty list to store processed chunks
    processed_chunks = []

    # Loop through every paragraph
    for paragraph in paragraphs:

        # Get the cleaned text from the current paragraph
        cleaned = paragraph["text"]

        # Skip the paragraph if no text is available
        if not cleaned:
            continue

        # Create chunks from the cleaned text
        chunks = create_chunks(cleaned)

        # Loop through every chunk
        for chunk_number, chunk in enumerate(chunks, start=1):

            # Store the source, paragraph number, chunk number, and text
            processed_chunks.append({
                "source": Path(file_path).name,       # TXT file name
                "paragraph": paragraph["paragraph"],  # Paragraph Number
                "chunk": chunk_number,                # Chunk Number
                "text": chunk                         # Chunk Text
            })

    # Return all processed chunks
    return processed_chunks


# Function to process different file formats
def process_file(file_path):       # Function to process a file according to its format

    # Get the file extension
    file_extension = Path(file_path).suffix.lower()   # Get the file extension and convert it to lowercase

    # Check if the file is a PDF
    if file_extension == ".pdf":

        # Process the PDF file
        return process_pdf(file_path)   # Send the PDF file to the PDF processing function

    # Check if the file is a DOCX file
    elif file_extension == ".docx":

        # Process the DOCX file
        return process_docx(file_path)   # Send the DOCX file to the DOCX processing function

    # Check if the file is a TXT file
    elif file_extension == ".txt":

        # Process the TXT file
        return process_txt(file_path)   # Send the TXT file to the TXT processing function

    # If the file format is not supported
    else:

        # Display an error message
        raise ValueError("Unsupported file format. Only PDF, DOCX, and TXT files are supported.")


# Temporary File Path
file_path = "C:\\Users\\yadao\\Downloads\\29_vedant.docx"   # Temporary File Path


# Process the file automatically according to its format
processed_chunks = process_file(file_path)   # Automatically select the correct processing function


# Print the number of processed chunks
print("Number of processed chunks:", len(processed_chunks))   # This prints the number of processed chunks


# Check if processed chunks are available
if processed_chunks:

    # Print the first processed chunk
    print("\nFirst processed chunk:")   # Print the first processed chunk

    print(processed_chunks[0])   # Display the first processed chunk

    # Print the second processed chunk if available
    if len(processed_chunks) > 1:

        print("\nSecond processed chunk:")   # Print the second processed chunk

        print(processed_chunks[1])   # Display the second processed chunk

    # Print the first three processed chunks
    print("\nFirst three processed chunks:")

    for item in processed_chunks[:3]:

        print("\n------------------------")

        print("Source:", item["source"])   # Print the source of the chunk

        # Check whether the chunk belongs to a PDF
        if "page" in item:

            print("Page:", item["page"])   # Print the page number

        # Check whether the chunk belongs to a DOCX or TXT file
        if "paragraph" in item:

            print("Paragraph:", item["paragraph"])   # Print the paragraph number

        print("Chunk:", item["chunk"])   # Print the chunk number

        print(item["text"][:500])   # Print the first 500 characters of the chunk