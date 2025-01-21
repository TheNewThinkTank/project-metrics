"""_summary_
TODO: test this function
TODO: add docstring here
"""

from concurrent.futures import ThreadPoolExecutor, as_completed
from github.Repository import Repository
from src.REST.add_badge import update_repo  # type: ignore
from src.add_gha_wf import (  # type: ignore
    has_actions_workflow,
    # make_gha_file_content,
    # create_workflow,
    # create_file,
    add_language_files,
    create_and_add_workflow,
    repo_has_lang
)


def update_repos(username: str,
                 repositories: list[Repository],
                 language: str
                 ) -> None:
    """Update repositories with the specified language by adding necessary files and workflows.

    :param username: GitHub username
    :type username: str
    :param repositories: List of repository objects
    :type repositories: list
    :param language: Programming language of the repositories
    :type language: str
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

    def process_repo(repo):
        if not repo_has_lang(repo, language):
            return None

        print(f"Processing repo: {repo.name}")
        add_language_files(repo, lang_files[language])
        update_repo(username, repo, badge_name="ci_badge")

        if not has_actions_workflow(repo):
            create_and_add_workflow(repo, language)

        return repo.name

    with ThreadPoolExecutor() as executor:
        futures = []
        for repo in repositories:
            if repos_encountered >= num_repos_to_update:
                break

            futures.append(executor.submit(process_repo, repo))
            repos_encountered += 1

        for future in as_completed(futures):
            repo_name = future.result()
            if repo_name:
                print(f"Finished processing repo: {repo_name}")

    print(
        f"\t\thas processed {num_repos_to_update}"
        f"{language}-based repos now.\nquitting ...\n"
        )
