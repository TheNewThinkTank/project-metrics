"""_summary_
"""

from src.save_file_to_github import save_file_to_github  # type: ignore

# TODO: sort by loc descending
# TODO: consolidate wily tables
# TODO: add repo-name to file-name


def wily_to_md(in_file) -> None:
    """_summary_

    :param in_file: _description_
    :type in_file: _type_
    """

    with open(in_file, 'r') as rf:
        lines = rf.readlines()
    lines = [
        line
        for line in lines
        if not any(
            x in line
            for x in ["───", "═══", "__init__"]
            )
        ]
    sep = "| --- | --- |\n"

    md_str = lines[0].replace("│", "|")
    md_str += sep
    for line in lines[1:]:
        md_str += line.replace("│", "|")

    local_file_path = in_file.replace("-raw", "")
    with open(local_file_path, "w") as wf:
        wf.write(f"# {local_file_path.split('/')[-1].removesuffix('.md')}\n\n" + md_str)

    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)


def main() -> None:
    basepath = "docs/project_docs/code-analysis/"
    files = [
        "wily-loc-raw",
        "wily-mi-raw",
        ]
    for file in files:
        in_file = basepath + file + '.md'
        wily_to_md(in_file)


if __name__ == "__main__":
    main()
