import csv


def csv_to_md(in_file: str) -> None:

    out_file = in_file.replace(".csv", ".md")
    csv_dict = csv.DictReader(open(in_file, encoding="UTF-8"), delimiter=",")
    list_of_rows = [dict_row for dict_row in csv_dict]
    header = list(list_of_rows[0].keys())

    md_string = " | "
    for h in header:
        md_string += h + " |"

    md_string += "\n |"

    for _ in range(len(header)):
        md_string += "--- | "

    md_string += "\n"

    for row in list_of_rows:
        md_string += " | "
        for h in header:
            md_string += row[h] + " | "
        md_string += "\n"

    with open(out_file, "w", encoding="UTF-8") as wf:
        wf.write(md_string)


if __name__ == "__main__":
    csv_to_md("data/popular_repos.csv")
    csv_to_md("data/repos_wo_desc.csv")
