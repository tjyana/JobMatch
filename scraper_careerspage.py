import requests
from bs4 import BeautifulSoup
import pandas as pd

# run to scrape job descriptions from careers page and save in jobs.csv

# URL of the careers page
url = 'https://hrmos.co/pages/moneyforward/jobs?category=1707294702136684546'

# Fetch the main page
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')

jobs = []

# Find all job entries
job_entries = soup.find_all('div', class_='pg-list-cassette-detail has-cover-image')  # Adjust class name as needed

# Iterate through each job entry
for job_entry in job_entries:
    # Extract job title
    job_title = job_entry.find('h2').text.strip()  # Extract text from <h2>

    # Extract job description
    job_description_tag = job_entry.find('span', class_='pg-list-cassette-body jsc-joblist-cassette-body')  # Adjust class name as needed
    job_description = job_description_tag.text.strip() if job_description_tag else 'No description available'

    # Append job data to list
    jobs.append({'Job Title': job_title, 'Job Description': job_description})


# Create DataFrame and save to CSV
df = pd.DataFrame(jobs)
df.to_csv('../resume-data/jobs.csv', index=False)

print("Data successfully saved to jobs.csv")
