import streamlit as st
from src.functions import read_resume

def UI_resume_input():

    # Select input method: Copy and paste text or upload a file
    resume_method = st.sidebar.radio("""Resume input (レジュメ入力)""", ("File", "Text"), horizontal = True)

    # Input: Text
    if resume_method == "Text":
        resume_text = st.sidebar.text_area("Text Input (テキスト入力)", height=200)
        return resume_text

    # Input: File Upload
    elif resume_method == "File":
        resume_file = st.sidebar.file_uploader("File Upload (アップロード)", type=["pdf", "docx", "txt"])
        if resume_file:
            resume_text = read_resume(resume_file)
            if not resume_text:
                st.error("Unsupported file type. Please upload a PDF, DOCX, or TXT file.")
                return None
            return resume_text
