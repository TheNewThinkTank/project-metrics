# Performance benchmarks

- serial (using for loops) with `wf.yml`: 58 seconds (getting GH repos with one single bulk API request)
- GitHub Actions matrix strategy with `matrix_update_gh_repos.yml`: 90 seconds (one API requests per repo, very inefficient)
  mainly useful if program is CPU bound, but in this case code is mostly IO bound.
- Threading with `threading_update_gh_repos.yml`:
