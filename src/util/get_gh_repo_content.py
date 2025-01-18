"""
Get all of the file contents of the repository recursively.
"""

import os
from pprint import pprint as pp
from github import Auth, Github
from src.util.config_loader import load_config  # type: ignore

config_data = load_config()


def get_gh_repo_py_files(
        username=config_data['github_username'],
        access_token=os.environ[config_data['github_token']],
        repo_name=config_data['project_name']
        ) -> list:
    """_summary_

    :param username: _description_, defaults to "TheNewThinkTank"
    :type username: str, optional
    :param access_token: _description_, defaults to os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
    :type access_token: _type_, optional
    :param repo_name: _description_, defaults to "project-metrics"
    :type repo_name: str, optional
    :return: _description_
    :rtype: list
    """

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

    return [
        file
        for file in files
        if file.path.endswith(".py")
        and not file.path.endswith("__init__.py")
        ]


def main() -> None:

    # repo_names = [
    #     "project-metrics",
    #     "N-body-simulations",
    # ]

    repo_names = config_data['python_sample_repos']

    for repo_name in repo_names:
        print(f"files in {repo_name}:\n")
        pp(get_gh_repo_py_files(repo_name=repo_name))


if __name__ == "__main__":
    main()
