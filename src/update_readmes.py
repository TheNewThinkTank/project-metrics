
def add_repo_size_badge_to_readme(repo_name: str) -> None:
    size_badge = f"[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/{repo_name}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/{repo_name}/archive/refs/heads/main.zip)"

    with open("README.md", "r+") as readme:
        ...


def main():
    repo_name = "<my-awesome-repo>"
    # TODO: Check if repo's README.md has repo size badge already, otherwise:
    add_repo_size_badge_to_readme(repo_name)


if __name__ == "__main__":
    main()
