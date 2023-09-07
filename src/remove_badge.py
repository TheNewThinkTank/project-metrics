"""Given one or more badges to remove,
and one or more repos to remove them from,
loop through all the repos and apply the removals.
-------------------------------------------------------------------------------------
EXAMPLES:

Cleanup cross-over badges, i.e. badges belonging to a different repo (e.g. repo: AACT-Analysis).

badges to remove:

![CI]
(https://github.com/TheNewThinkTank/AACT-Analysis/actions/workflows/wf.yml/badge.svg)

[![GitHub repo size]
(https://img.shields.io/github/repo-size/TheNewThinkTank/AACT-Analysis?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)]
(https://github.com/TheNewThinkTank/AACT-Analysis/archive/refs/heads/main.zip)

test on a few repos
and check that repo: 'AACT-Analysis' is unaffected.
-------------------------------------------------------------------------------------

TODO: perform above tasks in parallel.
"""

# from get_badge import get_badge  # type: ignore
# from util.get_gh_repos import get_gh_repos  # type: ignore

# badges_to_remove = [
# "CI",
# "GitHub repo size",
# ]
