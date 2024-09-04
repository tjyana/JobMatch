import streamlit as st
from src.functions import match_percentage
from src.BERT_function import match_resume_minilm, match_resume_multilingual




def submit_BERT_multilingual(resume_text):
    with st.spinner("Finding jobs..."):
        output = match_resume_multilingual(resume_text)
    with st.spinner("Assessing fit..."):
        st.write("You might be a good fit for these jobs ")
        st.write("この仕事があってるかも")
        results = match_percentage(resume_text, output)
        st.write(" ", results)


# ------------- in progress below
# adjust to take new match_resume

def submit_BERT_minilm(resume_text):
    with st.spinner("Finding jobs..."):
        output = match_resume_minilm(resume_text)
    return output



def process_inputs(resume_text, output):
    with st.spinner("Assessing fit..."):
        st.write("You might be a good fit for these jobs ")
        st.write("この仕事があってるかも")
        results = match_percentage(resume_text, output)
        st.write(" ", results)
