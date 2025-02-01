
import os
from unittest.mock import mock_open, patch
# from src.save_file_to_github import save_file_to_github
# from src.config import settings
from src.wily_to_md import (  # type: ignore
    read_and_filter_lines,
    convert_to_markdown,
    save_markdown_file,
    # wily_to_md,
)

# Sample data for testing
SAMPLE_INPUT = [
    "│ Header1 │ Header2 │\n",
    "│ ───     │ ───     │\n",
    "│ Data1   │ Data2   │\n",
    "│ Data3   │ Data4   │\n",
]

EXPECTED_FILTERED_LINES = [
    "│ Header1 │ Header2 │\n",
    "│ Data1   │ Data2   │\n",
    "│ Data3   │ Data4   │\n",
]

EXPECTED_MARKDOWN = (
    "| Header1 | Header2 |\n"
    "| --- | --- |\n"
    "| Data1   | Data2   |\n"
    "| Data3   | Data4   |\n"
)


def test_read_and_filter_lines():
    with patch("builtins.open", mock_open(read_data="".join(SAMPLE_INPUT))):
        filtered_lines = read_and_filter_lines("dummy_path.txt")
        assert filtered_lines == EXPECTED_FILTERED_LINES


def test_convert_to_markdown():
    md_str = convert_to_markdown(EXPECTED_FILTERED_LINES)
    assert md_str == EXPECTED_MARKDOWN


def test_save_markdown_file():
    mock_file_path = "output.md"
    with patch("builtins.open", mock_open()) as mocked_file:
        save_markdown_file(mock_file_path, EXPECTED_MARKDOWN)
        mocked_file.assert_called_once_with(mock_file_path, "w")
        mocked_file().write.assert_called_once_with(
            f"# {os.path.basename(mock_file_path).removesuffix('.md')}\n\n{EXPECTED_MARKDOWN}"
        )


# @patch("src.save_file_to_github.save_file_to_github")
# @patch("src.wily_to_md.save_markdown_file")
# @patch("src.wily_to_md.convert_to_markdown")
# @patch("src.wily_to_md.read_and_filter_lines")
# def test_wily_to_md(
#     mock_read_and_filter_lines,
#     mock_convert_to_markdown,
#     mock_save_markdown_file,
#     mock_save_file_to_github,
# ):
#     # Mock the return values
#     mock_read_and_filter_lines.return_value = EXPECTED_FILTERED_LINES
#     mock_convert_to_markdown.return_value = EXPECTED_MARKDOWN

#     # Call the function
#     wily_to_md("dummy_path-raw.txt")

#     # Assertions
#     mock_read_and_filter_lines.assert_called_once_with("dummy_path-raw.txt")
#     mock_convert_to_markdown.assert_called_once_with(EXPECTED_FILTERED_LINES)
#     mock_save_markdown_file.assert_called_once_with("dummy_path.txt", EXPECTED_MARKDOWN)
#     mock_save_file_to_github.assert_called_once_with(
#         settings["PROJECT_NAME"], "dummy_path.txt", EXPECTED_MARKDOWN.encode()
#     )
