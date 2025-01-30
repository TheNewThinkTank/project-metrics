"""_summary_
"""

import argparse
import os
from github import Github
from src.REST.add_badge import update_repo  # type: ignore
from src.config import settings  # type: ignore


def main() -> None:
    username = settings['GITHUB_USERNAME']
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo_name", type=str, required=True)
    args = parser.parse_args()
    repo_name = args.repo_name

    if repo_name == username:
        return

    g = Github(os.environ[settings['GITHUB_TOKEN']])
    repo = g.get_user().get_repo(repo_name)
    update_repo(username, repo, "size_badge")


if __name__ == "__main__":
    main()
