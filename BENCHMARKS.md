# Performance benchmarks

| type | workflowname | commit ID | workflow_run_number | total_wf_time | total_job_time | total_step_time |
|-----|-----|-----|-----|-----|-----|-----|
| serial | `wf.yml` |  |  |  |  |  |
| parallel | `matrix_update_gh_repos.yml` |  |  |  |  |  |
| threading | `threading_update_gh_repos.yml` |  |  |  |  |  |


## Notes

- serial (using for loops) with `wf.yml`, see run `#313`: 54 seconds (getting GH repos with one single bulk API request).

  `update_repos` JOB TOTAL TIME: 1 minute and 38 seconds<br>

  NB: should be subtracted 14 seconds for the extra `add GitHub Actions workflow to Python-based repos` step

- GitHub Actions matrix strategy with `matrix_update_gh_repos.yml`: 90 seconds overall
  (one API requests per repo, very inefficient), but ~2 seconds per repo processing on average.
  There is a large Parallel Execution Overhead due to process creation, context switching, and synchronization.
  mainly useful if program is CPU bound, but in this case code is mostly IO bound.

  `update_repos` JOB TOTAL TIME: 1 minute and 58 seconds

- Threading with `threading_update_gh_repos.yml`: 42 seconds to update all repos.

  `update_repos` JOB TOTAL TIME: 1 minute and 13 seconds

Conclusion: the comparison (processing 32 public GitHub repos) shows threading as the most optimal strategy, and indicates that program execution is mostly IO bound.
