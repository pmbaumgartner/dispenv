from pathlib import Path
from typing import Optional, Union
from uuid import uuid4

import questionary
from packaging import version

from ._types import Options, EnvData, URLString


def _ver_validate(version_string: str) -> bool:
    return (
        isinstance(version.parse(version_string), version.Version)
        and version_string.count(".") <= 2
    )


def _path_validate(folder_name: str) -> Union[str, bool]:
    return f"{folder_name} exists" if Path(folder_name).exists() else True


def _gist_validate(gist_url: URLString) -> bool:
    if gist_url.startswith("https://gist.github.com/") or gist_url == "":
        return True
    return False


def ask_environment_questions(default_name: Optional[str] = None) -> EnvData:
    python_version: str = questionary.text(
        "What python version would you like to use?",
        default="3.8",
        validate=_ver_validate,
    ).unsafe_ask()
    environment_type: str = questionary.select(
        "What type of virtual environment are you creating?",
        choices=[
            "conda",
            questionary.Choice("docker (VSCode devcontainer)", value="docker"),
        ],
    ).unsafe_ask()

    default_or_uuid: str = str(uuid4()) if default_name is None else default_name
    folder_name: str = questionary.text(
        "What should the folder be named?",
        default=default_or_uuid,
        validate=_path_validate,
    ).unsafe_ask()
    docker = environment_type == "docker"
    env_type_str = "image" if docker else "environment"
    environment_name: str = questionary.text(
        f"What should the {env_type_str} be named?", default=folder_name
    ).unsafe_ask()

    requirements_txt_gist = questionary.text(
        "Paste link to a requirements.txt in a gist.",
        instruction="Optional",
        default="",
        validate=_gist_validate,
    ).unsafe_ask()

    # ENV Specific
    # Docker
    build_image = (
        questionary.confirm("Build docker image?", default=False)
        .skip_if(environment_type != "docker", default=None)
        .ask()  # skip_if doesn't work with unsafe_ask
    )

    options = Options(build_image=build_image) if docker else None

    data = {
        "python_version": python_version,
        "folder_name": folder_name,
        "environment_type": environment_type,
        "environment_name": environment_name,
        "requirements_txt_gist": None
        if requirements_txt_gist == ""
        else requirements_txt_gist,
        "options": options,
    }
    env_data = EnvData(**data)

    return env_data


if __name__ == "__main__":
    e = ask_environment_questions()
    print(e)
