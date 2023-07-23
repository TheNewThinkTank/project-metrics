import os
import requests
from github import Auth, Github

# Docs: https://pygithub.readthedocs.io/en/stable/examples/Repository.html#update-a-file-in-the-repository


def get_repo_size(username, repository):
    """Function to fetch the repository size"""

    url = f'https://api.github.com/repos/{username}/{repository}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data['size']
    return None


# GitHub credentials
username = 'TheNewThinkTank'

access_token = os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
auth = Auth.Token(access_token)
# Initialize the GitHub API client
g = Github(auth=auth)

# Fetch all repositories for the given user
user = g.get_user(username)
repositories = user.get_repos()


# repo = repositories[0]
# repository = repo.name
# print(f'Processing repository: {repository}')
# os.system(f'git clone https://github.com/{username}/{repository}.git')
# repo_path = os.path.join(os.getcwd(), repository)
# print(f"{repo_path = }")
# # size = get_repo_size(username, repository)
# # print(f"{size = }")
# size_badge = f"[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/{repository}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/{repository}/archive/refs/heads/main.zip)"
# contents = repo.get_contents("README.md", ref="master")
# content = contents.decoded_content.decode()
# if size_badge not in content:
#     repo.update_file(contents.path, "Chore: update README", size_badge + contents, contents.sha, branch="master")


for repo in repositories[:2]:
    repository = repo.name
    print(f'Processing repository: {repository}')

    print(repo)

    # Clone the repository locally
    os.system(f'git clone https://github.com/{username}/{repository}.git')

    # Get the local path of the repository
    repo_path = os.path.join(os.getcwd(), repository)

    size_badge = f"[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/{repository}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/{repository}/archive/refs/heads/main.zip)"


    # TODO: check if default branch is main or master

    git_ref = repo.default_branch
    print(git_ref)

    # git_ref = "main"

    contents = repo.get_contents("README.md", ref="master")



    # content = contents.decoded_content.decode()

    # if size_badge not in content:
    #     repo.update_file(contents.path, "Chore: update README", size_badge + contents, contents.sha, branch="master")
