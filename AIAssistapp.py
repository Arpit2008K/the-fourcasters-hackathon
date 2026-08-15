"""
AI Research Assistant - Streamlit Frontend
Upload research papers, search across them by semantic similarity, generate
concise summaries, ask grounded questions, and compare multiple documents.
"""

import os
import tempfile
import streamlit as st

from Dataprocessing import process_file
from backend import embed_chunks, semantic_retrieve, get_answer, summarize_document

# ------------------------------------------------------------- PAGE CONFIG -------------------------------------------------------------

st.set_page_config(
    page_title="AI Research Assistant",
    page_icon="📚",
    layout="wide",
)

st.title("📚 AI Research Assistant")
st.caption("Upload PDF, DOCX, TXT, or PPTX files. Ask grounded questions, get summaries, and compare papers.")

# ------------------------------------------------------------- SESSION STATE -------------------------------------------------------------

if "processed_chunks" not in st.session_state:
    st.session_state.processed_chunks = []          # all chunks (with embeddings) from all uploaded files

if "processed_file_names" not in st.session_state:
    st.session_state.processed_file_names = set()     # names already processed, avoid reprocessing

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []                 # list of (question, answer)

if "summaries" not in st.session_state:
    st.session_state.summaries = {}                     # source_name -> summary text

# ------------------------------------------------------------- SIDEBAR: UPLOAD -------------------------------------------------------------

with st.sidebar:
    st.header("Upload Documents")

    uploaded_files = st.file_uploader(
        "Choose research files",
        type=["pdf", "docx", "txt", "pptx"],
        accept_multiple_files=True,
    )

    process_clicked = st.button("Process Documents", type="primary")

    if process_clicked and uploaded_files:
        new_files = [f for f in uploaded_files if f.name not in st.session_state.processed_file_names]

        if not new_files:
            st.info("All uploaded files have already been processed.")
        else:
            with st.spinner(f"Extracting text and computing embeddings for {len(new_files)} file(s)..."):
                for uploaded_file in new_files:
                    suffix = os.path.splitext(uploaded_file.name)[1]
                    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                        tmp.write(uploaded_file.getbuffer())
                        tmp_path = tmp.name

                    try:
                        chunks = process_file(tmp_path)
                        for chunk in chunks:
                            chunk["source"] = uploaded_file.name  # restore original filename
                        embed_chunks(chunks)  # semantic similarity search relies on this
                        st.session_state.processed_chunks.extend(chunks)
                        st.session_state.processed_file_names.add(uploaded_file.name)
                    except Exception as e:
                        st.error(f"Failed to process {uploaded_file.name}: {e}")
                    finally:
                        os.remove(tmp_path)

            st.success(f"Processed {len(new_files)} file(s) successfully.")

    if st.session_state.processed_file_names:
        st.subheader("Loaded Documents")
        for name in sorted(st.session_state.processed_file_names):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.write(f"📄 {name}")
            with col2:
                if st.button("Summarize", key=f"summarize_{name}"):
                    with st.spinner("Generating summary..."):
                        st.session_state.summaries[name] = summarize_document(
                            name, st.session_state.processed_chunks
                        )

        if st.button("Clear All Documents"):
            st.session_state.processed_chunks = []
            st.session_state.processed_file_names = set()
            st.session_state.chat_history = []
            st.session_state.summaries = {}
            st.rerun()

# ------------------------------------------------------------- MAIN: SUMMARIES -------------------------------------------------------------

if st.session_state.summaries:
    st.subheader("📝 Document Summaries")
    for name, summary in st.session_state.summaries.items():
        with st.expander(name, expanded=False):
            st.markdown(summary)
    st.divider()

# ------------------------------------------------------------- MAIN: CHAT -------------------------------------------------------------

if not st.session_state.processed_file_names:
    st.info("Upload and process at least one document from the sidebar to get started.")
else:
    for question, answer in st.session_state.chat_history:
        with st.chat_message("user"):
            st.markdown(question)
        with st.chat_message("assistant"):
            st.markdown(answer)

    question = st.chat_input("Ask a question about your documents...")

    if question:
        with st.chat_message("user"):
            st.markdown(question)

        with st.chat_message("assistant"):
            with st.spinner("Searching documents by semantic similarity and generating answer..."):
                retrieved_chunks = semantic_retrieve(question, st.session_state.processed_chunks)

                if not retrieved_chunks:
                    answer = "I could not find relevant information in the uploaded documents to answer this question."
                else:
                    answer = get_answer(question, retrieved_chunks)

            st.markdown(answer)

            if retrieved_chunks:
                with st.expander("Sources used"):
                    for chunk in retrieved_chunks:
                        location = ""
                        if "page" in chunk:
                            location = f" (Page {chunk['page']})"
                        elif "paragraph" in chunk:
                            location = f" (Paragraph {chunk['paragraph']})"
                        elif "slide" in chunk:
                            location = f" (Slide {chunk['slide']})"
                        st.write(f"- {chunk['source']}{location}")

        st.session_state.chat_history.append((question, answer))