
import pytest
from unittest.mock import MagicMock, patch
from github.PaginatedList import PaginatedList
from github.Repository import Repository
from src.add_gha_wf import (  # type: ignore
    has_actions_workflow,
    make_gha_file_content,
    create_workflow,
    create_file,
    add_language_files,
    create_and_add_workflow,
    update_repos,
)


@pytest.fixture
def mock_repo():
    """Fixture to create a mock Repository object."""
    repo = MagicMock(spec=Repository)
    repo.name = "test-repo"
    repo.default_branch = "main"
    repo.description = "Test repository description"
    return repo


@pytest.fixture
def mock_workflows():
    """Fixture to create a mock PaginatedList of workflows."""
    workflow = MagicMock()
    workflow.name = "test-workflow"
    workflows = MagicMock(spec=PaginatedList)
    workflows.totalCount = 1
    workflows.__iter__.return_value = [workflow]
    return workflows


def test_has_actions_workflow_with_workflows(mock_repo, mock_workflows):
    """Test has_actions_workflow when workflows exist."""
    mock_repo.get_workflows.return_value = mock_workflows
    assert has_actions_workflow(mock_repo) is True


def test_has_actions_workflow_without_workflows(mock_repo):
    """Test has_actions_workflow when no workflows exist."""
    mock_repo.get_workflows.return_value.totalCount = 0
    assert has_actions_workflow(mock_repo) is False


@patch("builtins.open", create=True)
def test_make_gha_file_content(mock_open, mock_repo):
    """Test make_gha_file_content function."""
    mock_open.return_value.__enter__.return_value.read.return_value = (
        "{repo_name} {repo_branch}"
    )
    content = make_gha_file_content(mock_repo, language="Python")
    assert content == f"{mock_repo.name} {mock_repo.default_branch}"


# @patch("src.add_gha_wf.create_file")
# def test_create_workflow(mock_create_file, mock_repo):
#     """Test create_workflow function."""
#     file_content = "test-content"
#     create_workflow(mock_repo, file_content)

#     # Verify GitHub API calls
#     mock_repo.create_git_tree.assert_called_once()
#     mock_repo.create_git_commit.assert_called_once()
#     mock_repo.get_git_ref.return_value.edit.assert_called_once()


# @patch("builtins.open", create=True)
# def test_create_file_existing_file(mock_open, mock_repo):
#     """Test create_file when the file already exists."""
#     mock_open.return_value.__enter__.return_value.read.return_value = "{project-name}"
#     mock_repo.get_contents.side_effect = Exception("File already exists.")
#     mock_repo.name = "TestRepo"
#     mock_repo.description = "Test Description"

#     create_file(mock_repo, "pyproject.toml", "assets/Python/pyproject.txt")
#     mock_repo.create_file.assert_not_called()


# @patch("builtins.open", create=True)
# @patch("src.util.get_readme_format.get_readme_format", return_value="markdown")
# def test_create_file_new_file(mock_get_readme_format, mock_open, mock_repo):
#     """Test create_file when creating a new file."""
#     mock_open.return_value.__enter__.return_value.read.return_value = "{project-name} {description} {readme-format}"
#     mock_repo.get_contents.side_effect = Exception("File not found.")
#     mock_repo.name = "TestRepo"
#     mock_repo.description = "Test Description"

#     create_file(mock_repo, "pyproject.toml", "assets/Python/pyproject.txt")

#     expected_content = "TestRepo Test Description markdown"
#     mock_repo.create_file.assert_called_once_with(
#         "pyproject.toml",
#         "chore: add pyproject.toml",
#         expected_content,
#         branch=mock_repo.default_branch,
#     )


def test_add_language_files(mock_repo):
    """Test add_language_files function."""
    files = [("pyproject.toml", "assets/Python/pyproject.txt")]
    with patch("src.add_gha_wf.create_file") as mock_create_file:
        add_language_files(mock_repo, files)
        mock_create_file.assert_called_once_with(
            mock_repo, "pyproject.toml", "assets/Python/pyproject.txt"
        )


@patch("src.add_gha_wf.make_gha_file_content")
@patch("src.add_gha_wf.create_workflow")
def test_create_and_add_workflow(
    mock_create_workflow, mock_make_gha_file_content, mock_repo
):
    """Test create_and_add_workflow function."""
    mock_make_gha_file_content.return_value = "workflow-content"
    create_and_add_workflow(mock_repo, "Python")
    mock_create_workflow.assert_called_once()


# @patch("src.add_gha_wf.has_actions_workflow", return_value=False)
# @patch("src.add_gha_wf.add_language_files")
# @patch("src.add_gha_wf.create_and_add_workflow")
# @patch("src.REST.add_badge.update_repo")
# @patch("src.util.get_gh_repos.get_gh_repos")
# @patch("src.util.repo_has_lang.repo_has_lang", return_value=True)
# def test_update_repos(
#     mock_repo_has_lang,
#     mock_get_gh_repos,
#     mock_update_repo,
#     mock_create_and_add_workflow,
#     mock_add_language_files,
#     mock_has_actions_workflow,
#     mock_repo,
# ):
#     """Test update_repos function."""
#     mock_get_gh_repos.return_value = [mock_repo]
#     lang_files = [("pyproject.toml", "assets/Python/pyproject.txt")]
#     mock_repo.name = "TestRepo"
#     mock_repo.description = "Test Description"

#     update_repos("test-user", [mock_repo], "Python")

#     mock_add_language_files.assert_called_once_with(mock_repo, lang_files)
#     mock_update_repo.assert_called_once_with("test-user", mock_repo, badge_name="ci_badge")
#     mock_create_and_add_workflow.assert_called_once_with(mock_repo, "Python")
