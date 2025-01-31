"""_summary_
"""

from dynaconf import Dynaconf  # type: ignore

settings = Dynaconf(
        settings_files=[".config/settings.toml"],
        # envvar_prefix="DYNACONF",
        environments=True,
        # default_env="default",
        load_dotenv=True,
        # envvar_for_dynaconf=".env",
    )

# settings.setenv("default")  # Ensure the correct environment is active
# settings.validators.validate()
# settings = settings.as_dict()


def main() -> None:

    from pprint import pprint as pp

    # pp(settings)
    pp(settings.platforms.to_dict())
    # pp(settings.platforms.github.badges)  # ['PLATFORMS']['github']['badges'])

    # pp(settings.platforms.github.badges.size_badge)

    # pp(settings.platforms.github.badges.size_badge.label)
    # pp(settings.platforms.github.badges.size_badge.value)

    # pp(settings.platforms.github.badges.ci_badge)
    # pp(settings.platforms.github.badges.codecov_badge)

if __name__ == "__main__":
    main()
