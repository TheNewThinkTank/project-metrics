import requests


def group_repos_by_tag(username, token):
    url = f'https://api.github.com/users/{username}/repos'
    headers = {'Authorization': f'token {token}'}
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        repositories = response.json()

        tag_groups = {}

        for repo in repositories:
            name = repo['name']
            tags_url = repo['tags_url'].replace('{/repo}', '')
            tags_response = requests.get(tags_url, headers=headers)
            if tags_response.status_code == 200:
                tags = tags_response.json()
                for tag in tags:
                    tag_name = tag['name']
                    if tag_name in tag_groups:
                        tag_groups[tag_name].append(name)
                    else:
                        tag_groups[tag_name] = [name]

        for tag, repos in tag_groups.items():
            print(f'Tag: {tag}')
            for repo in repos:
                print(f'- {repo}')
            print()
    else:
        print(f'Request failed with status code {response.status_code}')
        print(response.text)


# Replace 'YOUR_USERNAME' and 'YOUR_TOKEN' with your GitHub username and personal access token
group_repos_by_tag('YOUR_USERNAME', 'YOUR_TOKEN')
