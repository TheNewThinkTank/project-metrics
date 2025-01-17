"""
Check if repo's main language is Python.
If so, check if GitHub Actions workflow already exists,
otherwise, add wf with Qualify-Code job, with linting etc.
"""

from github import InputGitTreeElement, Repository
from src.REST.add_badge import update_repo  # type: ignore
from src.util.get_gh_repos import get_gh_repos  # type: ignore
from src.util.get_readme_format import get_readme_format  # type: ignore
from src.util.repo_has_lang import repo_has_lang  # type: ignore


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


def create_file(
        repo: Repository.Repository,
        file_path: str,
        file_asset: str
        ) -> None:
    """_summary_

    :param repo: _description_
    :type repo: Repository.Repository
    :param file_path: _description_
    :type file_path: str
    :param file_asset: _description_
    :type file_asset: str
    """
    with open(file_asset, "r") as rf:
        file_content = rf.read()

        if file_path == "pyproject.toml":
            repo_description = repo.description if repo.description is not None else ""
            file_content = file_content.replace("{project-name}", repo.name)
            file_content = file_content.replace("{description}", repo_description)
            file_content = file_content.replace(
                "{readme-format}", get_readme_format(repo)
            )

        if file_path == "package-lock.json":
            file_content = file_content.replace("{project-name}", repo.name)

    try:
        repo.get_contents(file_path)
        print(f"File '{file_path}' already exists.")
    except Exception:
        repo.create_file(
            file_path,
            f"chore: add {file_path}",
            file_content,
            branch=repo.default_branch,
        )


def update_repos(username, repositories, language):
    """_summary_

    :param username: _description_
    :type username: _type_
    :param repositories: _description_
    :type repositories: _type_
    :param language: _description_
    :type language: _type_
    """
    # test on just a few repos first
    num_repos_to_update = 2
    repos_encountered = 0

    lang_files = {
        "Python": [("pyproject.toml", "assets/Python/pyproject.txt")],
        "TypeScript": [
            ("tsconfig.json", "assets/TypeScript/tsconfig.txt"),
            ("package.json", "assets/TypeScript/package.txt"),
            (".eslintrc.js", "assets/TypeScript/eslintrc.txt"),
            ("package-lock.json", "assets/TypeScript/package-lock.txt"),
        ],
    }

    for repo in repositories:
        if not repo_has_lang(repo, language):
            continue
        print(f"Processing repo: {repo.name}")

        for files in lang_files[language]:
            create_file(repo, files[0], files[1])

        update_repo(username, repo, badge_name="ci_badge")
        if has_actions_workflow(repo):
            continue

        # if language == "Python":
        #     file_content = make_gha_file_content(repo)
        #     create_workflow(repo, file_content)
        # if language == "TypeScript":
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
                f"\t\thas processed {num_repos_to_update}"
                f" {language}-based repos now.\nquitting ...\n"
            )
            break


def main() -> None:
    username = "TheNewThinkTank"
    repositories = get_gh_repos()

    languages = [
        "Python",
        "TypeScript",
    ]

    for language in languages:
        update_repos(username, repositories, language)


if __name__ == "__main__":
    main()
