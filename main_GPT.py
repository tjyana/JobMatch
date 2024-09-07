import streamlit as st
from src.functions import find_jobs
import pandas as pd



def submit_GPT(resume_text):
    with st.spinner("Finding jobs..."):
        jobs = pd.read_csv('resume-data/jobs.csv')
        st.write("You might be a good fit for these jobs ")
        st.write("この仕事があってるかも")
        results = find_jobs(resume_text, jobs)
        return results
