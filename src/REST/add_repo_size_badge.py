import os
from pathlib import Path
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


###################  Test on a single repo before rolling out changes to all repos  ###################

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

###################  Test on a single repo before rolling out changes to all repos  ###################


# def update_readme(repo, size):
#     repo_contents = repo.get_contents("README.md", ref="master")
#     content = repo_contents.decoded_content.decode()

#     # Check if the size badge is already present
#     if not has_size_badge(content):
#         # Append the size badge to the content
#         badge = f'![Repo Size](https://img.shields.io/github/repo-size/{username}/{repository})'
#         updated_content = badge + '\n' + content

#         # Update the file
#         repo.update_file(repo_contents.path, "Update README.md", updated_content.encode(), repo_contents.sha, branch="master")


# def update_readme_rst(repo, size):
#     repo_contents = repo.get_contents("README.rst", ref="master")
#     content = repo_contents.decoded_content.decode()

#     # Check if the size badge is already present
#     if not has_size_badge(content):
#         # Append the size badge to the content
#         badge = f'.. image:: https://img.shields.io/github/repo-size/{username}/{repository}'
#         updated_content = badge + '\n\n' + content

#         # Update the file
#         repo.update_file(repo_contents.path, "Update README.rst", updated_content.encode(), repo_contents.sha, branch="master")


for repo in repositories:
    repository = repo.name

    # Skip the profile page
    if repository == username:
        continue

    print(f'Processing repository: {repository}')
    # Clone the repository locally
    os.system(f'git clone https://github.com/{username}/{repository}.git')
    # Get the local path of the repository
    repo_path = os.path.join(os.getcwd(), repository)

    # Check if README.md exists and update it
    readme_md_path = Path(repo_path + '/README.md')
    if readme_md_path.exists():
        size_badge = f"[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/{repository}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/{repository}/archive/refs/heads/main.zip)"
        # update_readme(repo, size)
        contents = repo.get_contents("README.md", ref=repo.default_branch)
        content = contents.decoded_content.decode()
        if size_badge not in content:
            repo.update_file(contents.path, "Chore: update README", size_badge + "\n" + content, contents.sha, branch=repo.default_branch)

    # Check if README.rst exists and update it
    readme_rst_path = Path(repo_path + '/README.rst')
    if readme_rst_path.exists():

        size_badge = f""".. image:: https://img.shields.io/github/repo-size/TheNewThinkTank/{repository}?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size
                               :target: https://github.com/TheNewThinkTank/{repository}/archive/refs/heads/main.zip)"""

        # update_readme_rst(repo, size)
        contents = repo.get_contents("README.rst", ref=repo.default_branch)
        content = contents.decoded_content.decode()
        if size_badge not in content:
            repo.update_file(contents.path, "Chore: update README", size_badge + "\n\n" + content, contents.sha, branch=repo.default_branch)
