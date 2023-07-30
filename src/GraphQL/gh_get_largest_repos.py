
import os
import requests

single_repo_query = '''
{
  repository(name: "Fitness-Tracker", owner: "TheNewThinkTank") {
    diskUsage
  }
}
'''

'''
{
  repositoryOwner(login: "TheNewThinkTank") {
    repositories(first: 10, orderBy: {field: UPDATED_AT, direction: DESC}, privacy: PUBLIC, isFork: false) {
      totalCount
      totalDiskUsage
      nodes {
        name
        diskUsage
      }
    }
  }
}
'''

'''
{
  search(query: "user:TheNewThinkTank size:>1000 is:public fork:false", type: REPOSITORY, first: 10) {
    repositoryCount
    nodes {
      ... on Repository {
        name
        diskUsage
      }
    }
  }
}
'''


def fetch_largest_repos(username, token):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'bearer {token}'}
    query = '''
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
    '''
    variables = {'login': username, 'limit': 10}
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        user = data.get('data', {}).get('user')
        if user:
            repositories = user['repositories']['nodes']
            for repo in repositories:
                name = repo['name']
                size = repo['diskUsage']
                print(f'{name} - {size} bytes')
        else:
            print('Unable to fetch repositories.')
    else:
        print(f'Request failed with status code {response.status_code}')
        print(response.text)


def main():
    token = os.environ["FG_GITHUB_ACCESS_TOKEN"]
    fetch_largest_repos('TheNewThinkTank', token)


if __name__ == "__main__":
    main()
