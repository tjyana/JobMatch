import streamlit as st
import os
import pandas as pd
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from openai import OpenAI


'''
BERT models to match resume to job descriptions
Use semantic similarity to match resume to job descriptions
'''



####### Load API Key #######
load_dotenv()
api_key = os.getenv('OPENAI_API_KEY')
if api_key is None:
    api_key = st.secrets['OPENAI_API_KEY']


####### Load Jobs DF #######

def get_df():
    csv_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../resume-data/jobs.csv'))
    jobs_df = pd.read_csv(csv_path)
    return jobs_df


####### Get Models (BERT only) #######

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


####### Search Functions (SEPARATE) #######

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


def search_GPT(resume_text, jd_text):

    # streamlit
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a tech recruiter screening resumes."
            },
            {
                "role": "user",
                "content": f"""
                Resume: ```{resume_text}```
                Job Descriptions: ```{jd_text}```

                You will be given 1 resume and a dataframe containing many job titles along with their descriptions.
                I would like you to:

                1. Please analyze the resume, and categorize the candidate into one of the following categories:
                    a. If the candidate is either an engineer or non-engineer job seeker.
                        Engineer: Engineering, QA, Data Science, SRE, Product Management, Design, etc.
                        Non-engineer roles: Marketing, Sales, Customer Success, Customer Support, Operations, HR, Legal, etc.
                    b. What specific type of role the candidate is experienced most in.
                        Engineer:
                            Development: Backend, Frontend, Fullstack, Mobile, etc.
                                For Development candidates, please also find the programming language they are most experienced in.
                            Other engineer: SRE, Data Engineer, Data Scientist, QA, etc.
                            Product: Product Management, Project Management, Design, Scrum Master, etc.
                        Non-engineer roles:
                            Marketing, Sales, Customer Support, Operations, Finance, HR, Legal, etc.

                2. Find the 3 best matching jobs for this candidate based on the job title and qualifications in the job description.
                Please make sure to consider the type of job the candidate is looking for or has experience in, and the type of job the job description is for.
                (ex: a backend engineer should be recommended for backend engineer positions, not a marketing job. A customer support person should not be recommended for a software engineering job, etc.).
                It's better if the candidate is recommended same type of job they are currently in.
                It's ok if the job titles are not an exact match, but they should be in the same category.
                Recommending multiple types of jobs is fine, but please make sure to recommend the best matching jobs first.

                3. After you've identified the 3 best matching jobs, please compare the resume to each job description and give an estimated match percentage for each job.
                Please especially focus on the mandatory qualifications of the job and penalize heavily for any missing mandatory qualifications.

                4. Please provide the final response output in the following format.
                Do not output the above analysis in final response. Only output the final response in the following format:

                FINAL RESPONSE OUTPUT FORMAT (please make sure to include the full job titles. DO NOT output the rubric in the final response):
                ```
                ## Job 1: [Job Title 1]
                Estimated match percentage: [percentage]

                ## Job 2: [Job Title 2]
                Estimated match percentage: [percentage]

                ## Job 3: [Job Title 3]
                Estimated match percentage: [percentage]
                ```

                """
            }
        ]
    )

    content = completion.choices[0].message.content

    return content


####### Top 3 Functions (SEPARATE) #######

def top3_BERT(resume_text, match):
    with st.spinner("Finding jobs..."):
        jobs_df = get_df()
        model = get_model(match)
        top3 = search_BERT(model, resume_text, jobs_df)

        print('match_resume top3:', top3)
        return top3


def top3_GPT(resume_text):
    with st.spinner("Finding jobs..."):
        jobs_df = get_df()
        top3 = search_GPT(resume_text, jobs_df)
        return top3


####### Match Percentage Functions (SEPARATE) #######

def match_percentage(resume_text, jd_text):
    '''
    Function to calculate the match percentage between the resume and job description.
    Used in both the BERT and GPT models.
    '''

    # streamlit
    client = OpenAI()

    completion = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system",
             "content": "You are a tech recruiter screening resumes."
            },
            {
                "role": "user",
                "content": f"""
                Resume: ```{resume_text}```
                Job Descriptions: ```{jd_text}```

                You will be given 1 resume and 3 job titles along with their descriptions.
                Please compare the resume to each job description and give an estimated qualification percentage for each job.
                Please penalize heavily for any missing mandatory qualifications.

                Please use the below grading rubric to determine the estimated qualification percentage (do NOT output the rubric in the final response):

                ## Candidate Summary:
                (summarize candidate's experiences and skills and compare to persona of job description)

                # Qualifications:
                [✅/❌] [Qualification 1]: [What you can tell from the resume]
                [✅/❌] [Qualification 2]: [What you can tell from the resume]
                etc.

                # Nice-to-have:
                [✅/❌] [Nice-to-have 1]: [What you can tell from the resume]
                [✅/❌] [Nice-to-have 2]: [What you can tell from the resume]
                etc.

                Skill gaps: [consider any notable skill gaps]


                FINAL RESPONSE OUTPUT FORMAT:
                ```
                ## Job 1: [Job Title 1]
                Estimated match percentage: [percentage]

                ## Job 2: [Job Title 2]
                Estimated match percentage: [percentage]

                ## Job 3: [Job Title 3]
                Estimated match percentage: [percentage]
                ```

                """
            }
        ]
    )

    content = completion.choices[0].message.content

    return content

####### Results Functions (SEPARATE) #######

def results_BERT(resume_text, top3):
    with st.spinner("Assessing fit..."):
        results = match_percentage(resume_text, top3)
        return results


def results_GPT(resume_text, top3):
    with st.spinner("Assessing fit..."):
        results = match_percentage(resume_text, top3)
        return results
