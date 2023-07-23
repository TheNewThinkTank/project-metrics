import os
import requests
from github import Auth, Github


def get_repo_size(username, repository):
    """Function to fetch the repository size"""

    url = f'https://api.github.com/repos/{username}/{repository}'
    response = requests.get(url)
    if response.ok:
        data = response.json()
        return data['size']
    return None


def update_readme(repo_path, size):
    """Function to update the README.md file"""

    with open(repo_path, 'r') as f:
        content = f.read()
        if 'repo-size.svg' not in content:
            badge = f'![Repo Size](https://img.shields.io/github/repo-size/{username}/{repository})'
            new_content = badge + '\n' + content
            with open(repo_path, 'w') as f:
                f.write(new_content)


# Your GitHub credentials
username = 'TheNewThinkTank'

access_token = os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
auth = Auth.Token(access_token)
# Initialize the GitHub API client
g = Github(auth=auth)  # access_token)

# Fetch all repositories for the given user
user = g.get_user(username)
repositories = user.get_repos()


########## Testing ###################

repo = repositories[0]
repository = repo.name
print(f'Processing repository: {repository}')
os.system(f'git clone https://github.com/{username}/{repository}.git')

repo_path = os.path.join(os.getcwd(), repository)
print(f"{repo_path = }")
size = get_repo_size(username, repository)
print(f"{size = }")


contents = repo.get_contents("README.md", ref="test")

repo.update_file(contents.path, size, size, contents.sha, branch="main")


# with open(os.path.join(repo_path, 'README.md'), 'r') as rf:
#     text = rf.read()
#     print("README before adding size: \n")
#     print(text)

# update_readme(os.path.join(repo_path, 'README.md'), size)

# with open(os.path.join(repo_path, 'README.md'), 'r') as rf:
#     text = rf.read()
#     print("README after adding size: \n")
#     print(text)


# print("git config:\n")

# print("git config --global user.email 'ProjectMetricsGHAagent@example.com':")
# os.system(f"git config --global user.email 'ProjectMetricsGHAagent@example.com'")

# print("git config --global user.name 'ProjectMetricsGHAagent':")
# os.system(f"git config --global user.name 'ProjectMetricsGHAagent'")


# print("git status:")
# os.system(f"git status")

# print(f"git add .:")
# os.system(f"git add .")

# print("git status:")
# os.system(f"git status")

# print("git commit -m 'update README':")
# os.system(f"git commit -m 'update README'")

# print("git status:")
# os.system(f"git status")

# print("git push")
# os.system(f"git push")

# print("remove local clone of repo")
# os.system(f'rm -rf {repo_path}')

########## Testing ###################



'''
# Process each repository
for repo in repositories:

    # print(f"{user = }")

    repository = repo.name
    print(f'Processing repository: {repository}')

    # Clone the repository locally
    os.system(f'git clone https://github.com/{username}/{repository}.git')

    # Get the local path of the repository
    repo_path = os.path.join(os.getcwd(), repository)

    # Fetch the repository size using the GitHub API
    size = get_repo_size(username, repository)

    # Update the README.md file with the badge if it's not already present
    update_readme(os.path.join(repo_path, 'README.md'), size)

    # Clean up by removing the local clone
    # os.system(f'rm -rf {repo_path}')
'''
