
# from github import Github

from config import platforms
from get_repos import get_all_repos

# # Authenticate yourself 
# g = Github("yourusername", "yourauthtoken")

# # Find your repository and path of README.md
# repo=g.get_user().get_repo("your repo")
# file = repo.get_contents("README.md")

# # The new contents of your README.md
# content = "your updated README file contents"

# # Update README.md
# repo.update_file("README.md", "commit message", content, file.sha)


# all_repos = get_all_repos()


def add_repo_size_badge_to_readme(repo_name: str) -> None:
    size_badge = f"[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/{repo_name}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/{repo_name}/archive/refs/heads/main.zip)"

    with open("README.md", "r+") as readme:
        text = readme.readlines()
        # text = readme.read()
        # tag = f"# {repo_name}"  # TODO: make case insensitive using regex

        readme.write(text[0])
        readme.write(size_badge)
        readme.write(*text[1:])


def main():
    repo_name = "world-maps"  # "<my-awesome-repo>"
    # TODO: Check if repo's README.md has repo size badge already, otherwise:
    add_repo_size_badge_to_readme(repo_name)


if __name__ == "__main__":
    main()
