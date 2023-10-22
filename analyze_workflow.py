import requests
import json

import os
from dotenv import load_dotenv
from datetime import datetime

from rich import box
from rich.align import Align
from rich.console import Console

from rich.table import Table

from argparse import ArgumentParser

load_dotenv()

TOKEN = os.getenv("GITHUB_TOKEN")

argparser = ArgumentParser()
argparser.add_argument('-n', '--team_name', type=str, default=None)
argparser.add_argument('-t', '--team_info', type=str, default=None)
argparser.add_argument('-s', '--student_info', type=str, default=None)

args = argparser.parse_args()


with open(args.team_info, 'r', encoding='utf-8') as file:
    team_info = json.load(file)

student_info = []

if args.student_info:
    with open(args.student_info, 'r', encoding='utf-8') as file:
        student_info = json.load(file)

def map_name(nickname):
    for student in student_info:
        if student['nickname'] == nickname:
            return student['name']
    return nickname

team_name = args.team_name
target_team = None
for team in team_info:
    if team['team'] == team_name:
        target_team = team
        break

console = Console(record=True)
console.clear()

core_branches = ['main', 'master', 'develop']

owner, repo = target_team['repo'].replace('https://github.com/', '').split('/')

# GitHub API Endpoint 설정
URL = f"https://api.github.com/repos/{owner}/{repo}/activity"

headers = {
    'Authorization': f'token {TOKEN}',
    'Accept': 'application/vnd.github.v3+json'
}

all_activities = []

while URL:
    response = requests.get(URL, headers=headers)
    activities = response.json()
    all_activities.extend(activities)
    # 다음 페이지로 이동 (pagination)
    if 'next' in response.links:
        URL = response.links['next']['url']
    else:
        URL = None

data = []
for activity in all_activities:
    dto = datetime.strptime(activity['timestamp'], '%Y-%m-%dT%H:%M:%SZ')
    
    datum = {
        "branch": activity['ref'].replace('refs/heads/', ''),
        "timestamp": f'{dto.year}/{dto.month}/{dto.day} {dto.hour}:{dto.minute}:{dto.second}',
        "activity_type": activity["activity_type"],
        "actor": map_name(activity["actor"]["login"]),
    }
    data.append(datum)
    
# 데이터 파싱 및 정렬
activities = []
for entry in data:
    timestamp = datetime.strptime(entry['timestamp'], '%Y/%m/%d %H:%M:%S')
    activities.append((timestamp, entry['branch'], entry['activity_type'], entry['actor']))
activities.sort(key=lambda x: x[0])  # 시간 순서대로 정렬

table = Table(show_footer=False, show_edge=False)
table.box = box.SIMPLE
table_centered = Align.center(table)

colors = ["red", "green", "cyan", "magenta", "yellow", "purple", "white", "gold3", "orange3", "gray63" ]
branch_columns = {}
branch_status = {}
actors = {}
actor_colors = {}
color_index = 0
branch_index = 0

branch = 'time'
table.add_column(branch, justify="center", no_wrap=True)
branch_columns[branch] = len(branch_columns)

branch_creations = []

for timestamp, branch, activity, actor in activities:
    if activity == 'branch_creation':
        branch_creations.append(branch)
    
    if branch not in branch_columns:
        branch_columns[branch] = len(branch_columns)

    if actor not in actors:
        actors[actor] = True
        actor_colors[actor] = colors[color_index % len(colors)]
        color_index += 1

actor_intro = ''
for actor in actor_colors:
    actor_intro += f' [{actor_colors[actor]}]󰙃 {actor}[/{actor_colors[actor]}]'
table.title = f"[bold]{target_team['team']}[/bold]\n{actor_intro}"

for branch in branch_columns:
    if branch == 'time':
        continue
    if branch in branch_creations:
        branch_status[branch] = False
    else:
        branch_status[branch] = True # 이미 있던 브랜치임 |    | 표시해야 됨
    
    if branch in core_branches:
        pass
    elif 'release' in branch.lower():
        branch = f'R{branch_columns[branch]}'
    elif 'hotfix' in branch.lower(): 
        branch = f'H{branch_columns[branch]}'
    else:
        branch = f'F{branch_columns[branch]}'
        
    table.add_column(branch, justify="center", no_wrap=True)

last_row_data = [None] * len(branch_columns)
last_timestamp_mmdd = None  # 이전 timestamp의 MMDD 값을 추적하는 변수

for timestamp, branch, activity, actor in activities: 

    match activity:
        case 'branch_creation':
            cell = f'┌─󱓊─┐'
            table.columns[branch_columns[branch]].header_style = 'not dim'
            branch_status[branch] = True
        case 'branch_deletion':
            cell = f'└─󱓋─┘'
            table.columns[branch_columns[branch]].header_style = 'dim'
            branch_status[branch] = False
        case 'force_push':
            if branch_status[branch]:
                cell = f'│~~│'
            else:
                cell = f'~~'
        case 'push':
            if branch_status[branch]:
                cell = f'│  │'
            else:
                cell = f''
        case 'pr_merge':
            cell = f'│  │'
        case _:
            cell = f'󰀍'

    timestamp_mmdd = timestamp.strftime("%m/%d")
    display_timestamp_mmdd = timestamp_mmdd if timestamp_mmdd != last_timestamp_mmdd else ""
    
    
    row_data = [display_timestamp_mmdd] + [None] * (len(branch_columns) - 1)  # 첫 열에 timestamp MMDD를 넣습니다.

    for br in branch_status:
        if branch_status[br]:
            row_data[branch_columns[br]] = '│   │'

    row_data[branch_columns[branch]] = f'[{actor_colors[actor]}]{cell}[/{actor_colors[actor]}]'

    if row_data[1:] != last_row_data[1:]:  # 연속된 행을 방지
        # with beat(1):
        table.add_row(*row_data)
        last_row_data = row_data.copy()
        last_timestamp_mmdd = timestamp_mmdd  # 이전 timestamp의 MMDD 값을 업데이트

# branch columns to captions
caption = ''
for branch in branch_columns:
    if branch == 'time':
        continue
    
    caption += f'[b]#{branch_columns[branch]}:[/b] {branch}\n'


console.print(table)
console.print('\n')
console.print(caption)
console.print(team_info)
