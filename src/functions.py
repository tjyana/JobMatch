from openai import OpenAI
import pdfplumber

def match_percentage(resume_text, jd_text):

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
                Estimated qualification percentage: [percentage]

                ## Job 2: [Job Title 2]
                Estimated qualification percentage: [percentage]

                ## Job 3: [Job Title 3]
                Estimated qualification percentage: [percentage]
                ```

                """
            }
        ]
    )

    print(completion)
    print(completion.choices[0].message)

    content = completion.choices[0].message.content

    return content


def find_jobs(resume_text, jd_text):

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
                1. Please analyze the resume, and find 3 main skills and experience level with that skill (example: 3 years with ruby on rails, 2 years with flutter, 1 year with react).
                2. Find the 3 best matching jobs based on the qualifications in the job description and the skills and experiences in the resume.
                3. After you've identified the 3 best matching jobs, please compare the resume to each job description and give an estimated match percentage for each job.
                Please especially focus on the mandatory qualifications of the job and penalize heavily for any missing mandatory qualifications.

                FINAL RESPONSE OUTPUT FORMAT (please make sure to include the full job titles):
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

    print(completion)
    print(completion.choices[0].message)

    content = completion.choices[0].message.content

    return content


def read_resume(file):
    '''
    PDFPlumber is a Python library that extracts text, tables, and images from PDF files.
    read_resume function reads the resume file and extracts text from it.
    '''
    if file.type == "text/plain":
        # Read text file
        text = str(file.read(), "utf-8")
    elif file.type == "application/pdf":
        # Extract text from PDF
        with pdfplumber.open(file) as pdf:
            text = '\n'.join(page.extract_text() for page in pdf.pages if page.extract_text())
    elif file.type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        # Extract text from DOCX
        doc = docx.Document(file)
        text = '\n'.join(paragraph.text for paragraph in doc.paragraphs if paragraph.text)
    else:
        text = "Unsupported file type"
    return text
