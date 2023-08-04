"""_summary_
"""

from github import Repository


def repo_has_lang(repo: Repository.Repository, lang: str) -> bool:
    """_summary_

    :param repo: _description_
    :type repo: Repository.Repository
    :param lang: _description_
    :type lang: str
    :return: _description_
    :rtype: bool
    """

    languages = repo.get_languages()

    if lang in languages:
        return True
    return False
