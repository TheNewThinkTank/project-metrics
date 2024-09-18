
from save_file_to_github import save_file_to_github  # type: ignore


def wily_to_md(in_file) -> None:
    with open(in_file, 'r') as rf:
        lines = rf.readlines()
    lines = [line for line in lines if not any(x in line for x in ["───", "═══"])]
    sep = "| --- | --- |\n"

    md_str = lines[0].replace("│", "|")  # + "\n"
    md_str += sep
    for line in lines[1:]:
        md_str += line.replace("│", "|")

    local_file_path = in_file.replace("-raw", "")
    with open(local_file_path, "w") as wf:
        wf.write(f"# {local_file_path.split('/')[-1].removesuffix('.md')}\n\n" + md_str)

    with open(local_file_path, "rb") as file:
        content = file.read()
    save_file_to_github("project-metrics", local_file_path, content)


if __name__ == "__main__":
    basepath = "docs/project_docs/code-analysis/"
    files = [
        "wily-loc-raw",
        "wily-mi-raw",
        ]
    for file in files:
        in_file = basepath + file + '.md'
        wily_to_md(in_file)
