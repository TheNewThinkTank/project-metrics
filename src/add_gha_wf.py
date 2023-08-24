"""Check if repo's main language is Python.
If so, check if GitHub Actions workflow already exists,
otherwise, add wf with Qualify-Code job, with linting etc.
"""

from github import InputGitTreeElement, Repository

from REST.add_badge import update_repo  # type: ignore
from util.get_gh_repos import get_gh_repos  # type: ignore
from util.get_readme_format import get_readme_format  # type: ignore
from util.repo_has_lang import repo_has_lang  # type: ignore


def has_actions_workflow(repo: Repository.Repository) -> bool:
    """_summary_

    :param repo: _description_
    :type repo: Repository.Repository
    :return: _description_
    :rtype: bool
    """

    workflows = repo.get_workflows()

    # Check if there are any workflows present in the repository
    if workflows.totalCount > 0:
        return True
    else:
        return False


def make_gha_file_content(repo: Repository.Repository, language: str = "Python") -> str:
    """_summary_

    :param repo: _description_
    :type repo: Repository.Repository
    :return: _description_
    :rtype: str
    """

    with open(f"assets/{language}/wf.txt", "r") as rf:
        wf = (
            rf.read()
            .replace("{repo_name}", repo.name)
            .replace("{repo_branch}", repo.default_branch)
        )

    return wf


def create_workflow(
    repo: Repository.Repository,
    file_content: str,
    file_path: str = ".github/workflows/wf.yml",
) -> None:
    """_summary_

    :param repo: _description_
    :type repo: Repository.Repository
    :param file_content: _description_
    :type file_content: str
    :param file_path: _description_, defaults to ".github/workflows/wf.yml"
    :type file_path: str, optional
    """

    branch = repo.default_branch

    # Get the branch reference
    ref = repo.get_git_ref(f"heads/{branch}")

    # Get the latest commit of the branch
    latest_commit = repo.get_commit(ref.object.sha)

    # Create a new tree with the updated file
    new_tree = repo.create_git_tree(
        [InputGitTreeElement(file_path, "100644", "blob", file_content)],
        base_tree=latest_commit.commit.tree,
    )

    # Create a new commit
    new_commit = repo.create_git_commit(
        message=f"Add {file_path} via PyGithub from project-metrics",
        tree=new_tree,
        parents=[latest_commit.commit],
    )

    # Update the branch reference to the new commit
    ref.edit(sha=new_commit.sha)

    # Push the changes to the remote repository
    repo.get_git_ref(f"heads/{branch}").edit(new_commit.sha)


def create_pyproject_file(repo: Repository.Repository) -> None:
    """Add pyproject.toml to repo if it doesn't exist already.

    :param repo: _description_
    :type repo: Repository.Repository
    """

    file_path = "pyproject.toml"
    repo_description = repo.description if repo.description is not None else ""

    with open("assets/Python/pyproject.txt", "r") as rf:
        file_content = rf.read().replace("{project-name}", repo.name)
        file_content = file_content.replace("{description}", repo_description)
        file_content = file_content.replace("{readme-format}", get_readme_format(repo))

    try:
        repo.get_contents(file_path)
        print(f"File '{file_path}' already exists.")
    except Exception:
        repo.create_file(
            file_path,
            "chore: add pyproject.toml",
            file_content,
            branch=repo.default_branch,
        )


def update_repos(username, repositories, language="Python"):
    # test on just a few repos first
    num_repos_to_update = 2
    repos_encountered = 0

    for repo in repositories:
        if not repo_has_lang(repo, language):
            continue
        print(f"Processing repo: {repo.name}")

        if language == "Python":
            create_pyproject_file(repo)

        if language == "TypeScript":
            # add tsconfig.json and .eslintrc.js (both from assets/TypeScript)
            ...

        update_repo(username, repo, badge_name="ci_badge")
        if has_actions_workflow(repo):
            continue

        if language == "Python":
            file_content = make_gha_file_content(repo)
            create_workflow(repo, file_content)
        if language == "TypeScript":
            file_content = make_gha_file_content(repo, language=language)
            create_workflow(
                repo,
                file_content,
                file_path=f".github/workflows/{language.lower()}-wf.yml",
            )

        print(f"\tcreated workflow for {repo.name}")
        repos_encountered += 1
        if repos_encountered >= num_repos_to_update:
            print(
                f"\t\thas processed {num_repos_to_update} {language}-based repos now.\nquitting ...\n"
            )
            break


def main() -> None:
    username = "TheNewThinkTank"
    repositories = get_gh_repos()

    update_repos(username, repositories)
    update_repos(username, repositories, "TypeScript")


if __name__ == "__main__":
    main()
