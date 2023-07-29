[![GitHub repo size](https://img.shields.io/github/repo-size/TheNewThinkTank/project-metrics?style=flat&logo=github&logoColor=whitesmoke&label=Repo%20Size)](https://github.com/TheNewThinkTank/project-metrics/archive/refs/heads/main.zip)
# project-metrics

![CI](https://github.com/TheNewThinkTank/project-metrics/actions/workflows/wf.yml/badge.svg)

<!-- [![codecov](https://codecov.io/gh/TheNewThinkTank/project-metrics/branch/main/graph/badge.svg?token=CKAX4A3JQF)](https://codecov.io/gh/TheNewThinkTank/project-metrics) -->


Overview of projects and their health

[popular repos](query-results/popular_repos.md)<br>
[repos without description](query-results/repos_wo_desc.md)<br>
[repos grouped by language](query-results/group_by_lang.md)

## Current features
- GitHub Actions workflow.<br>NB: as the repo updates itself, the only trigger should be `workflow_dispatch` to avoid recursive workflow invocation.
- GitHub Actions updates this repo's README (links above) with following projects metrics:
  - top 10 most popular GitHub repos, by star count
  - repos lacking any description, across GitHub and GitLab
  - repos grouped by programming language
- All GitHub repos (including this one) get a repo size badge on top of their README<br>
  NB: does not affect the GitHub profile page, which is a special repo.
  - support for both `.md` and `.rst` files

## Upcoming features
- group by category (using tags), e.g. health (nutrition, fitness, athlete profiler)
- group by repo size, display largest and smallest repos
- group by created_at, display newest and oldest repos
