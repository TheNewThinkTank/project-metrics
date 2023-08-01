"""_summary_
"""

import os
from pprint import pprint as pp
import requests  # type: ignore

from save_file_to_github import save_file_to_github  # type: ignore
from make_md_table import table_from_nested  # type: ignore


def group_repos_by_language(username: str, token: str) -> list:
    """_summary_

    :param username: _description_
    :type username: str
    :param token: _description_
    :type token: str
    :return: _description_
    :rtype: list
    """

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
        language_groups = dict()  # type: ignore

        for repo in repositories:
            name = repo['name']
            language = repo['primaryLanguage']
            if language is not None:
                language_name = language['name']
                if language_name in language_groups:
                    language_groups[language_name].append(name)
                else:
                    language_groups[language_name] = [name]

        pp(language_groups)

        return [language_groups]

    else:
        print(f'Request failed with status code {response.status_code}')
        print(response.text)
        return []


def main() -> None:
    repo_name = 'project-metrics'
    lang_repos = group_repos_by_language('TheNewThinkTank',
                                         os.environ["FG_GITHUB_ACCESS_TOKEN"]
                                         )
    file_path = 'query-results/group_by_lang.md'
    file_content = table_from_nested(lang_repos)

    save_file_to_github(repo_name, file_path, file_content)


if __name__ == "__main__":
    main()
