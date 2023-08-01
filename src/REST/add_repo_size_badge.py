import os
from pathlib import Path
# import requests  # type: ignore
from typing import Literal

from github import Auth, Github, Repository, PaginatedList

# Docs: https://pygithub.readthedocs.io/en/stable/examples/Repository.html#update-a-file-in-the-repository


# def get_repo_size(username: str, repository: str) -> str | None:
#     """Fetch the size of a repository.

#     :param username: _description_
#     :type username: str
#     :param repository: _description_
#     :type repository: str
#     :return: _description_
#     :rtype: str | None
#     """

#     url = f'https://api.github.com/repos/{username}/{repository}'
#     response = requests.get(url)
#     if response.ok:
#         data = response.json()
#         return data['size']
#     return None


def get_badge(repo: Repository.Repository, badge_name: str) -> dict:
    """_summary_

    :param badge: _description_
    :type badge: str
    :return: _description_
    :rtype: dict
    """

    badges = {
        "size_badge": {
            "label": "GitHub repo size",
            "value": [
                f"https://img.shields.io/github/repo-size/TheNewThinkTank/{repo.name}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size",
                f"https://github.com/TheNewThinkTank/{repo.name}/archive/refs/heads/main.zip",
            ]
        },
        "ci_badge": {
            "label": "CI",
            "value": f"https://github.com/TheNewThinkTank/{repo.name}/actions/workflows/wf.yml/badge.svg",
        },
        "codecov_badge": {
            "label": "codecov",
            "value": [
                f"https://codecov.io/gh/TheNewThinkTank/{repo.name}/branch/main/graph/badge.svg",
                f"https://codecov.io/gh/TheNewThinkTank/{repo.name})"
            ]
        }
    }

    return badges[badge_name]


def update_readme(repo: Repository.Repository, format: Literal['md', 'rst'], badge_name: str) -> None:

    badge = get_badge(repo, badge_name)

    newlines = {
        'md': '\n',
        'rst': '\n\n'
    }
    newline = newlines[format]

    if format == 'md':
        if isinstance(badge['value'], list):
            badge_content = f"[![{badge['label']}]({badge['value'][0]})]({badge['value'][1]})"
        else:
            badge_content = f"![{badge['label']}]({badge['value']})"

    elif format == 'rst':
        if isinstance(badge['value'], list):
            badge_content = f""".. image:: {badge['value'][0]}
                                  :target: {badge['value'][1]}"""
        else:
            badge_content = f""".. image:: {badge['value']}"""

    repo_contents = repo.get_contents(f"README.{format}", ref=repo.default_branch)
    content = repo_contents.decoded_content.decode()  # type: ignore
    if badge_content not in content:
        updated_content = badge_content + newline + content
        repo.update_file(repo_contents.path,  # type: ignore
                         f"chore: update README.{format}",
                         updated_content.encode(),
                         repo_contents.sha,  # type: ignore
                         branch=repo.default_branch
                         )


def update_repo(username: str, repo: Repository.Repository, badge_name: str) -> None:

    print(f'Processing repository: {repo.name}')
    # Clone the repository locally
    os.system(f'git clone https://github.com/{username}/{repo.name}.git')
    # Get the local path of the repository
    repo_path = os.path.join(os.getcwd(), repo.name)

    # Check if README.md exists and update it
    readme_md_path = Path(repo_path + '/README.md')
    if readme_md_path.exists():
        update_readme(repo, 'md', badge_name)

    # Check if README.rst exists and update it
    readme_rst_path = Path(repo_path + '/README.rst')
    if readme_rst_path.exists():
        update_readme(repo, 'rst', badge_name)


def update_all_repos(username: str, repositories: PaginatedList.PaginatedList[Repository.Repository]) -> None:
    """_summary_

    :param username: _description_
    :type username: str
    :param repositories: _description_
    :type repositories: PaginatedList.PaginatedList[Repository.Repository]
    """

    badge_names = [
        "size_badge",
        # "ci_badge",
        # "codecov_badge",
              ]

    for repo in repositories:

        # Skip the profile page
        if repo.name == username:
            continue

        for badge_name in badge_names:
            update_repo(username, repo, badge_name)


def main() -> None:
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
