
import os
import requests

# import sys
# sys.path.append(".")
# sys.path.append("..")

from tomark import Tomark

from save_file_to_github import save_file_to_github


def fetch_top_repos(username, token):
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
        for repo in repositories:
            name = repo['node']['name']
            stargazers = repo['node']['stargazers']['totalCount']
            print(f'{name} - {stargazers} stargazers')

        return [
            {
                "name": repo['node']['name'],
                "stars": repo['node']['stargazers']['totalCount']
            }
            for repo in repositories
            ]

    else:
        print(f'Request failed with status code {response.status_code}')
        print(response.text)


def main():
  token = os.environ["FG_GITHUB_ACCESS_TOKEN"]
  popular_repos = fetch_top_repos('TheNewThinkTank', token)
  
  repo_name = 'project-metrics'
  file_path = 'popular_repos.md'

  file_content = Tomark.table(popular_repos)
  # print(file_content)
  github_token = os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
  save_file_to_github(repo_name, file_path, file_content, github_token)


if __name__ == "__main__":
    main()
