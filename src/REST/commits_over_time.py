"""_summary_
"""

from datetime import datetime

import matplotlib.pyplot as plt
import requests

from save_file_to_github import save_file_to_github  # type: ignore

owner = "TheNewThinkTank"
repo = "N-body-simulations"

url = f"https://api.github.com/repos/{owner}/{repo}/commits"
response = requests.get(url)

if response.status_code == 200:
    commits_data = response.json()

    commit_dates = []
    commit_counts = []

    for commit in commits_data:
        commit_date = datetime.strptime(
            commit["commit"]["committer"]["date"], "%Y-%m-%dT%H:%M:%SZ"
        )
        commit_dates.append(commit_date)
        commit_counts.append(1)  # Each commit counts as 1

    plt.figure(figsize=(10, 6))
    plt.plot(commit_dates, commit_counts, marker="o")
    plt.title(f"Commit Activity - {repo}")
    plt.xlabel("Date")
    plt.ylabel("Number of Commits")
    plt.xticks(rotation=45)
    plt.tight_layout()
    # plt.show()
    local_file_path = f"imgs/commits_over_time_{repo}.png"
    plt.savefig(local_file_path)
    plt.close()
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)
else:
    print(f"Failed to fetch commit history. Status code: {response.status_code}")
