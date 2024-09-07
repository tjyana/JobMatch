import streamlit as st
from src.functions import match_percentage
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


'''
BERT models to match resume to job descriptions
Use semantic similarity to match resume to job descriptions
'''

def get_df():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resume-data/jobs.csv'))
    jobs_df = pd.read_csv(csv_path)
    return jobs_df


def get_model(match):
    model_dict = {
    "BERT (MiniLM)": 'all-MiniLM-L6-v2',
    "BERT (Multilingual)": 'sentence-transformers/paraphrase-xlm-r-multilingual-v1',
    "BERT (cl-tohoku)": 'cl-tohoku/bert-base-japanese',
    "BERT (sonoisa)": 'sonoisa/sentence-bert-base-ja-mean-tokens'
    }
    model = SentenceTransformer(model_dict[match])

    print('get_model model:', model_dict[match])
    return model


def search_BERT(model, resume_text, jobs_df):
    # Step 2: Encode job descriptions into embeddings
    job_embeddings = model.encode(jobs_df['Job Title'].tolist(), convert_to_tensor=True)

    # Step 3: Example resume data
    resume = resume_text

    # Step 4: Encode resume into an embedding
    print(f"Resume text: {resume}")
    resume_embedding = model.encode([resume], convert_to_tensor=True)

    # Step 5: Calculate cosine similarities
    # Convert embeddings to numpy arrays first
    resume_embedding_cpu = resume_embedding.cpu().detach().numpy()
    job_embeddings_cpu = job_embeddings.cpu().detach().numpy()
    similarities = cosine_similarity(resume_embedding_cpu, job_embeddings_cpu)

    # Step 6: Get the indices of the top 5 most similar job descriptions
    top_3_indices = similarities[0].argsort()[-3:][::-1]  # Sort in descending order and get top 5

    # Step 7: Retrieve the top 5 matching job titles and descriptions
    top_3_matches = jobs_df.iloc[top_3_indices]

    # Step 8: Print the results
    top3 = []
    for idx, row in top_3_matches.iterrows():
        result = {
            "Title": row['Job Title'],
            "Description": row['Job Description']
        }
        top3.append(result)

    print('get_top3 top3:', top3)
    return top3


def top3_BERT(resume_text, match):
    with st.spinner("Finding jobs..."):
        jobs_df = get_df()
        model = get_model(match)
        top3 = search_BERT(model, resume_text, jobs_df)

        print('match_resume top3:', top3)
        return top3

def get_results(resume_text, top3):
    with st.spinner("Assessing fit..."):
        results = match_percentage(resume_text, top3)
        return results


def process_inputs(results):
    st.write("You might be a good fit for these jobs ")
    st.write("この仕事があってるかも"))
    st.write(" ", results)
