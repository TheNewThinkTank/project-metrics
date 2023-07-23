import os
import requests
from github import Github  # pip install PyGithub


def get_repo_size(username, repository):
    """Function to fetch the repository size"""

    url = f'https://api.github.com/repos/{username}/{repository}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data['size']
    return None


def update_readme(repo_path, size):
    """Function to update the README.md file"""

    with open(repo_path, 'r') as f:
        content = f.read()
        if 'repo-size.svg' not in content:
            badge = f'![Repo Size](https://img.shields.io/github/repo-size/{username}/{repository})'
            new_content = badge + '\n' + content
            with open(repo_path, 'w') as f:
                f.write(new_content)


# Your GitHub credentials
username = 'TheNewThinkTank'
access_token = os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]

# Initialize the GitHub API client
g = Github(access_token)

# Fetch all repositories for the given user
user = g.get_user(username)
repositories = user.get_repos()

# Process each repository
for repo in repositories:

    print(f"{user = }")

    repository = repo.name
    print(f'Processing repository: {repository}')

    # Clone the repository locally
    # os.system(f'git clone https://github.com/{username}/{repository}.git')

    # Get the local path of the repository
    # repo_path = os.path.join(os.getcwd(), repository)

    # Fetch the repository size using the GitHub API
    # size = get_repo_size(username, repository)

    # Update the README.md file with the badge if it's not already present
    # update_readme(os.path.join(repo_path, 'README.md'), size)

    # Clean up by removing the local clone
    # os.system(f'rm -rf {repo_path}')
