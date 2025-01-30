"""_summary_
"""

import os
from src.save_file_to_github import save_file_to_github  # type: ignore
from src.config import settings  # type: ignore

# TODO: sort by loc descending
# TODO: consolidate wily tables
# TODO: add repo-name to file-name


def read_and_filter_lines(in_file: str) -> list[str]:
    """Read lines from a file and filter out unwanted lines."""
    with open(in_file, 'r') as rf:
        lines = rf.readlines()
    return [
        line
        for line in lines
        if not any(x in line for x in ["───", "═══", "__init__"])
    ]


def convert_to_markdown(lines: list[str]) -> str:
    """Convert lines to markdown format."""
    sep = "| --- | --- |\n"
    md_str = lines[0].replace("│", "|")
    md_str += sep
    for line in lines[1:]:
        md_str += line.replace("│", "|")
    return md_str


def save_markdown_file(local_file_path: str, md_str: str) -> None:
    """Save markdown string to a file."""
    with open(local_file_path, "w") as wf:
        wf.write(f"# {os.path.basename(local_file_path).removesuffix('.md')}\n\n" + md_str)


def wily_to_md(in_file: str) -> None:
    """Convert a wily raw file to markdown and save it to GitHub.

    :param in_file: Path to the input file.
    :type in_file: str
    """
    lines = read_and_filter_lines(in_file)
    md_str = convert_to_markdown(lines)
    local_file_path = in_file.replace("-raw", "")
    save_markdown_file(local_file_path, md_str)

    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github(settings['PROJECT_NAME'], local_file_path, content)


def main() -> None:

    from pprint import pprint as pp

    # pp(settings)
    # pp(settings.keys())
    # pp(settings.values())

    pp(settings)

    basepath = f"{settings['DOCS_PATH']}/code-analysis/"
    files = [
        "wily-loc-raw",
        "wily-mi-raw",
        ]
    for file in files:
        in_file = basepath + file + '.md'
        wily_to_md(in_file)


if __name__ == "__main__":
    main()
