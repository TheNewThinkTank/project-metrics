
from github import Github


def save_file_to_github(repo_name: str, file_path: str, file_content, github_token):
    """_summary_

    :param repo_name: _description_
    :type repo_name: _type_
    :param file_path: _description_
    :type file_path: _type_
    :param file_content: _description_
    :type file_content: _type_
    :param github_token: _description_
    :type github_token: _type_
    """

    g = Github(github_token)
    repo = g.get_user().get_repo(repo_name)

    branch_name = repo.default_branch

    try:
        # Get the existing file (if it exists)
        file = repo.get_contents(file_path, ref=branch_name)
        # Update the file
        repo.update_file(file_path, "Updating file", file_content, file.sha, branch=branch_name)
    except Exception as e:
        # If the file doesn't exist, create it
        repo.create_file(file_path, "Creating file", file_content, branch=branch_name)
