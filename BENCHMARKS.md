# Performance benchmarks

| type | total_wf_time | total_job_time | total_step_time | workflow_name | workflow_file | commit ID | workflow_run_number |
|-----|-----|-----|-----|-----|-----|-----|-----|
| serial | 2m 8s | 1m 57s | 1m 26s | `Project Metrics Workflow` | `wf.yml` | 5294192eb66667f978ad335a9cfd9278e90ff196 | 318 |
| parallel | 2m 3s | 1m 26s | 51s (25s of `get_gh_repo_names` job plus 26s for longest downstream processing job, `update_repos (AACT-Analysis)` | `Matrix strategy - Update GH repos` | `matrix_update_gh_repos.yml` | 5294192eb66667f978ad335a9cfd9278e90ff196 | 3 |
| threading | 1m 16s | 1m 6s | 33s | `Threading - Update GH repos` | `threading_update_gh_repos.yml` | 5294192eb66667f978ad335a9cfd9278e90ff196 | 2 |

## Notes
The main job to compare, `update_repos`:

GitHub Actions matrix strategy with workflow `matrix_update_gh_repos.yml`:<br>
one API requests per repo, very inefficient, but ~2 seconds per repo processing on average.
There is a large Parallel Execution Overhead due to process creation, context switching, and synchronization.
mainly useful if program is CPU bound, but in this case code is mostly IO bound.

## Conclusion
the comparison (processing 32 public GitHub repos) shows threading as the most optimal strategy,
and indicates that program execution is mostly IO bound.
