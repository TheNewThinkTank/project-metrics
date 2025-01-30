"""_summary_
"""

import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore
from src.save_file_to_github import save_file_to_github  # type: ignore
from src.util.get_gh_repos import get_gh_repos  # type: ignore
from src.config import settings  # type: ignore


def get_repo_names_and_sizes() -> tuple[list[str], list[int]]:
    """_summary_

    :return: _description_
    :rtype: tuple[list[str], list[int]]
    """
    repositories = get_gh_repos()
    name_and_size = {repo.name: repo.size for repo in repositories}
    data_by_size_desc = sorted(
        name_and_size.items(),
        key=lambda x: x[1],
        reverse=True
        )
    names = [item[0] for item in data_by_size_desc]
    sizes = [item[1] for item in data_by_size_desc]
    return names, sizes


def split_data(names, sizes, n):
    """_summary_

    :param names: _description_
    :type names: _type_
    :param sizes: _description_
    :type sizes: _type_
    :param n: _description_
    :type n: _type_
    :return: _description_
    :rtype: _type_
    """
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


def commit_barplot(
    names,
    sizes,
    filename="largest_repos"
) -> None:
    """_summary_

    :param names: _description_
    :type names: _type_
    :param sizes: _description_
    :type sizes: _type_
    :param filename: _description_, defaults to "largest_repos"
    :type filename: str, optional
    """
    sns.set_theme(style="whitegrid")
    basepath = f"{settings['DOCS_PATH']}/img/"
    figure_title_parts = filename.split("_")
    figure_title = " ".join(map(str.title, figure_title_parts))
    local_file_path = f"{basepath}{filename}.png"

    plt.figure(figsize=(12, 6))
    ax = sns.barplot(x=names, y=sizes, palette="pastel")
    plt.xlabel("repo name")
    plt.ylabel("repo size (KB)")
    plt.title(f"{figure_title}")
    ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
    plt.tight_layout()
    plt.savefig(local_file_path)
    plt.close()
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github(settings['PROJECT_NAME'], local_file_path, content)


def main() -> None:
    names, sizes = get_repo_names_and_sizes()
    n = 8

    (
        names_largest,
        sizes_largest,
        names_medium,
        sizes_medium,
        names_small,
        sizes_small,
        names_smallest,
        sizes_smallest,
    ) = split_data(names, sizes, n)

    commit_barplot(
        names=names_largest,
        sizes=sizes_largest,
        filename="largest_repos"
    )

    commit_barplot(
        names=names_medium,
        sizes=sizes_medium,
        filename="medium_repos"
    )

    commit_barplot(
        names=names_small,
        sizes=sizes_small,
        filename="small_repos"
    )

    commit_barplot(
        names=names_smallest,
        sizes=sizes_smallest,
        filename="smallest_repos"
    )


if __name__ == "__main__":
    main()
