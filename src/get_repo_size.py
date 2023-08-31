"""_summary_
"""

from pprint import pprint as pp

from util.get_gh_repos import get_gh_repos  # type: ignore

repositories = get_gh_repos()

name_and_size = {repo.name: repo.size for repo in repositories}
pp(name_and_size)

# print(f"Repository Size: {repo.size} KB")
