import requests
import json
import csv
import os
from dotenv import load_dotenv
from icecream import ic

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")
OWNER = os.getenv("GITHUB_OWNER")
REPO = os.getenv("GITHUB_REPO")

# GitHub API Endpoint 설정
URL = f"https://api.github.com/repos/{OWNER}/{REPO}/commits"

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

all_commits = []

while URL:
    response = requests.get(URL, headers=headers)
    commits = response.json()
    all_commits.extend(commits)
    # 다음 페이지로 이동 (pagination)
    if 'next' in response.links:
        URL = response.links['next']['url']
    else:
        URL = None

# 학생별 커밋 정보 정렬
student_commits = {}
for commit in all_commits:
    # Use 'login' for the GitHub ID/nickname
    author = commit['author']['login'] if commit['author'] else commit['commit']['author']['name']
    # author = commit['author']['login'] if commit['author'] else None

    if not author:
        ic(commit['commit']['author'])
        continue

    if author not in student_commits:
        student_commits[author] = []
    student_commits[author].append({
        'date': commit['commit']['author']['date'],
        'message': commit['commit']['message'],
        'url': commit['html_url']
    })

with open('student_info.json', 'r', encoding='utf-8') as file:
    student_info = json.load(file)

# CSV 파일로 저장
with open('student_commits.csv', 'w', newline='', encoding='utf-16') as file:
    writer = csv.writer(file, delimiter='\t')  # Use tab as delimiter for utf-16
    writer.writerow(['Author', 'Name', 'Student Id', 'Team', 'Date', 'Message', 'URL'])
    for author, commits in student_commits.items():
        for commit in commits:
            try:
                vals = [val for val in student_info if val['nickname'] == author or val.get('alias', '') == author]
                name = vals[0]['name']
                team = vals[0]['team']
                sid = vals[0]['id']
                writer.writerow([author, name, sid, team, commit['date'], commit['message'], commit['url']])
            except IndexError:
                ic(f'IndexError: {author}')