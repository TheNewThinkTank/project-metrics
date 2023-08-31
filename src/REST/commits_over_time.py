"""_summary_
"""

from datetime import datetime  # type: ignore

import matplotlib.pyplot as plt  # type: ignore
import requests  # type: ignore

from save_file_to_github import save_file_to_github  # type: ignore

owner = "TheNewThinkTank"

repos = [
    "project-metrics",
    "code-vault",
    "fitness-tracker",
]

for repo in repos:
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
                    commit["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ"
                ).date()
                if commit_date in commit_activity:
                    commit_activity[commit_date] += 1
                else:
                    commit_activity[commit_date] = 1

            page += 1  # Move to the next page
        else:
            print(
                f"Failed to fetch commit history. Status code: {response.status_code}"
            )
            break

    sorted_dates = sorted(commit_activity.keys())
    commit_counts = [commit_activity[date] for date in sorted_dates]

    plt.figure(figsize=(10, 6))
    plt.plot(sorted_dates, commit_counts, marker="o")
    plt.title(f"Commit frequency - {repo}")
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    local_file_path = f"imgs/commits_over_time_{repo}.png"
    plt.savefig(local_file_path)
    plt.close()
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)
