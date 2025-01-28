"""_summary_
"""

from loguru import logger  # type: ignore
from file_convertion_tools.make_md_table import table  # type: ignore
from src.REST.get_repos import get_all_repos, get_repo_info, print_repo_info  # type: ignore
from src.config import platforms  # type: ignore
from src.save_file_to_github import save_file_to_github  # type: ignore
from src.util.config_loader import config_data  # type: ignore


def repo_missing_descriptions(repo_info: dict | None) -> bool:
    """
    Determines if a repository is missing a description.

    :param repo_info: A dictionary containing repository information, or None.
    :type repo_info: dict | None
    :return: True if the repository is missing a description or if repo_info is None, False otherwise.
    :rtype: bool
    """

    if repo_info is None:
        return True
    return repo_info.get("description") is None


def get_repos_wo_desc(platforms: dict, all_repos: list) -> list:
    """_summary_

    :param platforms: _description_
    :type platforms: dict
    :param all_repos: _description_
    :type all_repos: list
    :return: _description_
    :rtype: list
    """

    logger.info(
        f"\t{'#' * 20}\tRepos missing descriptions:\t{'#' * 20}\t"
    )

    repos_wo_desc = []
    for repo in all_repos:
        repo_info = get_repo_info(platforms, repo)
        if repo_info and repo_missing_descriptions(repo_info):
            print_repo_info(repo_info)
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
    """_summary_"""

    basepath = f"{config_data['docs_path']}/query-results/"
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
    if not repos_wo_desc:
        print("No repositories without descriptions found.")
        return

    file_path = f"{basepath}repos-without-description.md"
    file_content = table(repos_wo_desc)
    save_file_to_github(config_data['project_name'], file_path, file_content)

    # popular_repos = get_popular_repos(platforms, all_repos)
    # for repo in popular_repos:
    #     print(repo)

    # with open("popular_repos.json", "w") as wf:
    #     for repo in popular_repos:
    #         wf.write(repo)


if __name__ == "__main__":
    main()
