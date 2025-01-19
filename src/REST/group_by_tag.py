"""_summary_
"""

from typing import Any
import requests  # type: ignore


def fetch_repositories(username: str, headers: dict[str, str]) -> list[dict[str, Any]]:
    """Fetch repositories for a given user.

    :param username: GitHub username
    :type username: str
    :param headers: _description_
    :type headers: dict[str, str]
    :return: _description_
    :rtype: list[dict]
    """
    url = f"https://api.github.com/users/{username}/repos"
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return []
    return response.json()


def fetch_tags(tags_url: str, headers: dict[str, str]) -> list[dict[str, Any]]:
    """Fetch tags for a given repository.

    :param tags_url: _description_
    :type tags_url: str
    :param headers: _description_
    :type headers: dict[str, str]
    :return: _description_
    :rtype: list[dict]
    """
    response = requests.get(tags_url, headers=headers)
    if response.status_code != 200:
        return []
    return response.json()


def group_repos_by_tag(username: str, token: str) -> None:
    """Group repositories by tags and print the result.

    :param username: GitHub username
    :type username: str
    :param token: GitHub token for authentication
    :type token: str
    """
    headers: dict[str, str] = {"Authorization": f"token {token}"}
    repositories = fetch_repositories(username, headers)
    tag_groups: dict[str, list[str]] = {}

    for repo in repositories:
        name: str = repo["name"]
        tags_url: str = repo["tags_url"].replace("{/repo}", "")
        tags: list[dict[str, Any]] = fetch_tags(tags_url, headers)

        for tag in tags:
            tag_name = tag["name"]
            if tag_name in tag_groups:
                tag_groups[tag_name].append(name)
            else:
                tag_groups[tag_name] = [name]

    for tag, repos in tag_groups.items():  # type: ignore
        print(f"Tag: {tag}")
        for repo in repos:  # type: ignore
            print(f"- {repo}")
        print()


if __name__ == "__main__":
    group_repos_by_tag("USERNAME", "TOKEN")
