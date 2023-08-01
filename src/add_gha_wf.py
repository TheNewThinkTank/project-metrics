"""Check if repo's main language is Python.
If so, check if GitHub Actions workflow already exists,
otherwise, add wf with Qualify-Code job, with linting etc.
"""

import os
# import textwrap

from github import Auth, Github, Repository, InputGitTreeElement

from REST.add_repo_size_badge import update_repo  # type: ignore


def has_python_code(repo: Repository.Repository) -> bool:

    languages = repo.get_languages()

    if 'Python' in languages:
        return True
    return False


def has_actions_workflow(repo: Repository.Repository) -> bool:

    workflows = repo.get_workflows()

    # Check if there are any workflows present in the repository
    if workflows.totalCount > 0:
        return True
    else:
        return False


def create_workflow(repo: Repository.Repository,
                    file_content: str,
                    file_path: str = ".github/workflows/wf.yml"
                    ) -> None:
    branch = repo.default_branch

    # Get the branch reference
    ref = repo.get_git_ref(f"heads/{branch}")

    # Get the latest commit of the branch
    latest_commit = repo.get_commit(ref.object.sha)

    # Create a new tree with the updated file
    new_tree = repo.create_git_tree([
        InputGitTreeElement(file_path, '100644', 'blob', file_content)
    ], base_tree=latest_commit.commit.tree)

    # Create a new commit
    new_commit = repo.create_git_commit(
        message=f"Add {file_path} via PyGithub from project-metrics",
        tree=new_tree,
        parents=[latest_commit.commit]
    )

    # Update the branch reference to the new commit
    ref.edit(sha=new_commit.sha)

    # Push the changes to the remote repository
    repo.get_git_ref(f"heads/{branch}").edit(new_commit.sha)


def make_gha_file_content(repo: Repository.Repository) -> str:
    """_summary_

    :param repo: _description_
    :type repo: Repository.Repository
    :return: _description_
    :rtype: str
    """

    with open("assets/python-wf.txt", "r") as rf:
        wf = rf.read().replace("{repo_name}", repo.name).replace("{repo_branch}", repo.default_branch)

    return wf


def get_readme_format(repo: Repository.Repository):
    return repo.get_readme().name.split(".")[-1]


def main():
    username = 'TheNewThinkTank'
    access_token = os.environ["PROJECT_METRICS_GITHUB_PAT"]
    auth = Auth.Token(access_token)
    g = Github(auth=auth)
    user = g.get_user(username)
    repositories = user.get_repos()

    # test on just one repo first
    python_repos_encountered = 0

    for repo in repositories:
        if not has_python_code(repo):
            continue

        print(f"Processing repo: {repo.name}")

        # Add pyproject.toml to repo if it doesn't exist already
        file_path = "pyproject.toml"
        with open("assets/pyproject.txt", "r") as rf:
            file_content = rf.read().replace("{project-name}", repo.name)
            file_content = file_content.replace("{description}", repo.description)
            file_content = file_content.replace("{readme-format}", get_readme_format(repo))
        try:
            repo.get_contents(file_path)
            print(f"File '{file_path}' already exists.")
        except Exception:
            repo.create_file(file_path, "chore: add pyproject.toml", file_content, branch=repo.default_branch)

        # TODO: add CI badge if not exists
        update_repo(username, repo, badge_name="ci_badge")

        if has_actions_workflow(repo):
            continue

        file_content = make_gha_file_content(repo)
        create_workflow(repo, file_content)

        python_repos_encountered += 1
        if python_repos_encountered >= 1:
            print("has processed 1 python based repos now.\nquitting ...\n")
            break


if __name__ == "__main__":
    main()
