
import os
from pprint import pprint as pp
import requests

from make_md_table import table
from save_file_to_github import save_file_to_github


def fetch_top_repos(username: str, token: str) -> list:

    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'bearer {token}'}

    query = '''
    query ($login: String!, $limit: Int!) {
      user(login: $login) {
        repositories(first: $limit, orderBy: {field: STARGAZERS, direction: DESC}) {
          edges {
            node {
              name
              stargazers {
                totalCount
              }
            }
          }
        }
      }
    }
    '''

    variables = {'login': username, 'limit': 10}
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)
    
    if response.status_code == 200:
        data = response.json()
        repositories = data['data']['user']['repositories']['edges']
        popular_repos = [
            {
                "name": repo['node']['name'],
                "stars": repo['node']['stargazers']['totalCount']
            }
            for repo in repositories
            ]
        pp(popular_repos)
        return popular_repos
    else:
        print(f'Request failed with status code {response.status_code}')
        print(response.text)
        return []


def main():
  token = os.environ["FG_GITHUB_ACCESS_TOKEN"]
  popular_repos = fetch_top_repos('TheNewThinkTank', token)
  repo_name = 'project-metrics'
  file_path = 'query-results/popular_repos.md'
  file_content = table(popular_repos)
  save_file_to_github(repo_name, file_path, file_content)


if __name__ == "__main__":
    main()
