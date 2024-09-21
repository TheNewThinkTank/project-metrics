"""
Get all of the file contents of the repository recursively.
"""

import os
from pprint import pprint as pp
from github import Auth, Github


def get_gh_repos(username, access_token, repo_name) -> list:
    auth = Auth.Token(access_token)
    g = Github(auth=auth)
    repo = g.get_repo(f"{username}/{repo_name}")

    contents = repo.get_contents("")
    if not isinstance(contents, list):
        contents = [contents]

    files = []
    while contents:
        file_content = contents.pop(0)
        if file_content.type == "dir":
            # contents.extend(repo.get_contents(file_content.path))
            new_contents = repo.get_contents(file_content.path)
            if not isinstance(new_contents, list):
                new_contents = [new_contents]
            contents.extend(new_contents)
        else:
            files.append(file_content)

    return [file for file in files if file.path.endswith(".py")]


def main():
    username = "TheNewThinkTank"
    access_token = os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]

    repo_names = [
        "project-metrics",
        "N-body-simulations",
    ]

    for repo_name in repo_names:
        print(f"files in {repo_name}:\n")
        pp(get_gh_repos(username, access_token, repo_name))


if __name__ == "__main__":
    main()
