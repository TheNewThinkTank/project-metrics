"""_summary_
"""

import os
from github import Auth, Github
from src.util.config_loader import config_data  # type: ignore


def get_gh_repos(
    username: str=config_data['GITHUB_USERNAME'],
    access_token=os.environ[config_data['GITHUB_TOKEN']],
):
    """_summary_

    :param username: _description_, defaults to 'TheNewThinkTank'
    :type username: str, optional
    :param access_token: _description_, defaults to os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
    :type access_token: _type_, optional
    :return:
    :rtype:
    """

    auth = Auth.Token(access_token)
    g = Github(auth=auth)
    user = g.get_user(username)
    repositories = user.get_repos()

    print([repo.name for repo in repositories])

    return [repo.name for repo in repositories]


if __name__ == "__main__":
    get_gh_repos()
