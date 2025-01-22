
import os
from unittest.mock import Mock, patch
from src.util.get_gh_repos import get_gh_repos
# from github import Auth, Github


@patch("src.util.get_gh_repos.Github")
def test_get_gh_repos_with_default_values(mock_github):
    # Arrange
    # expected_username = "TheNewThinkTank"
    # expected_access_token = "mocked_access_token"
    repo_mock = Mock()
    user_mock = Mock()
    user_mock.get_repos.return_value = repo_mock

    # github_mock = Mock()
    # github_mock.get_user.return_value = user_mock

    mock_github.return_value.get_user.return_value = user_mock

    # with patch.dict(
    #     os.environ, {"PROJECT_METRICS_GITHUB_ACCESS_TOKEN": expected_access_token}
    # ):
    #     # Act
    #     result = get_gh_repos()
    result = get_gh_repos()

    # Assert
    assert result == repo_mock

    # github_mock.get_user.assert_called_once_with(expected_username)

    # Auth.Token.assert_called_once_with(
    #     os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
    # )
    # # Auth.Token.assert_called_once_with(expected_access_token)

    # Github.assert_called_once_with(auth=Auth.Token())


@patch("src.util.get_gh_repos.Github")
def test_get_gh_repos_with_custom_values(mock_github):
    # Arrange
    custom_username = "CustomUser"
    # custom_access_token = "custom_access_token"
    repo_mock = Mock()
    user_mock = Mock()
    user_mock.get_repos.return_value = repo_mock
    mock_github.return_value.get_user.return_value = user_mock

    # Act
    result = get_gh_repos(username=custom_username)

    # Assert
    assert result == repo_mock

    # github_mock.get_user.assert_called_once_with(custom_username)

    # Auth.Token.assert_called_once_with(
    #     os.environ["PROJECT_METRICS_GITHUB_ACCESS_TOKEN"]
    # )
    # # Auth.Token.assert_called_once_with(custom_access_token)

    # Github.assert_called_once_with(auth=Auth.Token())
