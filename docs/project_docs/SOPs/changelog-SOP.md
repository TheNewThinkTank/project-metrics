# Changelog Standards

Maintaining a changelog helps track changes between releases, improving transparency and usability for contributors and users. Follow these guidelines to ensure consistency:

1. Changelog File:

- Name the file `CHANGELOG.md`.
- Use the (Keep a Changelog)[https://keepachangelog.com/en/1.0.0/?spm=5aebb161.2ef5001f.0.0.14b05171VnhK3Q] format for structure.
- - Example:

```markdown
## [Unreleased]
- Added new feature X.
- Fixed issue Y.

## [1.0.1] - 2024-01-15
- Fixed bug Z.

## [1.0.0] - 2024-01-01
- Initial release.
```

2. Commit Message Standards:

- Use structured commit messages to facilitate automatic changelog generation.
- Adopt the Conventional Commits specification: `<type>(<scope>): <subject>`.
- - Types: `feat` (new feature), `fix` (bug fix), `docs` (documentation), `style` (formatting), `refactor`, `test`, etc.
- - Example: `feat(user): add login functionality`.

3. Tools for Standardization:

- Use **Commitizen** to enforce consistent commit messages.
- - Install Commitizen globally: `npm install -g commitizen cz-conventional-changelog`.
- - Configure your repository to use Commitizen:

```json
// package.json
{
  "config": {
    "commitizen": {
      "path": "./node_modules/cz-conventional-changelog"
    }
  }
}
```

Run `git cz` instead of `git commit` to interactively create standardized commits.

4. Automated Changelog Generation:

- Use tools like `standard-version` or `conventional-changelog` to automatically generate changelogs based on commit history.
- - Example with `standard-version`:

```bash
npm install --save-dev standard-version
npx standard-version
```

5. Release Process:

- Update the `CHANGELOG.md` file during each release.
- Include all relevant changes grouped by type (`Added`, `Changed`, `Deprecated`, `Removed`, `Fixed`, `Security`).
