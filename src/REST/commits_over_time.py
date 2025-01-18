"""_summary_
"""

from datetime import datetime  # type: ignore
import matplotlib.pyplot as plt  # type: ignore
import requests  # type: ignore
from src.save_file_to_github import save_file_to_github  # type: ignore
from src.util.config_loader import load_config  # type: ignore

config_data = load_config()


def get_commits(owner: str, repo: str) -> tuple[list, list]:
    """_summary_

    :param owner: _description_
    :type owner: str
    :param repo: _description_
    :type repo: str
    :return: _description_
    :rtype: tuple[list, list]
    """

    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    commit_activity = dict()  # type: ignore
    page = 1
    while True:
        response = requests.get(
            url, params={"page": page, "per_page": 100}
        )  # Fetch 100 commits per page
        if response.status_code == 200:
            commits_data = response.json()

            if not commits_data:  # No more commits, break the loop
                break

            for commit in commits_data:
                commit_date = datetime.strptime(
                    commit["commit"]["committer"]["date"],
                    "%Y-%m-%dT%H:%M:%SZ"
                ).date()
                if commit_date in commit_activity:
                    commit_activity[commit_date] += 1
                else:
                    commit_activity[commit_date] = 1

            page += 1  # Move to the next page
        else:
            print(
                f"Failed to fetch commit history."
                f"Status code: {response.status_code}"
            )
            break

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
