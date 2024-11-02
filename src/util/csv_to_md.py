# import csv


# def csv_to_md(in_file: str) -> None:
#     """Create a Markdown file from a csv file.

#     :param in_file: path to csv file
#     :type in_file: str
#     """

#     out_file = in_file.replace(".csv", ".md")
#     csv_dict = csv.DictReader(open(in_file, encoding="UTF-8"), delimiter=",")
#     list_of_rows = [dict_row for dict_row in csv_dict]
#     header = list(list_of_rows[0].keys())

#     md_string = " | "
#     for h in header:
#         md_string += h + " |"

#     md_string += "\n |"

#     for _ in range(len(header)):
#         md_string += "--- | "

#     md_string += "\n"

#     for row in list_of_rows:
#         md_string += " | "
#         for h in header:
#             md_string += row[h] + " | "
#         md_string += "\n"

#     with open(out_file, "w", encoding="UTF-8") as wf:
#         wf.write(md_string)


# def main() -> None:
#     # csv_to_md("popular_repos.csv")
#     # csv_to_md("repos_wo_desc.csv")
#     ...


# if __name__ == "__main__":
#     main()
