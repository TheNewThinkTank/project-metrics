"""_summary_
"""

import concurrent.futures
from github import Github

GITHUB_ACCESS_TOKEN = "YOUR_ACCESS_TOKEN"

repositories = [
    {"owner": "owner1", "name": "repo1"},
    {"owner": "owner2", "name": "repo2"},
]


def update_repository(repo):
    # update the repository (e.g., placing badges on the README file)
    ...


def main():
    g = Github(GITHUB_ACCESS_TOKEN)

    # Divide repositories into smaller chunks (the chunk size can be customized)
    chunk_size = 2
    repository_chunks = [
        repositories[i : i + chunk_size]
        for i in range(0, len(repositories), chunk_size)
    ]

    with concurrent.futures.ProcessPoolExecutor(
        max_workers=2
    ) as executor:  # Adjust max_workers as needed
        futures = {
            executor.submit(update_repository, repo): repo_chunk
            for repo_chunk in repository_chunks
        }

        for future in concurrent.futures.as_completed(futures):
            repo_chunk = futures[future]
            try:
                future.result()
            except Exception as e:
                print(f"An error occurred while updating {repo_chunk}: {e}")


if __name__ == "__main__":
    main()
