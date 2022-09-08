import os
import json
from typing import Dict, List, Optional, Union, cast
from IPython.display import display
from ipywidgets import IntProgress
import requests
import pandas as pd
from bs4 import BeautifulSoup

import time
from requests import get
from env import github_token, github_username


# due to github scraping limitaion, we can only scarp 90 repos every minite
# get repo name part will be in acauire.ipynb
# repo_name.csv file contain the repo_list

headers = {"Authorization": f"token {github_token}", "User-Agent": github_username} #setup token as described in README.md

if headers["Authorization"] == "token " or headers["User-Agent"] == "":
    raise Exception(
        "You need to follow the instructions marked TODO in this script before trying to use it"
    )

REPOS = repo_list

def github_api_request(url: str) -> Union[List, Dict]:
    time.sleep(0.25)
    print(url)
    response = requests.get(url, headers=headers, timeout=60) #get url. Use headers as specified above since website won't let you in without your token and username
    response_data = response.json() #convert to json format
    if int(response.headers['X-RateLimit-Remaining']) < 10: #once you have less than 10 repos before reaching the scraping limit, sleep for one minute to reset scraping limit
        print('Rate-limit exceeded. Slowing down.')
        time.sleep(60)
    if response.status_code != 200: #if you do not get '200' as a response code, flag and show error
        raise Exception(
            f"Error response from github api! status code: {response.status_code}, "
            f"response: {json.dumps(response_data)}"
        )
    return response_data

def get_repo_language(repo: str) -> str:
    url = f"https://api.github.com/repos/{repo}" #plug each repo from the list into url
    repo_info = github_api_request(url) #get repo info
    if type(repo_info) is dict:
        repo_info = cast(Dict, repo_info)
        return repo_info.get("language", None)
    raise Exception(
        f"Expecting a dictionary response from {url}, instead got {json.dumps(repo_info)}"
    )
    
def get_repo_contents(repo: str) -> List[Dict[str, str]]:
    url = f"https://api.github.com/repos/{repo}/contents/"
    contents = github_api_request(url)#get contents from repo
    if type(contents) is list:
        contents = cast(List, contents) #if content is in this format indicates which part of the info is the contents
        return contents
    raise Exception(
        f"Expecting a list response from {url}, instead got {json.dumps(contents)}"
    )
    
def get_readme_download_url(files: List[Dict[str, str]]) -> str:
    """
    Takes in a response from the github api that lists the files in a repo and
    returns the url that can be used to download the repo's README file.
    """
    for file in files:
        if file["name"].lower().startswith("readme"):
            return file["download_url"]
    return ""

def process_repo(repo: str) -> Dict[str, str]:
    """
    Takes a repo name like "gocodeup/codeup-setup-script" and returns a
    dictionary with the language of the repo and the readme contents.
    """
    contents = get_repo_contents(repo)
    try:
        readme_contents = requests.get(get_readme_download_url(contents)).text
    except:
        readme_contents = ''
    return {
        "repo": repo,
        "language": get_repo_language(repo),
        "readme_contents": readme_contents,
    }

def scrape_github_data() -> List[Dict[str, str]]:
    """
    Loop through all of the repos and process them. Returns the processed data.
    """
    f = IntProgress(min=0, max=len(REPOS), description='Downloading Data') #sets loading bar so you can monitor progress
    display(f)
    output = []
    for i, repo in enumerate(REPOS):
        f.value = i
        output.append(process_repo(repo))
    return output

def get_data(refresh=False): # get data if you have it. Download it if you don't.
    filename = './data.csv'
    if refresh or not os.path.isfile(filename):
        data = scrape_github_data()
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False)
    else:
        df = pd.read_csv(filename)
    return df

def wrangle_data():
    df = get_data()

    return df