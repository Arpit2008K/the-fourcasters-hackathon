import streamlit as st
import pymupdf
from docx import Document
from pptx import Presentation
import pandas as pd
import easyocr
import io


# TEXT EXTRACTION FUNCTION

def extract_text(uploaded_file):

    file_name = uploaded_file.name
    extension = file_name.split(".")[-1].lower()

    if extension == "pdf":
        # PDF extraction
        pass

    elif extension == "docx":
        # DOCX extraction
        pass

    elif extension == "pptx":
        # PPTX extraction
        pass

    elif extension == "txt":
        # TXT extraction
        pass

    elif extension in ["png", "jpg", "jpeg"]:
        # Image OCR
        pass

    return ""


# STREAMLIT UI 
st.set_page_config(
    page_title="AI Research Assistant", 
    page_icon="📚", 
    layout="wide")
st.title("AI Research Assistant")

uploaded_files = st.file_uploader(
    "Upload your research files",
    type=[
        "pdf",
        "docx",
        "pptx",
        "txt",
        "csv",
        "xlsx",
        "png",
        "jpg",
        "jpeg"
    ],
    accept_multiple_files=True
)

if uploaded_files:

    for uploaded_file in uploaded_files:

        st.subheader(f"📄 {uploaded_file.name}")

        text = extract_text(uploaded_file)

        st.text_area(
            "Extracted Text",
            text,
            height=300,
            key=uploaded_file.name
        )