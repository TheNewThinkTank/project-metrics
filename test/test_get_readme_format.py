
from unittest.mock import Mock
from src.util.get_readme_format import get_readme_format


def test_get_readme_format_with_valid_readme():
    # Arrange
    repo_mock = Mock()
    readme_mock = Mock()
    readme_mock.name = "README.md"
    repo_mock.get_readme.return_value = readme_mock

    # Act
    result = get_readme_format(repo_mock)

    # Assert
    assert result == "md"


def test_get_readme_format_with_missing_readme():
    # Arrange
    repo_mock = Mock()
    repo_mock.get_readme.return_value = None

    # Act
    result = get_readme_format(repo_mock)

    # Assert
    assert result == ""


def test_get_readme_format_with_empty_readme_name():
    # Arrange
    repo_mock = Mock()
    readme_mock = Mock()
    readme_mock.name = ""
    repo_mock.get_readme.return_value = readme_mock

    # Act
    result = get_readme_format(repo_mock)

    # Assert
    assert result == ""


def test_get_readme_format_with_complex_readme_name():
    # Arrange
    repo_mock = Mock()
    readme_mock = Mock()
    readme_mock.name = "project.readme.markdown"
    repo_mock.get_readme.return_value = readme_mock

    # Act
    result = get_readme_format(repo_mock)

    # Assert
    assert result == "markdown"
