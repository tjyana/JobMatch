import requests
from bs4 import BeautifulSoup
import pandas as pd

# run to scrape job descriptions from careers page and save in jobs.csv
url = 'https://hrmos.co/pages/moneyforward/jobs?category=1707294702136684546'

# Function to scrape many times and keep appending
def scrape_careerspage(url, jobs):

    # Fetch the main page
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')

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

    return jobs

def loop_scrape(url_list):
    jobs = []
    for url in url_list:
        jobs = scrape_careerspage(url, jobs)

    return jobs

def save_to_csv(jobs):
    # Create DataFrame and save to CSV
    df = pd.DataFrame(jobs)
    df.to_csv('../resume-data/jobs.csv', index=False)

    print("Data successfully saved to jobs.csv")


def scrape_and_save(url_list):
    jobs = loop_scrape(url_list)
    save_to_csv(jobs)



# # Function to scrape job descriptions from careers page ONCE
# def scrape_careerspage(url):

#     # Fetch the main page
#     response = requests.get(url)
#     soup = BeautifulSoup(response.content, 'html.parser')

#     jobs = []

#     # Find all job entries
#     job_entries = soup.find_all('div', class_='pg-list-cassette-detail has-cover-image')  # Adjust class name as needed

#     # Iterate through each job entry
#     for job_entry in job_entries:
#         # Extract job title
#         job_title = job_entry.find('h2').text.strip()  # Extract text from <h2>

#         # Extract job description
#         job_description_tag = job_entry.find('span', class_='pg-list-cassette-body jsc-joblist-cassette-body')  # Adjust class name as needed
#         job_description = job_description_tag.text.strip() if job_description_tag else 'No description available'

#         # Append job data to list
#         jobs.append({'Job Title': job_title, 'Job Description': job_description})

#     return jobs
