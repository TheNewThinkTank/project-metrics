import requests

def group_repos_by_language(username, token):
    url = 'https://api.github.com/graphql'
    headers = {'Authorization': f'bearer {token}'}
    query = '''
    query ($login: String!) {
      user(login: $login) {
        repositories(first: 100, orderBy: {field: NAME, direction: ASC}) {
          nodes {
            name
            primaryLanguage {
              name
            }
          }
        }
      }
    }
    '''
    variables = {'login': username}
    response = requests.post(url, json={'query': query, 'variables': variables}, headers=headers)

    if response.status_code == 200:
        data = response.json()
        repositories = data['data']['user']['repositories']['nodes']
        language_groups = {}

        for repo in repositories:
            name = repo['name']
            language = repo['primaryLanguage']
            if language is not None:
                language_name = language['name']
                if language_name in language_groups:
                    language_groups[language_name].append(name)
                else:
                    language_groups[language_name] = [name]

        for language, repos in language_groups.items():
            print(f'Language: {language}')
            for repo in repos:
                print(f'- {repo}')
            print()
    else:
        print(f'Request failed with status code {response.status_code}')
        print(response.text)

# Replace 'YOUR_USERNAME' and 'YOUR_TOKEN' with your GitHub username and personal access token
group_repos_by_language('YOUR_USERNAME', 'YOUR_TOKEN')
