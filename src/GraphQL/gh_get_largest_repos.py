"""
"""

import os
from src.GraphQL.gh_graphql_post import graphql_post  # type: ignore
from src.config import settings  # type: ignore

single_repo_query = """
{
  repository(name: "fitness-tracker", owner: $login) {
    diskUsage
  }
}
"""

"""
{
  repositoryOwner(login: $login) {
    repositories(first: $limit, orderBy: {field: UPDATED_AT, direction: DESC}, privacy: PUBLIC, isFork: false) {
      totalCount
      totalDiskUsage
      nodes {
        name
        diskUsage
      }
    }
  }
}
"""

"""
{
  search(query: "user:TheNewThinkTank size:>1000 is:public fork:false", type: REPOSITORY, first: $limit) {
    repositoryCount
    nodes {
      ... on Repository {
        name
        diskUsage
      }
    }
  }
}
"""


def handle_graphql_post_response(response) -> None:
    if response.status_code == 200:
        data = response.json()
        user = data.get("data", {}).get("user")
        if user:
            repositories = user["repositories"]["nodes"]
            for repo in repositories:
                name = repo["name"]
                size = repo["diskUsage"]
                print(f"{name} - {size} bytes")
        else:
            print("Unable to fetch repositories.")
    else:
        print(f"Request failed with status code {response.status_code}")
        print(response.text)


def fetch_largest_repos(username: str, token) -> None:
    """_summary_

    :param username: _description_
    :type username: str
    :param token: _description_
    :type token: _type_
    """

    query = """
    query ($login: String!, $limit: Int!) {
      user(login: $login) {
        repositories(first: $limit, orderBy: {field: DISK_USAGE, direction: DESC}) {
          nodes {
            name
            diskUsage
          }
        }
      }
    }
    """

    response = graphql_post(username, token, query)
    handle_graphql_post_response(response)


def main() -> None:
    token = os.environ[settings['FINEGRAINED_GITHUB_TOKEN']]
    username = settings['GITHUB_USERNAME']
    fetch_largest_repos(username, token)


if __name__ == "__main__":
    main()
