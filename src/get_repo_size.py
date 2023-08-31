"""_summary_
"""

# from pprint import pprint as pp

import matplotlib.pyplot as plt  # type: ignore
import seaborn as sns  # type: ignore

from save_file_to_github import save_file_to_github  # type: ignore
from util.get_gh_repos import get_gh_repos  # type: ignore

repositories = get_gh_repos()
name_and_size = {repo.name: repo.size for repo in repositories}

test_data = {
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

data = name_and_size  # test_data
data_by_size_desc = sorted(data.items(), key=lambda x: x[1], reverse=True)
# pp(data_by_size_desc)

names = [item[0] for item in data_by_size_desc]
sizes = [item[1] for item in data_by_size_desc]

sns.set(style="whitegrid")

# N largest repos
n = 8
names_largest = names[:n]
sizes_largest = sizes[:n]

# medium sized repos
names_medium = names[n : n + n]
sizes_medium = sizes[n : n + n]

# small repos
names_small = names[n + n : -n]
sizes_small = sizes[n + n : -n]

# smallest repos
names_smallest = names[-n:]
sizes_smallest = sizes[-n:]

plt.figure(figsize=(12, 6))
ax = sns.barplot(x=names_largest, y=sizes_largest, palette="pastel")
plt.xlabel("repo name")
plt.ylabel("repo size (KB)")
plt.title("Largest repos")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.tight_layout()
local_file_path = f"imgs/{n}_largest_repos.png"
plt.savefig(local_file_path)
plt.close()
with open(local_file_path, "rb") as file:
    content = file.read()
save_file_to_github("project-metrics", local_file_path, content)

plt.figure(figsize=(12, 6))
ax = sns.barplot(x=names_medium, y=sizes_medium, palette="pastel")
plt.xlabel("repo name")
plt.ylabel("repo size (KB)")
plt.title("Medium-sized repos")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.tight_layout()
local_file_path = f"imgs/{n}_medium_repos.png"
plt.savefig(local_file_path)
plt.close()
with open(local_file_path, "rb") as file:
    content = file.read()
save_file_to_github("project-metrics", local_file_path, content)

plt.figure(figsize=(12, 6))
ax = sns.barplot(x=names_small, y=sizes_small, palette="pastel")
plt.xlabel("repo name")
plt.ylabel("repo size (KB)")
plt.title("Small repos")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.tight_layout()
local_file_path = "imgs/small_repos.png"
plt.savefig(local_file_path)
plt.close()
with open(local_file_path, "rb") as file:
    content = file.read()
save_file_to_github("project-metrics", local_file_path, content)

plt.figure(figsize=(12, 6))
ax = sns.barplot(x=names_smallest, y=sizes_smallest, palette="pastel")
plt.xlabel("repo name")
plt.ylabel("repo size (KB)")
plt.title(f"Smallest repos")
ax.set_xticklabels(ax.get_xticklabels(), rotation=45, ha="right")
plt.tight_layout()
local_file_path = f"imgs/{n}_smallest_repos.png"
plt.savefig(local_file_path)
plt.close()
with open(local_file_path, "rb") as file:
    content = file.read()
save_file_to_github("project-metrics", local_file_path, content)
