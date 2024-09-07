import streamlit as st
import pdfplumber


# PDF reader
def read_resume(file):
    '''
    PDFPlumber is a Python library that extracts text, tables, and images from PDF files.
    read_resume function reads the resume file and extracts text from it.
    '''
    if file.type == "text/plain":
        # Read text file
        text = str(file.read(), "utf-8")
    elif file.type == "application/pdf":
        # Extract text from PDF
        with pdfplumber.open(file) as pdf:
            text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Extract text from DOCX
        doc = docx.Document(file)
        text = '\n'.join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)
    else:
        text = "Unsupported file type"
    return text


# Resume input method
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


# Final display of results
def UI_display_results(results):
    st.write("You might be a good fit for these jobs:")
    st.write("この仕事があってるかも！")
    st.write(" ", results)
