import streamlit as st      # For streamlit web app interface
import tempfile             # For creating temporary files
import os
from backend import answer_question                   # For interacting with the operating system
from dotenv import load_dotenv  # For loading environment variables from a .env file

load_dotenv()

# PAGE CONFIGURATION
st.set_page_config(
    page_title="AI Assistant",
    page_icon="🤖",
    layout="wide"
)
# title of the app
st.title("AI Assistant")
st.write("Upload your research paper and ask questions about it. And ask questions on them.")

# FILE UPLAOD
uploaded_files = st.file_uploader(
    "Upload your research paper", 
    type=[
        "pdf",
        "docx",
        "pptx",
        "txt"
        ], 
    accept_multiple_files=True)

# DISPLAY UPLOADED FILES
if uploaded_files:
    st.success(f"{len(uploaded_files)} file(s) uploaded successfully!")
    for uploaded_file in uploaded_files:
        size_kb = uploaded_file.size / 1024
        st.write( f"📄 **{uploaded_file.name}** "
            f"({size_kb:.1f} KB)")


# CONVERT STREAMLIT UPLOADED FILES TO TEMPORARY FILES
files_path = []
temporary_files = []
try:
    for uploaded_file in uploaded_files:
        suffix = os.path.splitext(
            uploaded_file.name
            )[1].lower()

        temporary_file = tempfile.NamedTemporaryFile(
            delete=False, suffix=suffix)
        
        temporary_file.write(
            uploaded_file.getvalue())
        
        temporary_file.close()

        # Store the path of the temporary file for later use
        files_path.append(
            temporary_file.name)

    st.success("Documents are ready for processing!")

    # QUESTION INPUT
    st.divider()

    st.subheader("Ask a question about your research paper")
    question = st.text_area(
        "Type your question here",
        placeholder= ("Example: What is the main methodology?"
                      "used in these research papers?"
    ),
    height=100)

    # ASK BUTTON 
    if st.button(
        "Ask AI",
        type = "primary",
        use_container_width=True):
        if not question.strip():
            st.warning("Please enter a question.")
        else:
            with st.spinner("Processing your documents and generating an answer..."):
                answer = answer_question(
                    question.strip(),
                    files_path
                )

        # DISPLAY ANSWER
        st.divider()
        st.subheader("Answer from AI")
        st.write(answer)

except Exception as e:
    st.error(f"An error occurred while processing the files : {str(e)}")
finally:
    # CLEAN UP TEMPORARY FILES
    for file_path in temporary_files:
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
        except Exception :
            pass  # Ignore errors during cleanup