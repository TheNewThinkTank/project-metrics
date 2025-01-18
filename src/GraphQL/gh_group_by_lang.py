"""_summary_
"""

import os
from pprint import pprint as pp
from src.GraphQL.gh_graphql_post import graphql_post  # type: ignore
from src.save_file_to_github import save_file_to_github  # type: ignore
from file_convertion_tools.make_md_table import table_from_nested  # type: ignore
from src.util.config_loader import load_config  # type: ignore

config_data = load_config()


def group_repos_by_language(username: str, token: str) -> list:
    """_summary_

    :param username: _description_
    :type username: str
    :param token: _description_
    :type token: str
    :return: _description_
    :rtype: list
    """

    query = """
    query ($login: String!, $limit: Int!) {
      user(login: $login) {
        repositories(first: $limit, orderBy: {field: NAME, direction: ASC}) {
          nodes {
            name
            primaryLanguage {
              name
            }
          }
        }
      }
    }
    """

    response = graphql_post(username, token, query, limit=100)

    if response.status_code != 200:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return []

    data = response.json()
    repositories = data["data"]["user"]["repositories"]["nodes"]

    language_groups = dict()  # type: ignore

    for repo in repositories:
        repo_name = repo["name"]
        language = repo["primaryLanguage"]

        if language is None:
            continue

        language_name = language["name"]

        if language_name in language_groups:
            language_groups[language_name].append(repo_name)
        else:
            language_groups[language_name] = [repo_name]

    pp(language_groups)
    return [language_groups]


def main() -> None:
    basepath = f"{config_data['docs_path']}/query-results/"
    lang_repos = group_repos_by_language(
        config_data['github_username'],
        os.environ[config_data['finegrained_github_token']]
    )
    file_path = f"{basepath}group-by-lang.md"
    file_content = table_from_nested(lang_repos)

    save_file_to_github(config_data['project_name'], file_path, file_content)


if __name__ == "__main__":
    main()
