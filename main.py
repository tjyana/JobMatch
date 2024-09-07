import streamlit as st
from src.UI import UI_resume_input
from src.main_BERT import process_inputs, submit_BERT
from main_GPT import submit_GPT



def main():
    # Title
    st.sidebar.title("JobMatch")
    st.sidebar.write("""Fill in your resume info to see which Money Forward job matches you best.""")
    st.sidebar.write("""レジュメを入力して、ピッタリの求人を探そう！""")

    resume_text = UI_resume_input()

    match = st.sidebar.radio("Match method (マッチ方法)", ("ChatGPT", "BERT (MiniLM)", "BERT (Multilingual)", "BERT (cl-tohoku)", "BERT (sonoisa)"))

    # Submit button
    if st.sidebar.button("Submit"):
        if match == "ChatGPT":
            top3 = submit_GPT(resume_text)
        else:
            top3 = submit_BERT(resume_text, match)

        process_inputs(resume_text, top3)




if __name__ == "__main__":
    main()
