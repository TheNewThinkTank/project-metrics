
import requests

from config import platforms


def get_repos(platform: str) -> list[dict]:
    """_summary_

    :param platform: _description_
    :type platform: str
    :return: _description_
    :rtype: list[dict]
    """

    username = platforms[platform]["username"]
    url = platforms[platform]["repos_url"]

    response = requests.get(url)
    repos = response.json()["values"] if platform == "bitbucket" else response.json()

    return [
        {"name": repo["name"], "owner": username, "platform": platform}
        for repo in repos
        ]
