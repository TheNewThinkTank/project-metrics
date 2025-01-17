"""_summary_
"""

import requests  # type: ignore


def graphql_post(username: str, token, query: str, limit=10):
    """_summary_

    :param username: _description_
    :type username: str
    :param token: _description_
    :type token: _type_
    :param query: _description_
    :type query: str
    """

    return requests.post(
        url="https://api.github.com/graphql",
        json={
            "query": query,
            "variables": {"login": username, "limit": limit}
            },
        headers={"Authorization": f"bearer {token}"}
    )
