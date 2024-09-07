import streamlit as st
from src.UI import UI_resume_input, UI_display_results
from src.main_BERT import results_BERT, results_GPT


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
            results = results_GPT(resume_text)
        else:
            results = results_BERT(resume_text, match)

        UI_display_results(results)




if __name__ == "__main__":
    main()
