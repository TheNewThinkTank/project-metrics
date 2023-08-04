![commit activity](https://img.shields.io/github/commit-activity/m/TheNewThinkTank/project-metrics)
[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/project-metrics?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/project-metrics/archive/refs/heads/main.zip)

# project-metrics

![CI](https://github.com/TheNewThinkTank/project-metrics/actions/workflows/wf.yml/badge.svg)

[![codecov](https://codecov.io/gh/TheNewThinkTank/project-metrics/branch/main/graph/badge.svg)](https://codecov.io/gh/TheNewThinkTank/project-metrics)


Overview of projects and their health

[popular repos](query-results/popular_repos.md)<br>
[repos without description](query-results/repos_wo_desc.md)<br>
[repos grouped by language](query-results/group_by_lang.md)

## Current features

- CI health badge

- Sphinx auto doc, with doc hosting on readthedocs:<br>
[project-metrics](https://project-metrics.readthedocs.io/en/latest/)

- Automatically checking for updates using `Dependabot`:
  - `pip` (monthly)
  - `GitHub Actions` (weekly)

- GitHub Actions workflow.<br>NB: as the repo updates itself, the only trigger should be `workflow_dispatch` to avoid recursive workflow invocation.
- The workflow contains two jobs:
  - `Qualify-Code`:
    - static type checking with `mypy`
    - code linting with `flake8` and `ruff`
    - spell checking of README
    - linting of YAML files
    - software complexity metrics with `wily`
    - unit tests with `pytest`
    - code coverage reporting
    - caching of `poetry` and `mypy` dependencies

  - `Get-Metrics`:
    - updates *this* repo's README (links above) with following projects metrics:
      - top 10 most popular GitHub repos, by star count
      - repos lacking any description, across `GitHub` and `GitLab`
      - repos grouped by programming language
    - updates *all* GitHub repos:
      - All GitHub repos (including this one) get a repo size badge on top of their README<br>
        NB: does not affect the GitHub profile page, which is a special repo.
      - support for both `.md` and `.rst` files
      - All GitHub Python repos gets a GitHub Actions `.github/workflows/wf.yml`,
        as well as a *CI* badge on their README

## Upcoming features
- security scannings with *bandit* (searching for API keys etc.)
- filter repos by number of users, descendingly
- get codecov at least above 50 % for this repo, ideally above 80 %
- improve documentation on `readthedocs`
- alphabetic sorting of words in `config/.wordlist.txt`
- group by category (using tags), e.g. health (nutrition, fitness, athlete profiler)
- group by repo size, display largest and smallest repos
- group by created_at, display newest and oldest repos
- check if repos have tests
- if so, setup codecov badge on their README's
- if not, set up pytest, perhaps using `cookiecutter` / `cruft` or custom template
- check if repos have GitHub Actions workflow
- if so, setup CI badge on their README's
- if not, set up workflow, using custom template
