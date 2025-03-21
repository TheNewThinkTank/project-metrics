"""_summary_
"""

import base64
import datetime
import os
from typing import TypedDict, Any
from pycodestyle import Checker, BaseReport, StyleGuide  # type: ignore
from src.save_file_to_github import save_file_to_github  # type: ignore
from src.util.get_gh_repo_content import get_gh_repo_py_files  # type: ignore
from src.config import settings  # type: ignore


class QuietReport(BaseReport):
    """Custom report to quietly count violations without printing errors."""

    def __init__(self, options):
        super().__init__(options)
        self.violations_count = 0

    def error(self, line_number, offset, text, check):
        self.violations_count += 1
        return super().error(line_number, offset, text, check)


class KPIDict(TypedDict):
    """_summary_

    :param TypedDict: _description_
    :type TypedDict: _type_
    """
    module: str
    lines: int
    pep8_violations: int


def decode_file_content(item) -> list[str]:
    """Decode the base64 content of a file and split it into lines."""
    file_content = base64.b64decode(item.content).decode('utf-8')
    return file_content.splitlines()


def filter_non_empty_lines(lines: list[str]) -> list[str]:
    """Filter out empty lines from the list of lines."""
    return [line for line in lines if line.strip()]


def process_file(item, style_guide) -> KPIDict | None:
    """Process a single file to collect KPI data."""
    if any(x in item.path for x in [".venv", "__init__.py"]):
        return None

    print(f"Processing: {item}")
    lines = decode_file_content(item)
    line_count = len(lines)

    if line_count == 0 or all(line.strip() == "" for line in lines):
        print(f"Skipping empty or blank file: {item.path}")
        return None

    non_empty_lines = filter_non_empty_lines(lines)
    if not non_empty_lines:
        print(f"Skipping file with only blank lines: {item.path}")
        return None

    report = QuietReport(style_guide.options)
    checker = Checker(lines=non_empty_lines, report=report)
    checker.check_all()
    pep8_count = report.violations_count

    return {
        "module": item.path,
        "lines": line_count,
        "pep8_violations": pep8_count
    }


def get_kpi_data(files: list) -> dict[str, Any]:
    """Collect KPI data from a list of files.

    :param files: _description_
    :type files: list
    :return: _description_
    :rtype: dict[str, Any]
    """

    file_count = 0
    kpi_list: list[KPIDict] = []
    style_guide = StyleGuide(quiet=True)

    for item in files:
        kpi_data = process_file(item, style_guide)
        if kpi_data:
            kpi_list.append(kpi_data)
            file_count += 1

    total_line_count = sum(x["lines"] for x in kpi_list)
    total_pep8_violations = sum(x["pep8_violations"] for x in kpi_list)
    kpi_list_sorted = sorted(kpi_list, key=lambda x: x["lines"], reverse=True)

    return {
        "kpi_list_sorted": kpi_list_sorted,
        "file_count": file_count,
        "total_line_count": total_line_count,
        "total_pep8_violations": total_pep8_violations
    }


def write_kpi_md(
        repo_name: str,
        local_file_path: str,
        kpi_list_sorted: list,
        file_count: int,
        total_line_count: int,
        total_pep8_violations: int
        ) -> None:
    """_summary_

    :param kpi_list_sorted: _description_
    :type kpi_list_sorted: _type_
    :param file_count: _description_
    :type file_count: _type_
    :param total_line_count: _description_
    :type total_line_count: _type_
    :param total_pep8_violations: _description_
    :type total_pep8_violations: _type_
    """

    table_sep = "| --- | --- | --- |\n"
    with open(local_file_path, "w") as wf:
        wf.write(f"# {repo_name} KPIs\n\nlogging timestamp:\n{datetime.datetime.now()}\n\n")
        wf.write(
            "| Python scripts | total code lines | total PEP-8 violations |\n"
            + table_sep
            )
        wf.write(f"| {file_count}| {total_line_count} | {total_pep8_violations} |\n\n")

        wf.write(
            "| Module name | lines | PEP-8 Violations |\n"
            + table_sep
            )
        for kpi in kpi_list_sorted:
            wf.write(
                f"| `{kpi['module']:<40}` | {kpi['lines']:>10} | {kpi['pep8_violations']:>20} |\n"
                )

    with open(local_file_path, "rb") as file:
        content = file.read()
    # save_file_to_github(repo_name, local_file_path, content)
    save_file_to_github(settings['PROJECT_NAME'], local_file_path, content)


def main() -> None:

    repo_names = settings['PYTHON_SAMPLE_REPOS']

    basepath = f"{settings['DOCS_PATH']}/code-analysis/"

    token = os.environ.get(settings['GITHUB_TOKEN'])
    if not token:
        raise ValueError(
            f"{settings['GITHUB_TOKEN']} environment variable is not set"
            )

    for repo_name in repo_names:
        print(f"Processing KPIs for repo: {repo_name}")
        files = get_gh_repo_py_files(
            access_token=token,
            repo_name=repo_name
            )
        local_file_path = f"{basepath}kpi_{repo_name}.md"
        data = get_kpi_data(files)
        write_kpi_md(repo_name, local_file_path, **data)


if __name__ == "__main__":
    main()
