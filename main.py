
from bs4 import BeautifulSoup
from Job import Job
from os import listdir
from os.path import isfile, join
import requests
import json

from SqlDB import SqlDB


# function to extract html document from given url
def getHTMLdocument(url):

    # request for HTML document of given url
    response = requests.get(url)

    # response will be provided in JSON format
    return response.text


# function to get the number of open positions
def get_num_of_open_positions(url):
    # create document
    html_document = getHTMLdocument(url_to_scrape)

    # create soap object
    soup = BeautifulSoup(html_document, 'html.parser')

    num_of_open_positions = soup.find('h1', class_='search-results-heading').text
    num_of_open_positions = str(num_of_open_positions)[0:3]

    return num_of_open_positions


# function to build a Job object
def create_job(data):
    start = data.find('/')
    end = data.find(' ') - 1
    job_description = data[start:end]
    job_description = "https://jobs.dell.com" + job_description

    start = data.find("<h2>") + 4
    end = data[start:].find("</h2>") + start
    job_title = data[start: end]

    start = data.find("job-location-search") + 21
    end = data[start:].find("</span>") + start
    job_location = data[start:end]

    if ',' in job_location:
        country_and_city = job_location.split(',')
        city = country_and_city[0].strip()
        country = country_and_city[1].strip()

    else:
        country = city = job_location

    job = Job(job_title, country, city, job_description)

    return job


# function to save the Job object into json file
def covert_job_to_json(job, num):
    with open('jsons/' + str(num) + ".json", "w") as outfile:
        json.dump(job.__dict__, outfile)


# function to get all the values from json file to insert sql

def jsons_to_values(dir_path):

    values = []
    # get all json full paths of the json files in dir_path
    all_json_files = [join(dir_path, f) for f in listdir(dir_path) if isfile(join(dir_path, f)) and f.endswith(".json")]

    for json_file_path in all_json_files:
        with open(json_file_path) as input_file:
            json_array = json.load(input_file)
            values.append(list(json_array.values()))

    return values


if __name__ == '__main__':

    # assign URL
    url_to_scrape = "https://jobs.dell.com/search-jobs"

    # get the number of the open positions
    num_of_open_positions = get_num_of_open_positions(url_to_scrape)

    # request for all jobs in the web in 1 page.
    json_url = f"https://jobs.dell.com/search-jobs/results?CurrentPage=1&RecordsPerPage={num_of_open_positions}&SearchResultsModuleName=Search+Results"

    print(json_url)

    res = requests.get(json_url)
    json_data = res.json()

    jobs_data = json_data["results"]
    jobs_data = jobs_data[jobs_data.find("href"):]

    jobs_before_clean = jobs_data.split("href")

    jobs = []
    for ind, job_before in enumerate(jobs_before_clean[1:]):
        temp_job = create_job(job_before)
        jobs.append(temp_job)
        covert_job_to_json(temp_job, ind)

    # for j in jobs:
    #     print(j)

    # login to sql db
    db = SqlDB()

    # convert all the json files to list of values
    values = jsons_to_values('jsons')

    # insert all to sql table.
    db.insert_many(values)

    # print all the rows
    db.select_all()








