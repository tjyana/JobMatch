import streamlit as st
from src.functions import read_resume
from main_BERT import submit_BERT
from main_GPT import submit_GPT



def main():
    # Title
    st.sidebar.title("JobMatch")
    st.sidebar.write("""Fill in your resume info to see which Money Forward job matches you best.""")
    st.sidebar.write("""履歴書を入力して、ピッタリの求人を探そう！""")

    # Input fields
    # Select input method: Copy and paste text or upload a file
    resume_method = st.sidebar.radio("""Resume input レジュメ入力""", ("File", "Text"), horizontal = True)

    # Input: Text
    if resume_method == "Text":
        resume_text = st.sidebar.text_area("Text Input テキスト入力", height=200)
    # Input: File Upload
    elif resume_method == "File":
        resume_file = st.sidebar.file_uploader("File Upload ファイル・アップロード", type=["pdf", "docx", "txt"])
        if resume_file is not None:
            resume_text = read_resume(resume_file)

    match = st.sidebar.radio("Match method マッチ方法", ("ChatGPT", "BERT"))

    # Submit button
    if st.sidebar.button("Submit"):

        if match == "ChatGPT":
            submit_GPT(resume_text)
        elif match == "BERT":
            submit_BERT(resume_text)



if __name__ == "__main__":
    main()
