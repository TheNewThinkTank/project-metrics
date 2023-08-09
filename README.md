![commit activity](https://img.shields.io/github/commit-activity/m/TheNewThinkTank/project-metrics)
[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/project-metrics?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/project-metrics/archive/refs/heads/main.zip)

# project-metrics

![CI](https://github.com/TheNewThinkTank/project-metrics/actions/workflows/wf.yml/badge.svg)
[![Documentation Status](https://readthedocs.org/projects/project-metrics/badge/?version=latest)](https://project-metrics.readthedocs.io/en/latest/?badge=latest)
[![codecov](https://codecov.io/gh/TheNewThinkTank/project-metrics/branch/main/graph/badge.svg)](https://codecov.io/gh/TheNewThinkTank/project-metrics)


Overview of projects and their health:

- [popular repos](query-results/popular_repos.md)<br>
- [repos without description](query-results/repos_wo_desc.md)<br>
- [repos grouped by language](query-results/group_by_lang.md)

## Current features

- CI health badge

- Sphinx auto doc, with doc hosting on readthedocs:<br>
[project-metrics](https://project-metrics.readthedocs.io/en/latest/)

- Automatically checking for updates using `Dependabot`:
  - `pip` (monthly)
  - `GitHub Actions` (weekly)

- GitHub Actions workflow `wf.yml`.<br>NB: as the repo updates itself, the only trigger should be `workflow_dispatch` to avoid recursive workflow invocation.
- The workflow contains the following jobs:
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

  - `Update-Repos`:
    - updates *all* GitHub repos:
      - All GitHub repos (including this one) get a repo size badge on top of their README<br>
        NB: does not affect the GitHub profile page, which is a special repo.
      - support for both `.md` and `.rst` files
      - All GitHub Python repos gets a GitHub Actions `.github/workflows/wf.yml`,
        as well as a *CI* badge on their README

the last job, `Update-Repos`, is further performance tested and a comparison of parallel and threading versions are
provided alongside the serial (for-loop) version:<br>
- [Performance Benchmarks](BENCHMARKS.md)

## Upcoming features
- cleanup script: `remove_badge.py`
- run all 3 benchmarks for same commit ID, perhaps using a single, resuable base workflow (poetry setup etc.)
- identify public repos without any README (e.g. 'web-application-jquery-and-bootstrap')
- security scannings with *bandit* (searching for API keys etc.)
- filter repos by number of users, descendingly
- getting codecov above 50 %
- improve & extend documentation on `readthedocs`
- alphabetic sorting of words in `config/.wordlist.txt`
- group by category (using tags), e.g. health (nutrition, fitness, athlete profiler)
- group by repo size, display largest and smallest repos
- group by created_at, display newest and oldest repos
- check if repos have tests
- if so, setup codecov badge on their README's
- if not, set up pytest, perhaps using `cookiecutter` / `cruft` or custom template
