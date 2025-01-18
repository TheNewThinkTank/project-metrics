"""_summary_
"""

import os
from github import Auth, Github, PaginatedList, Repository
from src.util.config_loader import load_config  # type: ignore

config_data = load_config()


def get_gh_repos(
    username: str=config_data['github_username'],
    access_token=os.environ[config_data['github_token']],
) -> PaginatedList.PaginatedList[Repository.Repository]:
    """_summary_

    :param username: _description_, defaults to 'TheNewThinkTank'
    :type username: str, optional
    :param access_token: _description_, defaults to os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
    :type access_token: _type_, optional
    :return: _description_
    :rtype: PaginatedList.PaginatedList[Repository.Repository]
    """

    auth = Auth.Token(access_token)
    g = Github(auth=auth)
    user = g.get_user(username)

    repositories = user.get_repos()

    # for repo in repositories:
    #     print(repo.name)

    return repositories


if __name__ == "__main__":
    get_gh_repos()
