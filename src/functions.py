# from openai import OpenAI
# from dotenv import load_dotenv
# import os
# import streamlit as st

# # Local
# load_dotenv()
# api_key = os.getenv('OPENAI_API_KEY')

# # Streamlit
# if api_key is None:
#     api_key = st.secrets['OPENAI_API_KEY']


# def match_percentage(resume_text, jd_text):
#     '''
#     Function to calculate the match percentage between the resume and job description.
#     Used in both the BERT and GPT models.
#     '''

#     # streamlit
#     client = OpenAI()

#     completion = client.chat.completions.create(
#         model="gpt-4o-mini",
#         messages=[
#             {"role": "system",
#              "content": "You are a tech recruiter screening resumes."
#             },
#             {
#                 "role": "user",
#                 "content": f"""
#                 Resume: ```{resume_text}```
#                 Job Descriptions: ```{jd_text}```

#                 You will be given 1 resume and 3 job titles along with their descriptions.
#                 Please compare the resume to each job description and give an estimated qualification percentage for each job.
#                 Please penalize heavily for any missing mandatory qualifications.

#                 Please use the below grading rubric to determine the estimated qualification percentage (do NOT output the rubric in the final response):

#                 ## Candidate Summary:
#                 (summarize candidate's experiences and skills and compare to persona of job description)

#                 # Qualifications:
#                 [✅/❌] [Qualification 1]: [What you can tell from the resume]
#                 [✅/❌] [Qualification 2]: [What you can tell from the resume]
#                 etc.

#                 # Nice-to-have:
#                 [✅/❌] [Nice-to-have 1]: [What you can tell from the resume]
#                 [✅/❌] [Nice-to-have 2]: [What you can tell from the resume]
#                 etc.

#                 Skill gaps: [consider any notable skill gaps]


#                 FINAL RESPONSE OUTPUT FORMAT:
#                 ```
#                 ## Job 1: [Job Title 1]
#                 Estimated match percentage: [percentage]

#                 ## Job 2: [Job Title 2]
#                 Estimated match percentage: [percentage]

#                 ## Job 3: [Job Title 3]
#                 Estimated match percentage: [percentage]
#                 ```

#                 """
#             }
#         ]
#     )

#     content = completion.choices[0].message.content

#     return content


# # def search_GPT(resume_text, jd_text):

# #     # streamlit
# #     client = OpenAI()

# #     completion = client.chat.completions.create(
# #         model="gpt-4o-mini",
# #         messages=[
# #             {"role": "system",
# #              "content": "You are a tech recruiter screening resumes."
# #             },
# #             {
# #                 "role": "user",
# #                 "content": f"""
# #                 Resume: ```{resume_text}```
# #                 Job Descriptions: ```{jd_text}```

# #                 You will be given 1 resume and a dataframe containing many job titles along with their descriptions.
# #                 I would like you to:

# #                 1. Please analyze the resume, and categorize the candidate into one of the following categories:
# #                     a. If the candidate is either an engineer or non-engineer job seeker.
# #                         Engineer: Engineering, QA, Data Science, SRE, Product Management, Design, etc.
# #                         Non-engineer roles: Marketing, Sales, Customer Success, Customer Support, Operations, HR, Legal, etc.
# #                     b. What specific type of role the candidate is experienced most in.
# #                         Engineer:
# #                             Development: Backend, Frontend, Fullstack, Mobile, etc.
# #                                 For Development candidates, please also find the programming language they are most experienced in.
# #                             Other engineer: SRE, Data Engineer, Data Scientist, QA, etc.
# #                             Product: Product Management, Project Management, Design, Scrum Master, etc.
# #                         Non-engineer roles:
# #                             Marketing, Sales, Customer Support, Operations, Finance, HR, Legal, etc.

# #                 2. Find the 3 best matching jobs for this candidate based on the job title and qualifications in the job description.
# #                 Please make sure to consider the type of job the candidate is looking for or has experience in, and the type of job the job description is for.
# #                 (ex: a backend engineer should be recommended for backend engineer positions, not a marketing job. A customer support person should not be recommended for a software engineering job, etc.).
# #                 It's better if the candidate is recommended same type of job they are currently in.
# #                 It's ok if the job titles are not an exact match, but they should be in the same category.
# #                 Recommending multiple types of jobs is fine, but please make sure to recommend the best matching jobs first.

# #                 3. After you've identified the 3 best matching jobs, please compare the resume to each job description and give an estimated match percentage for each job.
# #                 Please especially focus on the mandatory qualifications of the job and penalize heavily for any missing mandatory qualifications.

# #                 4. Please provide the final response output in the following format.
# #                 Do not output the above analysis in final response. Only output the final response in the following format:

# #                 FINAL RESPONSE OUTPUT FORMAT (please make sure to include the full job titles. DO NOT output the rubric in the final response):
# #                 ```
# #                 ## Job 1: [Job Title 1]
# #                 Estimated match percentage: [percentage]

# #                 ## Job 2: [Job Title 2]
# #                 Estimated match percentage: [percentage]

# #                 ## Job 3: [Job Title 3]
# #                 Estimated match percentage: [percentage]
# #                 ```

# #                 """
# #             }
# #         ]
# #     )

# #     content = completion.choices[0].message.content

# #     return content
