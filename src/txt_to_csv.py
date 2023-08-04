"""_summary_
"""

# import json
import pandas as pd  # type: ignore

# TODO: replace single with double quotes
# TODO: replace None values with double quotes


def txt_to_csv(in_file: str, sep: str = ",") -> None:
    """Create csv file from txt using Pandas.

    :param in_file: name of txt file
    :type in_file: str
    :param sep: _description_, defaults to ','
    :type sep: str, optional
    """

    # with open(in_file, 'r') as f:
    #     data = f.readlines()
    # data = [json.loads(d) for d in data]
    # df = pd.DataFrame.from_dict(data)

    df = pd.read_csv(in_file, sep=sep)

    df.to_csv(in_file.split(".")[0] + ".csv", index=False)


def main() -> None:
    # txt_to_csv('popular_repos.txt')
    # txt_to_csv('repos_wo_desc.txt')
    ...


if __name__ == "__main__":
    main()
