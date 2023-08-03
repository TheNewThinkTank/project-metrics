"""_summary_

Docs:
https://pygithub.readthedocs.io/en/stable/examples/Repository.html
"""

import os
from pathlib import Path
from typing import Literal

from github import Auth, Github, Repository, PaginatedList

from src.config import gh_badges


def get_badge(repo: Repository.Repository, badge_name: str):
    """_summary_

    :param badge: _description_
    :type badge: str
    :return: _description_
    :rtype: dict
    """

    badge = gh_badges[badge_name]

    if isinstance(badge["value"], str):  # type: ignore
        badge["value"] = badge["value"].replace("{repo}", repo.name)  # type: ignore

    elif isinstance(badge["value"], list):  # type: ignore
        badge["value"] = [url.replace("{repo}", repo.name)  # type: ignore
                          for url in badge["value"]  # type: ignore
                          ]  # type: ignore

    return badge


def update_readme(repo: Repository.Repository,
                  format: Literal['md', 'rst'],
                  badge_name: str
                  ) -> None:

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
    """_summary_

    :param username: _description_
    :type username: str
    :param repo: _description_
    :type repo: Repository.Repository
    :param badge_name: _description_
    :type badge_name: str
    """

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


def update_all_repos(username: str,
                     repositories: PaginatedList.PaginatedList[Repository.Repository]
                     ) -> None:
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
    username = 'TheNewThinkTank'
    access_token = os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
    auth = Auth.Token(access_token)
    g = Github(auth=auth)
    user = g.get_user(username)
    repositories = user.get_repos()
    update_all_repos(username, repositories)


if __name__ == "__main__":
    main()
