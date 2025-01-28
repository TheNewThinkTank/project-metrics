"""_summary_
"""

import os
from pprint import pprint as pp
from src.save_file_to_github import save_file_to_github  # type: ignore
from src.GraphQL.gh_graphql_post import graphql_post  # type: ignore
from file_convertion_tools.make_md_table import table  # type: ignore
from src.util.config_loader import config_data  # type: ignore


def fetch_top_repos(username: str, token: str) -> list:
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
        repositories(first: $limit, orderBy: {field: STARGAZERS, direction: DESC}) {
          edges {
            node {
              name
              description
              stargazers {
                totalCount
              }
            }
          }
        }
      }
    }
    """

    response = graphql_post(username, token, query)

    if response.status_code == 200:
        data = response.json()
        repositories = data["data"]["user"]["repositories"]["edges"]
        popular_repos = [
            {
                "name": repo["node"]["name"],
                "description": repo["node"]["description"],
                "stars": repo["node"]["stargazers"]["totalCount"],
            }
            for repo in repositories
        ]
        pp(popular_repos)
        return popular_repos
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)
        return []


def main() -> None:
    basepath = f"{config_data['DOCS_PATH']}/query-results/"
    token = os.environ[config_data['FINEGRAINED_GITHUB_TOKEN']]
    popular_repos = fetch_top_repos(config_data['GITHUB_USERNAME'], token)
    file_path = f"{basepath}popular-repos.md"
    file_content = table(popular_repos)
    save_file_to_github(config_data['PROJECT_NAME'], file_path, file_content)


if __name__ == "__main__":
    main()
