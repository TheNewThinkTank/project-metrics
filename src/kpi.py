
import subprocess
import datetime
from pathlib import Path

from save_file_to_github import save_file_to_github  # type: ignore

# count lines and PEP-8 violations in a file
line_count_cmd = "wc -l < {}"
pep8_count_cmd = "pycodestyle {} | wc -l"

project_path = Path.cwd()  # current project directory
basepath = "docs/project_docs/code-analysis/"
local_file_path = f"{basepath}kpi_{project_path.name}.md"

# Create dir if it doesn't exist
dir = project_path / basepath
dir.mkdir(parents=True, exist_ok=True)


def byte_to_str(byte_str):
    # Utility function to decode byte string and strip whitespaces
    return byte_str.decode("utf-8").strip()


def get_kpi_data():
    # Initialize counters and data storage
    file_count = 0
    total_line_count = 0
    total_pep8_violations = 0
    kpi_list = []
    # Iterate through Python files in the project directory
    for item in project_path.glob("**/*.py"):  # Recursively search Python files
        if ".venv" in item.parts:  # Skip the .venv directory
            continue
        print(f"Processing: {item}")
        if item.is_file() and not item.is_symlink():
            # count lines in the file
            lines = subprocess.check_output(line_count_cmd.format(item),
                                            shell=True,
                                            timeout=10
                                            )
            line_count = int(byte_to_str(lines))

            # count PEP-8 violations using pycodestyle
            pep8_violations = subprocess.check_output(pep8_count_cmd.format(item),
                                                      shell=True,
                                                      timeout=10
                                                      )
            pep8_count = int(byte_to_str(pep8_violations))

            # collect KPI data
            kpi_list.append({
                "module": str(item.relative_to(project_path)),
                "lines": line_count,
                "pep8_violations": pep8_count
            })

            # update counters
            file_count += 1
            total_line_count += line_count
            total_pep8_violations += pep8_count

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
