"""_summary_

Docs:
https://pygithub.readthedocs.io/en/stable/examples/Repository.html
"""

import os
from pathlib import Path
from typing import Literal
from github import PaginatedList, Repository
from src.get_badge import get_badge  # type: ignore
from src.util.get_gh_repos import get_gh_repos  # type: ignore
from src.config import settings  # type: ignore


def generate_badge_content(badge: dict, format: str) -> str:
    """Generate the badge content based on the format.

    :param badge: Badge information
    :type badge: dict
    :param format: Format of the README file ("md" or "rst")
    :type format: str
    :return: Badge content string
    :rtype: str
    """
    format_map = {
        "md": (
            f"[![{badge['label']}]({badge['value'][0]})]({badge['value'][1]})",
            f"![{badge['label']}]({badge['value']})",
        ),
        "rst": (
            f""".. image:: {badge['value'][0]}
            :target: {badge['value'][1]}""",
            f""".. image:: {badge['value']}""",
        ),
    }

    if isinstance(badge["value"], list):
        return format_map[format][0]
    return format_map[format][1]


def update_readme(
    repo: Repository.Repository,
    format: Literal["md", "rst"],
    badge_name: str
) -> None:
    """Update the README file with a badge.

    :param repo: GitHub repository object
    :type repo: Repository.Repository
    :param format: Format of the README file ("md" or "rst")
    :type format: Literal["md", "rst"]
    :param badge_name: Name of the badge to add
    :type badge_name: str
    """

    repo_name = repo.name
    badge = get_badge(repo_name, badge_name)
    newline = {"md": "\n", "rst": "\n\n"}.get(format, "\n")

    badge_content = generate_badge_content(badge, format)
    readme_path = f"README.{format}"
    repo_contents = repo.get_contents(readme_path, ref=repo.default_branch)
    content = repo_contents.decoded_content.decode()  # type: ignore

    if badge_content in content:
        return

    updated_content = badge_content + newline + content
    repo.update_file(
        repo_contents.path,  # type: ignore
        f"chore: update README.{format}",
        updated_content.encode(),
        repo_contents.sha,  # type: ignore
        branch=repo.default_branch,
    )


def update_repo(
        username: str,
        repo: Repository.Repository,
        badge_name: str
        ) -> None:
    """_summary_

    :param username: _description_
    :type username: str
    :param repo: _description_
    :type repo: Repository.Repository
    :param badge_name: _description_
    :type badge_name: str
    """

    print(f"Processing repository: {repo.name}")
    # Clone the repository locally
    os.system(f"git clone https://github.com/{username}/{repo.name}.git")
    # Get the local path of the repository
    repo_path = os.path.join(os.getcwd(), repo.name)

    if Path(repo_path + "/README.md").exists():
        update_readme(repo, "md", badge_name)

    if Path(repo_path + "/README.rst").exists():
        update_readme(repo, "rst", badge_name)


def update_all_repos(
    username: str,
    repositories: PaginatedList.PaginatedList[Repository.Repository]
    ) -> None:
    """_summary_

    :param username: _description_
    :type username: str
    :param repositories: _description_
    :type repositories: PaginatedList.PaginatedList[Repository.Repository]
    """

    # badge_names = [
    #     "size_badge",
    #     # "ci_badge",
    #     # "codecov_badge",
    # ]

    badge_name = "size_badge"

    for repo in repositories:
        # Skip the profile page
        if repo.name == username:
            continue
        update_repo(username, repo, badge_name)
        # for badge_name in badge_names:
        #     update_repo(username, repo, badge_name)


def main() -> None:
    repositories = get_gh_repos()
    update_all_repos(settings['GITHUB_USERNAME'], repositories)


if __name__ == "__main__":
    main()
