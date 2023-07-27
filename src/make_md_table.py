

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

    max_lang = max(len(row.get('Python', [])) for row in data)

    for row in data:
        md_row = ""
        for _, v in row.items():
            if isinstance(v, list):

                lang = v if v else []

                lang += [''] * (max_lang - len(lang))

                sorted_lang = sorted(lang, key=lambda x: x != "")

                md_row += '| ' + '\n'.join(map(str, sorted_lang)) + ' '
            else:
                md_row += '| ' + str(v) + ' '
        md_table += md_row + '|' + '\n'

    # for row in data:
    #     md_row = ""
    #     for _, v in row.items():
    #         if isinstance(v, list):
    #             if v:
    #                 # Join list elements with '\n' as the delimiter
    #                 md_row += '| ' + '\n'.join(map(str, v)) + ' '
    #             else:
    #                 md_row += '| '  # Empty cell for an empty list
    #         else:
    #             md_row += '| ' + str(v) + ' '
    #     md_table += md_row + '|' + '\n'

    return md_table
