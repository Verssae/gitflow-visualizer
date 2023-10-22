## GitHub Activity Workflow Visualizer
This is a CLI tool to visualize the workflow of a team's GitHub activity. 

## Features
- You can see PR merge, branch creation/deletion, direct/force push with a timeline.
- Color-coded for each team member.
- Auto squashing of consecutive commits.

## Installation
```
brew tap homebrew/cask-fonts
brew install --cask firacode-nerd-font

brew install poetry

poetry install
```

## Pre-requisites
```
echo "GITHUB_TOKEN=your_github_token" > .env
```

## Usage
```
poetry run python analyize_workflow.py -t team_info.json -n "team name" # -s student_info.json is optional

# or
poetry shell
python analyize_workflow.py -t team_info.json -n "team name" # -s student_info.json is optional
```

## Example Usage
```json
/* team_info.json */
[
    {
        "team": "Team 1",
        "repo": "https://github.com/team1/project"
    },
    {
        "team": "Team 2",
        "repo": "https://github.com/team2_owner/project2"
    },
...
]
```

```sh
poetry run python analyize_workflow.py -t team_info.json -n "Team 1"
```

## To Do
- [ ] Docs for `get_commits.py`
