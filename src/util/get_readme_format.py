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

    readme = repo.get_readme()

    if readme is None:
        return ""

    readme_format = readme.name.split(".")[-1]

    return readme_format
