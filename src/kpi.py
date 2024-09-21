
import base64
import datetime
# from pathlib import Path
from pprint import pprint as pp
import subprocess
from typing import TypedDict

from pycodestyle import Checker, StyleGuide  # , StandardReport  # type: ignore

from save_file_to_github import save_file_to_github  # type: ignore
from util.get_gh_repo_content import get_gh_repo_py_files  # type: ignore


# class QuietReport(StandardReport):
class QuietReport(Checker.report_class):
    """Custom report to quietly count violations without printing errors."""

    def __init__(self, options):
        super().__init__(options)
        self.violations_count = 0

    def error(self, line_number, offset, text, check):
        self.violations_count += 1
        return super().error(line_number, offset, text, check)


class KPIDict(TypedDict):
    module: str
    lines: int
    pep8_violations: int


# def byte_to_str(byte_str) -> str:
#     # Utility function to decode byte string and strip whitespaces
#     return byte_str.decode("utf-8").strip()


# def get_metric(item: str, cmd: str) -> int:
#     metric = subprocess.check_output(cmd.format(item),
#                                      shell=True,
#                                      timeout=10
#                                     )
#     return int(byte_to_str(metric))


def get_kpi_data(files: list) -> dict:

    # Initialize counters and data storage
    file_count = 0
    # kpi_list = []
    kpi_list: list[KPIDict] = []

    style_guide = StyleGuide(quiet=True)

    # Iterate through Python files in the project directory
    # for item in project_path.glob("**/*.py"):  # Recursively search Python files
    for item in files:
        # if any(x in item.parts for x in (".venv", "__init__.py")):
        # if any(x in [".venv", "__init__.py"] for x in item.parts):
        if any(x in item.path for x in [".venv", "__init__.py"]):
            continue

        print(f"Processing: {item}")
        # if item.is_file() and not item.is_symlink():
        file_content = base64.b64decode(item.content).decode('utf-8')
        line_count = len(file_content.splitlines())

        if line_count == 0:
            print(f"Skipping empty file: {item.path}")
            continue

        # checker = Checker(lines=file_content.splitlines())
        # pep8_count = checker.check_all()

        # report = QuietReport(options={})
        report = QuietReport(style_guide.options)
        checker = Checker(lines=file_content.splitlines(), report=report)
        checker.check_all()
        pep8_count = report.violations_count

        # line_count = get_metric(item, "wc -l < {}")  # lines in the file
        # pep8_count = get_metric(
        #     item,
        #     "pycodestyle {} | wc -l"
        #     )  # PEP-8 violations
        # collect KPI data
        kpi_list.append({
            "module": item.path.split(".")[-1],  # str(item.relative_to(project_path)),
            "lines": line_count,
            "pep8_violations": pep8_count
        })
        file_count += 1
    total_line_count = sum([x["lines"] for x in kpi_list])
    total_pep8_violations = sum([x["pep8_violations"] for x in kpi_list])
    # Sort files by line count in descending order
    kpi_list_sorted = sorted(kpi_list, key=lambda x: x["lines"], reverse=True)

    return {"kpi_list_sorted": kpi_list_sorted,
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
        wf.write(f"# KPI\n\nlogging timestamp:\n{datetime.datetime.now()}\n\n")
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
    save_file_to_github(repo_name, local_file_path, content)


def main() -> None:

    repo_names = [
        "project-metrics",
        "N-body-simulations",
    ]
    repo_name = repo_names[1]

    files = get_gh_repo_py_files(repo_name=repo_name)
    file = files[0]
    file_content = base64.b64decode(file.content).decode('utf-8')
    # print(f"Content of {file.path}:")
    # print(file_content)

    # # TODO: setup project_path for cross-repo access
    # # project_path = Path(repo_name)
    # project_path = Path.cwd()  # if repo_name == "project-metrics" else Path(repo_name)
    # print(f"{project_path = }")
    basepath = "docs/project_docs/code-analysis/"
    local_file_path = f"{basepath}kpi_{repo_name}.md"
    # dir = project_path / basepath
    # dir.mkdir(parents=True, exist_ok=True)  # Create dir if it doesn't exist

    data = get_kpi_data(files)
    # print(data)
    write_kpi_md(repo_name, local_file_path, **data)


if __name__ == "__main__":
    main()
