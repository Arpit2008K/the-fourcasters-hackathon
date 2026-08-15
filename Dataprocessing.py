# Import PyMuPDF for opening PDF files and extracting text
import pymupdf

# Import re for cleaning and processing extracted text
import re


# Function to clean extracted text
def clean_text(text):

    # Remove excessive spaces
    text = re.sub(r"[ \t]+", " ", text)         # Replace multiple spaces and tabs with a single space

    # Remove excessive blank lines
    text = re.sub(r"\n\s*\n+", "\n\n", text)           # Replace multiple blank lines with a single blank line

    # Fix spaces before punctuation
    text = re.sub(r"\s+([,.!?;:])", r"\1", text)              # Remove spaces before punctuation marks
 
    # Remove spaces from the beginning and end
    return text.strip()                         # Remove leading and trailing spaces from the text


# Function to extract text from a PDF file
def extract_text_from_the_pdf(pdf_path):                #function to extract text from a PDF file

    # Open the PDF file
    doc = pymupdf.open(pdf_path)                   # Open the PDF file using PyMuPDF

    # Create an empty list to store text from each page
    pages = []                                


    # Loop through every page in the PDF
    for page_number, page in enumerate(doc, start=1):             # Enumerate through each page in the PDF starting from page 1

        # Extract text from the current page
        text = page.get_text()                               # Extract text from the current page using PyMuPDF's get_text() method

        # Clean the extracted text
        text = clean_text(text)                         # Clean the extracted text using the clean_text function

        # Store the page number and extracted text
        pages.append({
            "page": page_number,   # Page Number
            "text": text            # Text
        })

    # Close the PDF file
    doc.close()             # Close File After Extraction

    # Return the extracted text
    return pages

def create_chunks(text, chunk_size=1000, overlap=200):            # Function to create chunks of text with specified size and overlap
    words = text.split()                                          # Overlap Means that the last 200 words of the previous chunk will be included in the next chunk to maintain context      

    chunks = []               # Empty list to store the chunks of text

    start = 0          # Initialize the starting index for chunking

    while start < len(words):           # Loop until all words are processed
        end = start + chunk_size     # Calculate the ending index for the current chunk

        chunk = " ".join(words[start:end])             # Join the words from the starting index to the ending index to form a chunk of text

        chunks.append(chunk)            # Add the current chunk to the list of chunks

        start += chunk_size - overlap                  # Move the starting index forward by the chunk size minus the overlap to create the next chunk

    return chunks                     

# Extract text from the PDF

pdf_path = "C:\\Users\\yadao\\Downloads\\FTH-Quaterly-Insight-Sep-2025.pdf"       # Temporary File Path  
pages = extract_text_from_the_pdf(pdf_path)      # Path

# Combine all page text
total_text = ""           # Combine all page text Add store it in empty string variable

for page in pages:
    total_text += page["text"] + "\n"             # Loop through pages and add each page's text with a new line

# Create chunks
chunks = create_chunks(total_text)       # Create chunks from the combined text

# Print number of chunks
print("Number of chunks:", len(chunks))          # This prints the number of chunks Created from the text

# Print the first chunk
print("\nFirst chunk:")               # 1st chunk and then    
print(chunks[0])

# Print the second chunk            #2nd chunk index 1
print("\nSecond chunk:")
print(chunks[1])