"""_summary_
"""

import yaml


def load_config():
    with open(".config/config.yml", "r") as rf:
        data = yaml.safe_load(rf)
    return data


def main():

    data = load_config()

    # docs_path = data["docs_path"]

    # github_username = data["github_username"]
    # gitlab_username = data["gitlab_username"]
    # bitbucket_username = data["bitbucket_username"]

    # github_token = data["github_token"]
    # gitlab_token = data["gitlab_token"]
    # bitbucket_token = data["bitbucket_token"]

    # languages = data["languages"]
    # python_sample_repos = data["python_sample_repos"]
    # wf_path = data["wf_path"]

    print(data)


if __name__ == "__main__":
    main()
