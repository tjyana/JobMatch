import streamlit as st
from src.functions import match_percentage, read_resume, find_jobs
from src.BERT_function import match_resume
from dotenv import load_dotenv
import re
import os
import time
import pandas as pd

# load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')

# additional features:
# job match mode: take resume input > compare to JD database and find best matches
# pdf upload: upload resume and JD as pdfs


# trying to create all chatgpt version of the main function
# pretty much taking out match_resume and doing everything within match_percentage

def main_GPT():
    # Title
    st.sidebar.title("JobMatch")
    st.sidebar.write("""Fill in your resume info to see which Money Forward job matches you best.""")

    # Input fields
    # Select input method: Copy and paste text or upload a file
    resume_method = st.sidebar.radio("""Choose Resume input method:""", ("File", "Text"), horizontal = True)

    # Input: Text
    if resume_method == "Text":
        resume_text = st.sidebar.text_area("Paste Resume text", height=200)
    # Input: File Upload
    elif resume_method == "File":
        resume_file = st.sidebar.file_uploader("Upload Resume file", type=["pdf", "docx", "txt"])
        if resume_file is not None:
            resume_text = read_resume(resume_file)

    # Submit button
    if st.sidebar.button("Submit"):

        # jobs = pd.read_csv('resume-data/jobs.csv')

        # with st.spinner("Finding jobs..."):
        #     st.write("You might be a good fit for these jobs:")
        #     results = find_jobs(resume_text, jobs)
        #     st.write(" ", results)


        with st.spinner("Finding jobs..."):
            process_inputs(resume_text)


def process_inputs(resume_text):

    jobs = pd.read_csv('resume-data/jobs.csv')

    st.write("You might be a good fit for these jobs:")
    results = find_jobs(resume_text, jobs)
    st.write(" ", results)



        # # Assess fit and display results
        # with st.spinner("Assessing fit..."):
        #     process_inputs(resume_text, jobs)


# def process_inputs(resume_text, output):
#     jobs = pd.read_csv('resume-data/jobs.csv')

#     st.write("You might be a good fit for these jobs:")
#     results = find_jobs(resume_text, jobs)
#     st.write(" ", results)

    # Function to display the final output:
    # Top 3 job matches plus estimated qualification percentage

    # for i, job in enumerate(output, 1):
    #     st.write(f"{i}: {job['Title']}")
    #     comparison = compare_resume(resume_text, job['Description'])
    #     pattern = r'Estimated qualification percentage: \d+%'
    #     match = re.search(pattern, comparison)
    #     if match:
    #         st.write(match.group(0))
    #     else:
    #         st.write("")
    #     st.write("")








if __name__ == "__main__":
    main()
