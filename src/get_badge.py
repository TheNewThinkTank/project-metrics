"""_summary_
"""

from src.config import settings  # type: ignore


def get_badge(repo_name: str, badge_name: str):
    """_summary_

    :param repo: _description_
    :type repo: str
    :param badge_name: _description_
    :type badge_name: str
    :return: _description_
    :rtype: dict
    """

    # avoid modifying the original gh_badges dictionary, by making a copy
    # badge = gh_badges[badge_name].copy()

    github_badges = settings.platforms.github.badges  # settings['PLATFORMS']['github']['badges']
    badge = github_badges[badge_name].copy()

    if isinstance(badge.value, str):  # type: ignore
        badge.value = badge.value.replace("{repo}", repo_name)  # type: ignore

    elif isinstance(badge.value, list):  # type: ignore
        badge.value = [
            url.replace("{repo}", repo_name)  # type: ignore
            for url in badge.value  # type: ignore
        ]  # type: ignore

    # print(f"badge from get_badge: {badge}")

    return badge


if __name__ == "__main__":

    from pprint import pprint as pp

    pp(settings)
    # pp(settings.platforms.github.badges)
    # pp(settings['PLATFORMS']['github']['badges']['size_badge'])
    # pp(settings['PLATFORMS']['github']['badges']['ci_badge'])
