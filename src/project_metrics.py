"""_summary_
"""

# import datetime
from operator import itemgetter
import os
# from pprint import pprint as pp

import requests


def get_bb_repos(platforms: dict):

    platform = "bitbucket"
    username = platforms[platform]["username"]
    url = platforms[platform]["repos_url"]

    response = requests.get(url)
    repos = response.json()["values"]

    # for repo in repos:
    #     print(repo["name"])

    return [
        {"name": repo["name"], "owner": username, "platform": platform}
        for repo in repos
        ]


def get_gh_repos(platforms: dict):

    platform = "github"
    username = platforms[platform]["username"]
    url = platforms[platform]["repos_url"]

    response = requests.get(url)
    repos = response.json()

    return [
            {"name": repo["name"], "owner": username, "platform": platform}
            for repo in repos
            ]


def get_gl_repos(platforms: dict):

    platform = "gitlab"
    username = platforms[platform]["username"]
    url = platforms[platform]["repos_url"]

    response = requests.get(url)
    repos = response.json()

    return [
            {"name": repo["name"], "owner": username, "platform": platform}
            for repo in repos
            ]


def get_repo_info(platforms, repo) -> dict | None:
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

    # DEBUG
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
            "creation_date": data["created_at"],  # datetime.datetime.strptime(data["created_at"], "%Y-%m-%dT%H:%M:%SZ"),
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


def print_repo_info(repo_info) -> None:
    """_summary_

    :param repo_info: _description_
    :type repo_info: _type_
    """

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


def repo_missing_descriptions(repo_info):
    if not repo_info["description"]:
        return True
    return False


def get_all_repos(platforms):
    # print(get_gl_repos())
    # get_bb_repos()

    gh_repos = get_gh_repos(platforms)
    gl_repos = get_gl_repos(platforms)
    # bb_repos = get_bb_repos(platforms)

    all_repos = []
    all_repos.extend(gh_repos)
    all_repos.extend(gl_repos)
    # all_repos.extend(bb_repos)

    return all_repos


def get_repos_wo_desc(platforms, all_repos):

    print("  ####################     Repos missing descriptions:     ####################  ")

    repos_wo_desc = []

    for repo in all_repos:
        repo_info = get_repo_info(platforms, repo)
        if repo_missing_descriptions(repo_info):
            # print_repo_info(repo_info)
            repos_wo_desc.append(repo_info)

    return repos_wo_desc


def get_popular_repos(platforms, all_repos):

    print("  ####################     Popular repos:     ####################  ")

    popular_repos = []

    for repo in all_repos:
        repo_info = get_repo_info(platforms, repo)
        if repo_info["stars"] > 1:
            popular_repos.append(repo_info)

    popular_repos_descending = sorted(popular_repos, key=itemgetter('stars'), reverse=True)

    return popular_repos_descending


def main() -> None:
    """_summary_
    """

    # Define the API endpoints and access tokens for each platform
    platforms = {
        "github": {
            "username": "TheNewThinkTank",
            "repos_url": "https://api.github.com/users/TheNewThinkTank/repos",
            "api_url": "https://api.github.com/repos/{owner}/{repo}",
            "access_token": os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"],
            "stars": "stargazers_count",
            "url": "html_url"
        },
        "gitlab": {
            "username": "TheNewThinkTank",
            "repos_url": "https://gitlab.com/api/v4/users/TheNewThinkTank/projects?owned=true&visibility=public",
            "api_url": "https://gitlab.com/api/v4/projects/{owner}%2F{repo}",
            "access_token": os.environ["PROJECT_METRICS_GITLAB_ACCESS_TOKEN"],
            "stars": "star_count",
            "url": "web_url"
        },
        # "bitbucket": {
        #     "username": "Gustav_Collin_Rasmussen",
        #     "repos_url": "https://api.bitbucket.org/2.0/repositories/Gustav_Collin_Rasmussen",
        #     "api_url": "https://api.bitbucket.org/2.0/repositories/{owner}/{repo}",
        #     "access_token": os.environ["PROJECT_METRICS_BITBUCKET_ACCESS_TOKEN"],
        #     "stars": "",
        #     "url": ""
        # },
    }

    all_repos = get_all_repos(platforms)

    # Iterate through the repositories and print their information

    # for repo in get_bb_repos():
    #     repo_info = get_repo_info(platforms, repo)
    #     print_repo_info(repo_info)
    #     print()  # Print a blank line to separate the output for each repository

    # for repo in gl_repos:
    #     repo_info = get_repo_info(platforms, repo)
    #     print_repo_info(repo_info)
    #     print()

    # for repo in gh_repos:
    #     repo_info = get_repo_info(platforms, repo)
    #     print_repo_info(repo_info)
    #     print()

    repos_wo_desc = get_repos_wo_desc(platforms, all_repos)
    with open("testfile.txt", "w") as wf:
        for repo in repos_wo_desc:
            print(repo)
            wf.write(str(repo))

    # popular_repos = get_popular_repos(platforms, all_repos)
    # for repo in popular_repos:
    #     print(repo)
    
    # with open("popular_repos.json", "w") as wf:
    #     for repo in popular_repos:
    #         wf.write(repo)


if __name__ == "__main__":
    main()
