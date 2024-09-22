# GitHub Activity Workflow Visualizer


The **GitHub Activity Workflow Visualizer** is a Python-based tool designed to visually analyze and track the workflow of a GitHub repository. It displays branch activities (e.g., branch creation, deletion, pull request merges) and other important events, allowing teams to easily understand the history of the repository's development process. For more information, see [GitHub API - List repository activities](https://docs.github.com/en/rest/repos/repos?apiVersion=2022-11-28#list-repository-activities).

![rich](./images/rich.png)

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Example 1: Core Branch Visualization](#example-1-core-branch-visualization)
  - [Example 2: Date Range Filtering](#example-2-date-range-filtering)
- [Customization](#customization)
- [Font Recommendation](#font-recommendation)
- [License](#license)
- [Contributing](#contributing)

## Features

- Visualize GitHub repository activities such as:
    ![icons](images/icons.png)
  - Branch creation 
  - Branch deletion
  - Pushes and force-pushes
  - Pull request merges
- Different colors for each user's activities
- Filter activities by date range
- Highlight active branches
- Abstract branch name like `release`, `hotfix`, and `feature` for better visualization.

## Installation

This project uses `poetry` for package management and dependency installation. Make sure you have `poetry` installed. If not, you can install it [here](https://python-poetry.org/docs/#installation).

### Step 1: Clone the Repository

```bash
git clone https://github.com/YourUsername/GitHub-Activity-Workflow-Visualizer.git
cd GitHub-Activity-Workflow-Visualizer
```

### Step 2: Install Dependencies

Run the following command to install the project dependencies via `poetry`:

```bash
poetry install
```

This will install the necessary dependencies, including `requests`, `rich`, and other libraries specified in `pyproject.toml`. You can use any other package manager or virtual environment if you prefer.

### Step 3: Configure Environment Variables

Create a `.env` file in the project root and add your GitHub token. The GitHub token is necessary to access the GitHub API for retrieving repository activity data.

```env
GITHUB_TOKEN=your_github_token_here
```

## Prerequisites

- Python 3.8+
- GitHub Personal Access Token (add to `.env` file)
- `poetry` package manager

## Usage

Once installed, you can use the script to visualize a GitHub repository's workflow. The script supports filtering activities based on core branches or specific date ranges.

```bash
usage: analyze_workflow.py [-h] [--core_branches [CORE_BRANCHES ...]] [--start_date START_DATE] [--end_date END_DATE] url

positional arguments:
  url                   GitHub repository URL

options:
  -h, --help            show this help message and exit
  --core_branches [CORE_BRANCHES ...]
                        List of core branch names. Other branch names would be abstracted (release->R, hotfix->H, feature->F)
  --start_date START_DATE
                        Start date in YYYY-MM-DD format
  --end_date END_DATE   End date in YYYY-MM-DD format
```

You can find some example outputs in the `images` directory.

## Customization

- **Core Branches**: By default, the tool includes `main`, `master`, and `develop` as core branches. You can override this using the `--core_branches` argument.
- **Date Range**: Use `--start_date` and `--end_date` to filter activities within a specific date range.

## Font Recommendation

For the best visual experience, it is recommended to use the **Fira Code** font. You can download and install it [here](https://github.com/tonsky/FiraCode) or via the following command on macOS:

```bash
brew tap homebrew/cask-fonts
brew install font-fira-code-nerd-font
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! If you'd like to contribute to this project, feel free to fork the repository and create a pull request.