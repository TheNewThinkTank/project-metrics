import json
import pandas as pd  # type: ignore

# TODO: replace single with double quotes
# TODO: replace None values with double quotes


def txt_to_csv(in_file: str) -> None:
    """Create csv file from txt using Pandas

    :param in_file: txt file with comma-delimited values
    :type in_file: str
    """

    with open(in_file) as f:
        data = f.readlines()

    data = [json.loads(d) for d in data]
    df = pd.DataFrame.from_dict(data)

    df.to_csv(in_file.split(".")[0] + ".csv", index=False)


def main() -> None:
    # txt_to_csv('popular_repos.txt')
    # txt_to_csv('repos_wo_desc.txt')
    ...


if __name__ == "__main__":
    main()
