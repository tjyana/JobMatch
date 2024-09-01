import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity

'''
BERT model to match resume to job descriptions
Separate file for this function because of size of imports and dependencies
Use semantic similarity to match resume to job descriptions
'''

def match_resume(resume_text):
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resume-data/jobs.csv'))
    df = pd.read_csv(csv_path)

    # Step 1: Load the pre-trained model
    # model = SentenceTransformer('all-MiniLM-L6-v2')
    model = SentenceTransformer('sentence-transformers/paraphrase-xlm-r-multilingual-v1')

    # Step 2: Encode job descriptions into embeddings
    job_embeddings = model.encode(df['Job Title'].tolist(), convert_to_tensor=True)

    # Step 3: Example resume data
    resume = resume_text

    # Step 4: Encode resume into an embedding
    resume_embedding = model.encode([resume], convert_to_tensor=True)

    # Step 5: Calculate cosine similarities
    # Convert embeddings to numpy arrays first
    resume_embedding_cpu = resume_embedding.cpu().detach().numpy()
    job_embeddings_cpu = job_embeddings.cpu().detach().numpy()
    similarities = cosine_similarity(resume_embedding_cpu, job_embeddings_cpu)

    # Step 6: Get the indices of the top 5 most similar job descriptions
    top_3_indices = similarities[0].argsort()[-3:][::-1]  # Sort in descending order and get top 5

    # Step 7: Retrieve the top 5 matching job titles and descriptions
    top_3_matches = df.iloc[top_3_indices]

    # Step 8: Print the results
    results = []
    for idx, row in top_3_matches.iterrows():
        result = {
            "Title": row['Job Title'],
            "Description": row['Job Description']
        }
        results.append(result)

    return results
