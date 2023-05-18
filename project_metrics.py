"""_summary_
"""

import datetime
import os
from pprint import pprint as pp

import requests


def get_bb_repos():
    username = "Gustav_Collin_Rasmussen"
    url = f"https://api.bitbucket.org/2.0/repositories/{username}"

    response = requests.get(url)
    repos = response.json()["values"]

    # for repo in repos:
    #     print(repo["name"])

    return [
        {"name": repo["name"], "owner": username, "platform": "bitbucket"}
        for repo in repos
        ]


def get_gh_repos():
    username = "TheNewThinkTank"
    url = f"https://api.github.com/users/{username}/repos"

    response = requests.get(url)
    repos = response.json()

    # for repo in repos:
    #     print(repo["name"])

    return [
            {"name": repo["name"], "owner": username, "platform": "github"}
            for repo in repos
            ]


def get_gl_repos():
    username = "TheNewThinkTank"
    url = f"https://gitlab.com/api/v4/users/{username}/projects?owned=true&visibility=public"

    response = requests.get(url)
    repos = response.json()

    # for repo in repos:
    #     print(repo["name"])

    return [
            {"name": repo["name"], "owner": username, "platform": "gitlab"}
            for repo in repos
            ]


def get_repo_info(platforms, repo) -> dict:
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
    api_url = platform["api_url"].format(owner=repo["owner"], repo=repo["name"])
    headers = {"Authorization": f"Bearer {platform['access_token']}"}

    # Make API requests to get the information for the repository
    response = requests.get(api_url, headers=headers)
    data = response.json()
    pp(data)

    # Parse the information from the API response
    try:

        print("Parsing the information from the API response")

        info = {
            "name": data["name"],
            "owner": data["owner"]["login"],
            "platform": repo["platform"],
            "url": data["html_url"],
            "description": data["description"],
            "stars": data["stargazers_count"],
            "creation_date": datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
            "commits": 0,
            "open_issues": 0,
            "closed_issues": 0,
            "repo_size": data["size"],
            "health_status": "",
            "languages": []
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


def print_repo_info(repo_info) -> None:
    """_summary_

    :param repo_info: _description_
    :type repo_info: _type_
    """

    print(f"Name: {repo_info['name']}")
    print(f"Owner: {repo_info['owner']}")
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


def main() -> None:
    """_summary_
    """

    # print(get_gl_repos())
    # get_bb_repos()

    gh_repos = get_gh_repos()
    gl_repos = get_gl_repos()
    bb_repos = get_bb_repos()

    all_repos = []
    all_repos.extend(gh_repos)
    all_repos.extend(gl_repos)
    all_repos.extend(bb_repos)

    # Define the API endpoints and access tokens for each platform
    platforms = {
        "github": {
            "api_url": "https://api.github.com/repos/{owner}/{repo}",
            "access_token": os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
        },
        "gitlab": {
            "api_url": "https://gitlab.com/api/v4/projects/{owner}%2F{repo}",
            "access_token": os.environ["PROJECT_METRICS_GITLAB_ACCESS_TOKEN"]
        },
        # "bitbucket": {
        #     "api_url": "https://api.bitbucket.org/2.0/repositories/{owner}/{repo}",
        #     "access_token": os.environ["PROJECT_METRICS_BITBUCKET_ACCESS_TOKEN"]
        # },
    }

    # Iterate through the repositories and print their information

    # for repo in get_bb_repos():
    #     repo_info = get_repo_info(platforms, repo)
    #     print_repo_info(repo_info)
    #     print()  # Print a blank line to separate the output for each repository

    # for repo in gh_repos:
    #     repo_info = get_repo_info(platforms, repo)
    #     print_repo_info(repo_info)
    #     print()

    for repo in gl_repos:
        repo_info = get_repo_info(platforms, repo)
        pp(repo_info)
        # print_repo_info(repo_info)
        # print()

    # for repo in all_repos:
    #     repo_info = get_repo_info(platforms, repo)
    #     print_repo_info(repo_info)
    #     print()


if __name__ == "__main__":
    main()
