"""_summary_
"""

import os
from typing import Any
from src.util.config_loader import config_data  # type: ignore

# Define the API endpoints and access tokens for each platform
platforms = {
    "github": {
        "username": config_data["GITHUB_USERNAME"],
        "repos_url": f"https://api.github.com/users/{config_data['GITHUB_USERNAME']}/repos",
        "api_url": "https://api.github.com/repos/{owner}/{repo}",
        "access_token": os.environ.get(config_data["GITHUB_TOKEN"], ""),
        "stars": "stargazers_count",
        "url": "html_url",
    },
    "gitlab": {
        "username": config_data["GITLAB_USERNAME"],
        "repos_url": f"https://gitlab.com/api/v4/users/{config_data['GITLAB_USERNAME']}/projects?owned=true&visibility=public",
        "api_url": "https://gitlab.com/api/v4/projects/{owner}%2F{repo}",
        "access_token": os.environ.get(config_data["GITLAB_TOKEN"], ""),
        "stars": "star_count",
        "url": "web_url",
    },
    # "bitbucket": {
    #     "username": config_data["BITBUCKET_USERNAME"],
    #     "repos_url": f"https://api.bitbucket.org/2.0/repositories/{config_data['BITBUCKET_USERNAME']}",
    #     "api_url": "https://api.bitbucket.org/2.0/repositories/{owner}/{repo}",
    #     "access_token": os.environ.get(config_data["BITBUCKET_TOKEN"], ''),
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
