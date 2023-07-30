
import pandas as pd


def table(data: list[dict]) -> str:
    """Transform a list of dicts into a md table.

    :param data: list of dicts
    :type data: list[dict]
    :return: markdown table as a multi-line string
    :rtype: str
    """

    md_table = ""
    md_header = '| ' + ' | '.join(map(str, data[0].keys())) + ' |'
    md_header_sep = '|-----' * len(data[0].keys()) + '|'
    md_table += md_header + '\n'
    md_table += md_header_sep + '\n'

    for row in data:
        md_row = ""
        for _, v in row.items():
            # if isinstance(v, list):
            #     repos = v if v else []
            #     md_row += '| ' + ', '.join(map(str, repos)) + ' '
            # else:
            md_row += '| ' + str(v) + ' '
        md_table += md_row + '|' + '\n'

    return md_table


def table_from_nested(data: list[dict[str, list[str]]], debug=False) -> str | pd.DataFrame:
    """_summary_

    :param data: _description_
    :type data: list[dict[str, list[str]]]
    :param debug: _description_, defaults to False
    :type debug: bool, optional
    :return: _description_
    :rtype: str | pd.DataFrame
    """

    if not data:
        return pd.DataFrame()

    flattened_data = {}

    for item in data:
        for language, projects in item.items():
            flattened_data.setdefault(language, []).extend(projects)

    # Find the maximum length of projects across all languages
    max_length = max(len(projects) for projects in flattened_data.values())

    # Fill shorter project lists with empty strings to match the maximum length
    for projects in flattened_data.values():
        projects.extend([''] * (max_length - len(projects)))

    df = pd.DataFrame(flattened_data)

    if debug:
        return df

    return df.to_markdown()
