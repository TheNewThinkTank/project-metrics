
import json
import pandas as pd

# TODO: replace single with double quotes
# TODO: replace None values with double quotes


def txt_to_csv(in_file: str) -> None:

    with open(in_file) as f:
        data = f.readlines()

    data = [json.loads(d) for d in data]
    df = pd.DataFrame.from_dict(data)
    # print(df)

    df.to_csv(in_file.split('.')[0] + '.csv',
              index=False
              )


def main():
    txt_to_csv('data/popular_repos.txt')
    txt_to_csv('data/repos_wo_desc.txt')


if __name__ == "__main__":
    main()
