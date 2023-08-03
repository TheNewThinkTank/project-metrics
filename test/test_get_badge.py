
from context import src
from src.get_badge import get_badge

repo_names = [
    "fitness-tracker",
    "world-maps",
    "workout-generator",
]

badge_names = [
    "size_badge",
    "ci_badge",
    "codecov_badge",
]


def test_get_badge():

    repo_name = repo_names[0]
    badge_name = badge_names[0]

    assert get_badge(repo_name, badge_name) == {
        "label": "GitHub repo size",
        "value": [
            "https://img.shields.io/github/repo-size/TheNewThinkTank/fitness-tracker?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size",
            "https://github.com/TheNewThinkTank/fitness-tracker/archive/refs/heads/main.zip",
        ]
    }
