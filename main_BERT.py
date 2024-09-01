import streamlit as st
from src.functions import match_percentage
from src.BERT_function import match_resume




def submit_BERT(resume_text):
    with st.spinner("Finding jobs..."):
        output = match_resume(resume_text)
    with st.spinner("Assessing fit..."):
        st.write("You might be a good fit for these jobs ")
        st.write("この仕事があってるかも")
        results = match_percentage(resume_text, output)
        st.write(" ", results)
