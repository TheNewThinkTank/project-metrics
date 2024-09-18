
# import os
import subprocess
import datetime
from pathlib import Path

# count lines and PEP-8 violations in a file
line_count_cmd = "wc -l < {}"
pep8_count_cmd = "pycodestyle {} | wc -l"

# path setup
project_path = Path.cwd()  # current project directory
log_dir = project_path / "docs/project_docs/code-analysis"  # log directory
logfile_name = f"kpi_{project_path.name}.txt"  # file name from project dir
logfile = log_dir / logfile_name

# Create log dir if it doesn't exist
log_dir.mkdir(parents=True, exist_ok=True)


def byte_to_str(byte_str):
    # Utility function to decode byte string and strip whitespaces
    return byte_str.decode("utf-8").strip()


def generate_project_overview():
    # generate project overview with PEP-8 violations
    # Initialize counters and data storage
    file_count = 0
    total_line_count = 0
    total_pep8_violations = 0
    kpi_list = []

    # Write log header
    with logfile.open("a") as wf:
        wf.write(f"{'-' * 75}\n\n")
        wf.write(f"{'*' * 8}\tLogging timestamp: {datetime.datetime.now()}\t{'*' * 8}\n\n\n")
        wf.write(f"{'Module name':<40}{'Lines':>10}{'PEP-8 Violations':>20}\n\n")

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

    # Log data into the file
    with logfile.open("a") as wf:
        for kpi in kpi_list_sorted:
            wf.write(f"{kpi['module']:<40}{kpi['lines']:>10}{kpi['pep8_violations']:>20}\n")
        # Summary of the overview
        wf.write(f"\n\n{'*' * 14}\tPython scripts: {file_count}\t{'*' * 14}\n")
        wf.write(f"\n{'*' * 14}\tTotal code lines: {total_line_count}\t{'*' * 14}\n")
        wf.write(f"\n{'*' * 14}\tTotal PEP-8 violations: {total_pep8_violations}\t{'*' * 14}\n\n")


if __name__ == "__main__":
    generate_project_overview()
