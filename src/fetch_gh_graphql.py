
import os
import requests


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
    else:
        print(f'Request failed with status code {response.status_code}')
        print(response.text)


def main():
  token = os.environ["GITHUB_ACCESS_TOKEN"]
  fetch_top_repos('TheNewThinkTank', token)


if __name__ == "__main__":
    main()
