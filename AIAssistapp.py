import streamlit as st
import pymupdf

st.title("AI Research Assistant")

uploaded_files = st.file_uploader(
    "Upload research papers",
    type=["pdf"],
    accept_multiple_files=True
)

if uploaded_files:

    st.success(f"{len(uploaded_files)} paper(s) uploaded successfully!")

    for uploaded_file in uploaded_files:

        st.subheader(f"📄 {uploaded_file.name}")

        doc = pymupdf.open(
            stream=uploaded_file.read(),
            filetype="pdf"
        )

        full_text = ""

        for page in doc:
            full_text += page.get_text()

        st.write("Number of pages:", len(doc))

        with st.expander("View extracted text"):
            st.text_area(
                "Paper Content",
                full_text,
                height=300,
                key=uploaded_file.name
            )