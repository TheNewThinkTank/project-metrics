"""_summary_
"""

from github import Repository


def get_readme_format(repo: Repository.Repository) -> str:
    """_summary_

    :param repo: _description_
    :type repo: Repository.Repository
    :return: _description_
    :rtype: str
    """

    readme_format = repo.get_readme().name.split(".")[-1]

    # try:
    #     readme_format = repo.get_readme().name.split(".")[-1]
    # except Exception as e:
    #     print(e)
    #     readme_format = ""

    return readme_format
