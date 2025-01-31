b"""_summary_
"""

import os
import requests  # type: ignore
# from icecream import ic  # type: ignore
from loguru import logger  # type: ignore
from src.config import settings  # type: ignore


def get_repos(platform: str) -> list[dict]:
    """_summary_

    :param platform: _description_
    :type platform: str
    :return: _description_
    :rtype: list[dict]
    """

    username = settings.platforms[platform]["username"]
    url = settings.platforms[platform]["repos_url"]

    headers = {
        "Authorization": f"token {os.getenv(settings.GITHUB_TOKEN)}"  # {os.getenv('PROJECT_METRICS_GITHUB_ACCESS_TOKEN')}"
    }

    response = requests.get(url, headers=headers)
    response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
    repos = response.json()

    if platform == "bitbucket":
        repos = repos["values"]

    logger.info(f"{platform=}")
    # ic(platform)

    return [
        {"name": repo["name"], "owner": username, "platform": platform}
        for repo in repos
    ]


def get_all_repos() -> list:
    """_summary_

    :return: _description_
    :rtype: list
    """

    gh_repos = get_repos("github")
    gl_repos = get_repos("gitlab")
    # bb_repos = get_repos("bitbucket")

    all_repos = []
    all_repos.extend(gh_repos)
    all_repos.extend(gl_repos)
    # all_repos.extend(bb_repos)

    return all_repos


def get_repo_info(platforms: dict, repo) -> dict | None:
    """Get the information for a single repository.

    :param platforms: _description_
    :type platforms: _type_
    :param repo: _description_
    :type repo: _type_
    :return: _description_
    :rtype: dict
    """

    # Get the API endpoint and access token for the repository's platform
    platform = platforms[repo["platform"]]
    api_url = platform["api_url"].format(
        owner=repo["owner"],
        repo=repo["name"]
        )
    headers = {"Authorization": f"Bearer {platform['access_token']}"}

    # Make API requests to get the information for the repository
    response = requests.get(api_url, headers=headers)
    data = response.json()

    # pp(data)
    # for k in sorted(data.keys()):
    #     print(k)

    # pp(data.keys())
    # print(type((data)))
    # print("name" in data.keys())
    # print(data["name"])

    try:
        # print("Parsing the information from the API response")
        info = {
            "name": data["name"],
            # "owner": data["owner"]["login"],
            "platform": repo["platform"],
            "url": data[platform["url"]],
            "description": data["description"],
            "stars": data[platform["stars"]],
            "creation_date": data[
                "created_at"
            ],
            # datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
            # "commits": 0,
            # "open_issues": 0,
            # "closed_issues": 0,
            # "repo_size": data["size"],
            # "health_status": "",
            # "languages": []
        }
    except KeyError:
        print(f"Error: could not get information for repository {repo}")
        return None

    # if repo["platform"] == "github":
    #     info["commits"] = data["default_branch"]
    #     issues_url = api_url + "/issues?state=all"
    # elif repo["platform"] == "gitlab":
    #     info["commits"] = data["default_branch"]
    #     issues_url = api_url + "/issues?state=all"
    # elif repo["platform"] == "bitbucket":
    #     response = requests.get(data["links"]["branches"]["href"], headers=headers)
    #     branch_data = response.json()
    #     default_branch = branch_data["values"][0]["name"]
    #     info["commits"] = default_branch
    #     issues_url = api_url + "/issues?q=state%20in%20(%22new%22,%22open%22,%22resolved%22,%22on_hold%22,%22invalid%22,%22duplicate%22)&fields=-votes,-watchers_count"

    # response = requests.get(issues_url, headers=headers)
    # data = response.json()
    # info["open_issues"] = data["size"]
    # info["closed_issues"] = len([issue for issue in data["values"] if issue["state"] == "closed"])

    # # Calculate the health status of the repository based on the number of open issues
    # if info["open_issues"] == 0:
    #     info["health_status"] = "good"
    # elif info["open_issues"] < 10:
    #     info["health_status"] = "fair"
    # else:
    #     info["health_status"] = "poor"

    # # Get the languages used in the repository
    # response = requests.get(api_url + "/languages", headers=headers)
    # data = response.json()
    # for language, bytes_of_code in data.items():
    #     info["languages"].append({"name": language, "bytes_of_code": bytes_of_code})

    return info


def print_repo_info(repo_info: dict | None) -> None:
    """_summary_

    :param repo_info: _description_
    :type repo_info: dict | None
    """

    if repo_info is None:
        return

    print(f"Name: {repo_info['name']}")
    # print(f"Owner: {repo_info['owner']}")
    print(f"Platform: {repo_info['platform']}")
    print(f"URL: {repo_info['url']}")
    print(f"Description: {repo_info['description']}")
    print(f"Stars: {repo_info['stars']}")
    print(f"Creation Date: {repo_info['creation_date']}")
    # print(f"Commits: {repo_info['commits']}")
    # print(f"Open Issues: {repo_info['open_issues']}")
    # print(f"Closed Issues: {repo_info['closed_issues']}")
    # print(f"Repo Size: {repo_info['repo_size']} bytes")
    # print(f"Health Status: {repo_info['health_status']}")
    # print("Languages:")
    # for language in repo_info["languages"]:
    #     print(f"\t{language['name']}: {language['bytes_of_code']} bytes")
