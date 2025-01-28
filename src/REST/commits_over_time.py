"""_summary_
"""

from datetime import datetime  # type: ignore
from typing import Any
import matplotlib.pyplot as plt  # type: ignore
import requests  # type: ignore
from src.save_file_to_github import save_file_to_github  # type: ignore
from src.util.config_loader import config_data  # type: ignore


def fetch_commits(url: str, page: int) -> list[dict]:
    """Fetch commits from the GitHub API."""
    response = requests.get(url, params={"page": page, "per_page": 100})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Failed to fetch commit history. Status code: {response.status_code}")
        return []


def process_commit_activity(
        commits_data: list[dict],
        commit_activity: dict
        ) -> None:
    """Process commit activity and update the commit_activity dictionary."""
    for commit in commits_data:
        commit_date = datetime.strptime(
            commit["commit"]["committer"]["date"],
            "%Y-%m-%dT%H:%M:%SZ"
        ).date()
        if commit_date in commit_activity:
            commit_activity[commit_date] += 1
        else:
            commit_activity[commit_date] = 1


def get_commits(owner: str, repo: str) -> tuple[list[datetime], list[int]]:
    """Get commit dates and counts for a given repository.

    :param owner: Repository owner
    :type owner: str
    :param repo: Repository name
    :type repo: str
    :return: Tuple of sorted commit dates and their corresponding counts
    :rtype: tuple[list[datetime], list[int]]
    """
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    commit_activity: dict[Any, Any] = {}
    page = 1

    while True:
        commits_data = fetch_commits(url, page)
        if not commits_data:
            break
        process_commit_activity(commits_data, commit_activity)
        page += 1

    sorted_dates = sorted(commit_activity.keys())
    commit_counts = [commit_activity[date] for date in sorted_dates]

    return sorted_dates, commit_counts


def make_line_chart(repo: str, sorted_dates: list, commit_counts: list) -> None:
    """_summary_

    :param repo: _description_
    :type repo: str
    :param sorted_dates: _description_
    :type sorted_dates: list
    :param commit_counts: _description_
    :type commit_counts: list
    """

    basepath = f"{config_data['docs_path']}/img/"

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, commit_counts, marker="o")
    plt.title(f"Commit frequency - {repo}")
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    local_file_path = f"{basepath}commits_over_time_{repo}.png"
    plt.savefig(local_file_path)
    plt.close()
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github(config_data['project_name'], local_file_path, content)


def main() -> None:
    owner = config_data['github_username']

    # repos = [
    #     "project-metrics",
    #     "code-vault",
    #     "fitness-tracker",
    # ]

    repos = config_data['active_repos']

    for repo in repos:
        sorted_dates, commit_counts = get_commits(owner, repo)
        make_line_chart(repo, sorted_dates, commit_counts)


if __name__ == "__main__":
    main()
