
import subprocess
import datetime
from pathlib import Path

from save_file_to_github import save_file_to_github  # type: ignore


def byte_to_str(byte_str) -> str:
    # Utility function to decode byte string and strip whitespaces
    return byte_str.decode("utf-8").strip()


def get_metric(item: str, cmd: str) -> int:
    metric = subprocess.check_output(cmd.format(item),
                                     shell=True,
                                     timeout=10
                                    )
    return int(byte_to_str(metric))


def get_kpi_data(repo_name: str, project_path) -> dict:
    print(repo_name)

    # Initialize counters and data storage
    file_count = 0
    kpi_list = []
    # Iterate through Python files in the project directory
    for item in project_path.glob("**/*.py"):  # Recursively search Python files
        if any(x in item.parts for x in (".venv", "__init__.py")):
            continue
        print(f"Processing: {item}")
        if item.is_file() and not item.is_symlink():
            line_count = get_metric(item, "wc -l < {}")  # lines in the file
            pep8_count = get_metric(
                item,
                "pycodestyle {} | wc -l"
                )  # PEP-8 violations
            # collect KPI data
            kpi_list.append({
                "module": str(item.relative_to(project_path)),
                "lines": line_count,
                "pep8_violations": pep8_count
            })
            file_count += 1
    total_line_count = sum(x["lines"] for x in kpi_list)
    total_pep8_violations = sum(x["pep8_violations"] for x in kpi_list)
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
    repo_name = repo_names[0]

    # project_path = Path(repo_name)
    project_path = Path.cwd()  # if repo_name == "project-metrics" else Path(repo_name)
    print(f"{project_path = }")
    basepath = "docs/project_docs/code-analysis/"
    local_file_path = f"{basepath}kpi_{project_path.name}.md"
    dir = project_path / basepath
    dir.mkdir(parents=True, exist_ok=True)  # Create dir if it doesn't exist

    data = get_kpi_data(repo_name, project_path)
    print(data)
    write_kpi_md(repo_name, local_file_path, **data)


if __name__ == "__main__":
    main()
