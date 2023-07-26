"""_summary_
"""

# from operator import itemgetter
import os
from pprint import pprint as pp

from github import Github

from config import platforms
from get_repos import get_all_repos, get_repo_info


def repo_missing_descriptions(repo_info: dict) -> bool:
    """_summary_

    :param repo_info: _description_
    :type repo_info: dict
    :return: _description_
    :rtype: bool
    """

    return False if repo_info["description"] else True


def get_repos_wo_desc(platforms: dict, all_repos: list) -> list:
    """_summary_

    :param platforms: _description_
    :type platforms: dict
    :param all_repos: _description_
    :type all_repos: list
    :return: _description_
    :rtype: list
    """

    print("  ####################     Repos missing descriptions:     ####################  ")

    repos_wo_desc = []

    for repo in all_repos:
        repo_info = get_repo_info(platforms, repo)
        if repo_missing_descriptions(repo_info):
            # print_repo_info(repo_info)
            repos_wo_desc.append(repo_info)

    return repos_wo_desc


# def get_popular_repos(platforms: dict[str, dict], all_repos: list) -> list:
#     """_summary_

#     :param platforms: _description_
#     :type platforms: dict[str, dict]
#     :param all_repos: _description_
#     :type all_repos: list
#     :return: _description_
#     :rtype: list
#     """

#     print("  ####################     Popular repos:     ####################  ")

#     popular_repos = []

#     for repo in all_repos:
#         repo_info = get_repo_info(platforms, repo)
#         if repo_info["stars"] > 1:
#             popular_repos.append(repo_info)

#     popular_repos_descending = sorted(popular_repos, key=itemgetter('stars'), reverse=True)

#     return popular_repos_descending


def main() -> None:
    """_summary_
    """

    all_repos = get_all_repos()

    # for repo in bb_repos:
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
            pp(repo)
            wf.write(str(repo))

    # TODO: git push testfile.txt


    def save_file_to_github(repo_name, file_path, file_content, github_token):
        g = Github(github_token)
        repo = g.get_user().get_repo(repo_name)

        branch_name = repo.default_branch  # 'main'

        try:
            # Get the existing file (if it exists)
            file = repo.get_contents(file_path, ref=branch_name)
            # Update the file
            repo.update_file(file_path, "Updating file", *file_content, file.sha, branch=branch_name)
        except Exception as e:
            # If the file doesn't exist, create it
            repo.create_file(file_path, "Creating file", *file_content, branch=branch_name)

    repo_name = 'project-metrics'
    file_path = 'testfile.txt'
    file_content = repos_wo_desc
    github_token = os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]

    save_file_to_github(repo_name, file_path, file_content, github_token)

    # popular_repos = get_popular_repos(platforms, all_repos)
    # for repo in popular_repos:
    #     print(repo)
    
    # with open("popular_repos.json", "w") as wf:
    #     for repo in popular_repos:
    #         wf.write(repo)


if __name__ == "__main__":
    main()
