"""_summary_
"""

import pytest
from src.get_badge import get_badge

testdata = [
    (
        "fitness-tracker",
        "size_badge",
        {
            "label": "GitHub repo size",
            "value": [
                "https://img.shields.io/github/repo-size/TheNewThinkTank/fitness-tracker?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size",
                "https://github.com/TheNewThinkTank/fitness-tracker/archive/refs/heads/main.zip",
            ],
        },
    ),
    (
        "world-maps",
        "ci_badge",
        {
            "label": "CI",
            "value": "https://github.com/TheNewThinkTank/world-maps/actions/workflows/wf.yml/badge.svg",
        },
    ),
    (
        "workout-generator",
        "codecov_badge",
        {
            "label": "codecov",
            "value": [
                "https://codecov.io/gh/TheNewThinkTank/workout-generator/branch/main/graph/badge.svg",
                "https://codecov.io/gh/TheNewThinkTank/workout-generator)",
            ],
        },
    ),
]


@pytest.mark.parametrize("repo,badge,expected", testdata)
def test_get_badge(repo, badge, expected):
    assert get_badge(repo, badge) == expected
