"""_summary_
"""

import os
from typing import Any
import yaml

with open(".config/config.yml", "r") as rf:
    data = yaml.safe_load(rf)

print(data)

# Define the API endpoints and access tokens for each platform
platforms = {
    "github": {
        "username": "TheNewThinkTank",
        "repos_url": "https://api.github.com/users/TheNewThinkTank/repos",
        "api_url": "https://api.github.com/repos/{owner}/{repo}",
        "access_token": os.environ.get("PROJECT_METRICS_GITHUB_ACCESS_TOKEN", ""),
        "stars": "stargazers_count",
        "url": "html_url",
    },
    "gitlab": {
        "username": "TheNewThinkTank",
        "repos_url": "https://gitlab.com/api/v4/users/TheNewThinkTank/projects?owned=true&visibility=public",
        "api_url": "https://gitlab.com/api/v4/projects/{owner}%2F{repo}",
        "access_token": os.environ.get("PROJECT_METRICS_GITLAB_ACCESS_TOKEN", ""),
        "stars": "star_count",
        "url": "web_url",
    },
    # "bitbucket": {
    #     "username": "Gustav_Collin_Rasmussen",
    #     "repos_url": "https://api.bitbucket.org/2.0/repositories/Gustav_Collin_Rasmussen",
    #     "api_url": "https://api.bitbucket.org/2.0/repositories/{owner}/{repo}",
    #     "access_token": os.environ.get('PROJECT_METRICS_BITBUCKET_ACCESS_TOKEN', ''),
    #     "stars": "",
    #     "url": ""
    # },
}

# GitHub badges
gh_badges: dict[str, Any] = {
    "size_badge": {
        "label": "GitHub repo size",
        "value": [
            "https://img.shields.io/github/repo-size/TheNewThinkTank/{repo}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size",
            "https://github.com/TheNewThinkTank/{repo}/archive/refs/heads/main.zip",
        ],
    },
    "ci_badge": {
        "label": "CI",
        "value": "https://github.com/TheNewThinkTank/{repo}/actions/workflows/wf.yml/badge.svg",
    },
    "codecov_badge": {
        "label": "codecov",
        "value": [
            "https://codecov.io/gh/TheNewThinkTank/{repo}/branch/main/graph/badge.svg",
            "https://codecov.io/gh/TheNewThinkTank/{repo})",
        ],
    },
}
