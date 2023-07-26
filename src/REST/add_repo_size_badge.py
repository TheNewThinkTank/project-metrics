import os
from pathlib import Path
import requests

from github import Auth, Github

# Docs: https://pygithub.readthedocs.io/en/stable/examples/Repository.html#update-a-file-in-the-repository


def get_repo_size(username: str, repository: str) -> str | None:
    """fetch the size of a repository"""

    url = f'https://api.github.com/repos/{username}/{repository}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data['size']
    return None


def update_readme(repo, format):

    if format == 'md':
        size_badge = f"[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/{repo.name}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/{repo.name}/archive/refs/heads/main.zip)"
        newline = '\n'
    elif format == 'rst':
        size_badge = f""".. image:: https://img.shields.io/github/repo-size/TheNewThinkTank/{repo.name}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size
                                :target: https://github.com/TheNewThinkTank/{repo.name}/archive/refs/heads/main.zip)"""
        newline = '\n\n'

    repo_contents = repo.get_contents(f"README.{format}", ref=repo.default_branch)
    content = repo_contents.decoded_content.decode()
    if size_badge not in content:
        updated_content = size_badge + newline + content
        repo.update_file(repo_contents.path, f"chore: update README.{format}", updated_content.encode(), repo_contents.sha, branch=repo.default_branch)


def update_repo(username, repo):
    print(f'Processing repository: {repo.name}')
    # Clone the repository locally
    os.system(f'git clone https://github.com/{username}/{repo.name}.git')
    # Get the local path of the repository
    repo_path = os.path.join(os.getcwd(), repo.name)

    # Check if README.md exists and update it
    readme_md_path = Path(repo_path + '/README.md')
    if readme_md_path.exists():
        update_readme(repo, 'md')

    # Check if README.rst exists and update it
    readme_rst_path = Path(repo_path + '/README.rst')
    if readme_rst_path.exists():
        update_readme(repo, 'rst')


def update_all_repos(username, repositories):
    for repo in repositories:

        # Skip the profile page
        if repo.name == username:
            continue

        update_repo(username, repo)


def main():

    # GitHub credentials
    username = 'TheNewThinkTank'
    access_token = os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
    auth = Auth.Token(access_token)
    # Initialize the GitHub API client
    g = Github(auth=auth)
    # Fetch all repositories for the given user
    user = g.get_user(username)
    repositories = user.get_repos()

    update_all_repos(username, repositories)


if __name__ == "__main__":
    main()
