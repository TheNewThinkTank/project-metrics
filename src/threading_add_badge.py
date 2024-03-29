"""_summary_
"""

import concurrent.futures

from REST.add_badge import update_repo  # type: ignore
from util.get_gh_repos import get_gh_repos  # type: ignore


def update_all_repos(username, repositories):
    badge_name = "size_badge"

    def update_repo_wrapper(repo):
        if repo.name == username:
            return
        update_repo(username, repo, badge_name)

    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(update_repo_wrapper, repositories)


def main():
    username = "TheNewThinkTank"
    repositories = get_gh_repos()

    update_all_repos(username, repositories)


if __name__ == "__main__":
    main()
