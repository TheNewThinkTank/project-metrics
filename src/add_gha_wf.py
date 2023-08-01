"""Check if repo's main language is Python.
If so, check if GitHub Actions workflow already exists,
otherwise, add wf with Qualify-Code job, with linting etc.
"""

import os

from github import Auth, Github, Repository, InputGitTreeElement


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

    return f"""
    ---
    name: {repo.name} Workflow
    on:
        push:
        branches: {repo.default_branch}
        workflow_dispatch

    jobs:
        Qualify-Code:
        runs-on: ubuntu-latest

        steps:
            - name: Check out code
            uses: actions/checkout@v3
            - name: Setup Python
            uses: actions/setup-python@v4
            with:
                python-version: 3.11
                cache: pip

            - name: Install and cache poetry
            run: |
                curl -sSL https://install.python-poetry.org | python3 -
            if: steps.cache.outputs.cache-hit != 'true'

            - name: Cache poetry dependencies
            id: cache
            uses: actions/cache@v3
            with:
                path: ~/.cache/pypoetry/virtualenvs
                key: ${{ runner.os }}-poetry-${{ hashFiles('**/poetry.lock') }}
                restore-keys: ${{ runner.os }}-poetry-

            - name: Install dependencies with poetry
            run: poetry install
            env:
                POETRY_VIRTUALENVS_IN_PROJECT: true
            if: steps.cache.outputs.cache-hit != 'true'

            - name: Lint with ruff
            run: poetry add ruff && poetry run ruff

    """


def main():
    username = 'TheNewThinkTank'
    access_token = os.environ["PROJECT_METRICS_GITHUB_PAT"]  # os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
    auth = Auth.Token(access_token)
    g = Github(auth=auth)
    user = g.get_user(username)
    repositories = user.get_repos()

    # test on just two repos first
    python_repos_encountered = 0

    for repo in repositories:
        if not has_python_code(repo):
            continue
        if has_actions_workflow(repo):
            continue

        print(f"Processing repo: {repo.name}")

        file_content = make_gha_file_content(repo)
        create_workflow(repo, file_content)

        python_repos_encountered += 1
        if python_repos_encountered >= 2:
            print("has processed 2 python based repos now.\nquitting ...\n")
            break


if __name__ == "__main__":
    main()
