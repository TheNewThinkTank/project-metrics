"""_summary_
"""

import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore

from save_file_to_github import save_file_to_github  # type: ignore
from util.get_gh_repos import get_gh_repos  # type: ignore


def get_repo_names_and_sizes():
    repositories = get_gh_repos()
    name_and_size = {repo.name: repo.size for repo in repositories}
    data_by_size_desc = sorted(name_and_size.items(), key=lambda x: x[1], reverse=True)
    names = [item[0] for item in data_by_size_desc]
    sizes = [item[1] for item in data_by_size_desc]
    return names, sizes


def split_data(names, sizes, n=8):
    # n largest repos
    names_largest = names[:n]
    sizes_largest = sizes[:n]
    # medium sized repos
    names_medium = names[n : n + n]
    sizes_medium = sizes[n : n + n]
    # small repos
    names_small = names[n + n : -n]
    sizes_small = sizes[n + n : -n]
    # smallest repos
    names_smallest = names[-n:]
    sizes_smallest = sizes[-n:]

    return (
        names_largest,
        sizes_largest,
        names_medium,
        sizes_medium,
        names_small,
        sizes_small,
        names_smallest,
        sizes_smallest,
    )


def commit_4_barplots(
    names_largest,
    sizes_largest,
    names_medium,
    sizes_medium,
    names_small,
    sizes_small,
    names_smallest,
    sizes_smallest,
):
    sns.set(style="whitegrid")

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=names_largest, y=sizes_largest, palette="pastel")
    plt.xlabel("repo name")
    plt.ylabel("repo size (KB)")
    plt.title("Largest repos")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    local_file_path = f"imgs/{n}_largest_repos.png"
    plt.savefig(local_file_path)
    plt.close()
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=names_medium, y=sizes_medium, palette="pastel")
    plt.xlabel("repo name")
    plt.ylabel("repo size (KB)")
    plt.title("Medium-sized repos")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    local_file_path = f"imgs/{n}_medium_repos.png"
    plt.savefig(local_file_path)
    plt.close()
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=names_small, y=sizes_small, palette="pastel")
    plt.xlabel("repo name")
    plt.ylabel("repo size (KB)")
    plt.title("Small repos")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    local_file_path = "imgs/small_repos.png"
    plt.savefig(local_file_path)
    plt.close()
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=names_smallest, y=sizes_smallest, palette="pastel")
    plt.xlabel("repo name")
    plt.ylabel("repo size (KB)")
    plt.title("Smallest repos")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    local_file_path = f"imgs/{n}_smallest_repos.png"
    plt.savefig(local_file_path)
    plt.close()
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)


def main():
    names, sizes = get_repo_names_and_sizes()
    (
        names_largest,
        sizes_largest,
        names_medium,
        sizes_medium,
        names_small,
        sizes_small,
        names_smallest,
        sizes_smallest,
    ) = split_data(names, sizes)
    commit_4_barplots(
        names_largest,
        sizes_largest,
        names_medium,
        sizes_medium,
        names_small,
        sizes_small,
        names_smallest,
        sizes_smallest,
    )


if __name__ == "__main__":
    main()
