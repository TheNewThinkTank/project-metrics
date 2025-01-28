"""_summary_
"""

from dynaconf import Dynaconf  # type: ignore

settings = Dynaconf(
        settings_files=[".config/settings.toml"],
        # envvar_prefix="DYNACONF",
        environments=True,
        default_env="default",
        # load_dotenv=True,
        # envvar_for_dynaconf=".env",
    )

settings.setenv("default")  # Ensure the correct environment is active
# settings.validators.validate()
config_data = settings.as_dict()


def main() -> None:

    from pprint import pprint as pp

    pp(config_data)


if __name__ == "__main__":
    main()
