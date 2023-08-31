"""_summary_
"""

from pprint import pprint as pp

import matplotlib.pyplot as plt
import seaborn as sns  # type: ignore

# from util.get_gh_repos import get_gh_repos  # type: ignore

# repositories = get_gh_repos()
# name_and_size = {repo.name: repo.size for repo in repositories}
# pp(name_and_size)
# print(f"Repository Size: {repo.size} KB")

data = {
    "AACT-Analysis": 326486,
    "AWS-recipes": 6,
    "Computation-Optimizations": 10,
    "DHC": 84,
    "Illustris-zoom-simulation": 2377,
    "IllustrisTNG": 16,
    "Machine-Learning-101": 195609,
    "N-body-simulations": 32691,
    "TheNewThinkTank": 7386,
    "advent-of-code": 909,
    "athlete": 24,
    "chess-explorer": 1115,
    "code-vault": 1152,
    "dark-matter-attractor": 55389,
    "fitness-tracker": 13573,
    "hypothesis-testing": 111,
    "image-models": 16581,
    "interactive-musicology": 2,
    "modelling-and-computations-Matlab": 11986,
    "nutrition-planner": 109,
    "performance": 107,
    "personal-finance": 56,
    "polylang": 145,
    "project-metrics": 581,
    "scRNA-seq": 107,
    "scrape-and-notify": 10,
    "security-scanner": 67,
    "sqlite-app": 45,
    "strava-insights": 401,
    "tomark": 9,
    "ts-snippets": 51,
    "twitter-novo": 1050,
    "web-application-jquery-and-bootstrap": 14761,
    "workout-generator": 102,
    "world-maps": 487,
}

data_by_size_desc = sorted(data.items(), key=lambda x: x[1], reverse=True)
pp(data_by_size_desc)

names = [item[0] for item in data_by_size_desc]
sizes = [item[1] for item in data_by_size_desc]

sns.set(style="whitegrid")
plt.figure(figsize=(12, 6))
ax = sns.barplot(x=names, y=sizes, palette="pastel")

plt.xlabel("repo name")
plt.ylabel("repo size (KB)")
plt.title("Repo Sizes")

# plt.xticks(rotation=45)
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.tight_layout()

# plt.show()
plt.savefig("imgs/repo_size.png")
