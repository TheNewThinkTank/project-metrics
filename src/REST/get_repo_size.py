"""_summary_
"""

# import requests


# def get_repo_size(username: str, repository: str) -> str | None:
#     """Fetch the size of a repository.

#     :param username: _description_
#     :type username: str
#     :param repository: _description_
#     :type repository: str
#     :return: _description_
#     :rtype: str | None
#     """

#     url = f'https://api.github.com/repos/{username}/{repository}'
#     response = requests.get(url)
#     if response.ok:
#         data = response.json()
#         return data['size']
#     return None
