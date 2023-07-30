import os

# Define the API endpoints and access tokens for each platform
platforms = {
    "github": {
        "username": "TheNewThinkTank",
        "repos_url": "https://api.github.com/users/TheNewThinkTank/repos",
        "api_url": "https://api.github.com/repos/{owner}/{repo}",
        "access_token": os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"],
        "stars": "stargazers_count",
        "url": "html_url"
    },
    "gitlab": {
        "username": "TheNewThinkTank",
        "repos_url": "https://gitlab.com/api/v4/users/TheNewThinkTank/projects?owned=true&visibility=public",
        "api_url": "https://gitlab.com/api/v4/projects/{owner}%2F{repo}",
        "access_token": os.environ["PROJECT_METRICS_GITLAB_ACCESS_TOKEN"],
        "stars": "star_count",
        "url": "web_url"
    },
    # "bitbucket": {
    #     "username": "Gustav_Collin_Rasmussen",
    #     "repos_url": "https://api.bitbucket.org/2.0/repositories/Gustav_Collin_Rasmussen",
    #     "api_url": "https://api.bitbucket.org/2.0/repositories/{owner}/{repo}",
    #     "access_token": os.environ["PROJECT_METRICS_BITBUCKET_ACCESS_TOKEN"],
    #     "stars": "",
    #     "url": ""
    # },
}
