
from unittest.mock import Mock
from src.util.repo_has_lang import repo_has_lang


def test_repo_has_lang_with_supported_language():
    # Arrange
    repo_mock = Mock()
    repo_mock.get_languages.return_value = ["Python", "JavaScript", "Java"]
    lang = "Python"

    # Act
    result = repo_has_lang(repo_mock, lang)

    # Assert
    assert result is True


def test_repo_has_lang_with_unsupported_language():
    # Arrange
    repo_mock = Mock()
    repo_mock.get_languages.return_value = ["Python", "JavaScript", "Java"]
    lang = "C++"

    # Act
    result = repo_has_lang(repo_mock, lang)

    # Assert
    assert result is False


def test_repo_has_lang_with_empty_language_list():
    # Arrange
    repo_mock = Mock()
    repo_mock.get_languages.return_value = []
    lang = "Python"

    # Act
    result = repo_has_lang(repo_mock, lang)

    # Assert
    assert result is False
