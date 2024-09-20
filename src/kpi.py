
import subprocess
import datetime
from pathlib import Path

from save_file_to_github import save_file_to_github  # type: ignore

project_path = Path.cwd()  # current project directory
basepath = "docs/project_docs/code-analysis/"
local_file_path = f"{basepath}kpi_{project_path.name}.md"

dir = project_path / basepath
dir.mkdir(parents=True, exist_ok=True)  # Create dir if it doesn't exist


def byte_to_str(byte_str):
    # Utility function to decode byte string and strip whitespaces
    return byte_str.decode("utf-8").strip()


def get_metric(item, cmd):
    metric = subprocess.check_output(cmd.format(item),
                                     shell=True,
                                     timeout=10
                                    )
    return int(byte_to_str(metric))


def get_kpi_data():
    # Initialize counters and data storage
    file_count = 0
    kpi_list = []
    # Iterate through Python files in the project directory
    for item in project_path.glob("**/*.py"):  # Recursively search Python files
        if ".venv" in item.parts:  # Skip the .venv directory
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


def write_kpi_md(kpi_list_sorted, file_count, total_line_count, total_pep8_violations):
    with open(local_file_path, "w") as wf:
        wf.write(f"# KPI\n\nlogging timestamp:\n{datetime.datetime.now()}\n\n")
        wf.write(
            "| Python scripts | total code lines | total PEP-8 violations |\n"
            "| -------------- | ---------------- | ---------------------- |\n"
            )
        wf.write(f"| {file_count}| {total_line_count} | {total_pep8_violations} |\n\n")

        wf.write(
            "| Module name | lines | PEP-8 Violations |\n"
            "| ----------- | ----- | ---------------- |\n"
            )
        for kpi in kpi_list_sorted:
            wf.write(
                f"| {kpi['module']:<40} | {kpi['lines']:>10} | {kpi['pep8_violations']:>20} |\n"
                )
    
    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)


if __name__ == "__main__":
    data = get_kpi_data()
    write_kpi_md(**data)
