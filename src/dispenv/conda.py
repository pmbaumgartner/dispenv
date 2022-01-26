import re
from pathlib import Path
from subprocess import run

import srsly
from wasabi import msg

from .checks import (
    run_conda_checks,
    run_gh_cli_checks,
)
from .github import get_requirements_from_gist
from ._types import EnvData
from typing import Dict, Any


def env_exists(environment_name) -> bool:
    env_regex: str = r"\b" + re.escape(environment_name) + r"\b"
    env_list: str = run(["conda", "info", "--envs"], capture_output=True).stdout.decode(
        "utf-8"
    )
    search_in = re.search(env_regex, env_list)
    return search_in is not None


def create(env_data: EnvData) -> None:
    run_conda_checks()
    if env_exists(env_data.environment_name):
        raise ValueError(f"Environment '{env_data.environment_name}' already exists")
    if Path(env_data.folder_name).exists():
        raise ValueError(f"Folder '{env_data.folder_name}' already exists.")

    folder_path = Path(env_data.folder_name).resolve()
    msg.info(f"Creating Folder: {folder_path}")
    folder_path.mkdir(parents=True, exist_ok=False)

    msg.info(f"Creating Environment: {env_data.environment_name}")
    with msg.loading("Creating..."):
        run(
            [
                "conda",
                "create",
                "-y",
                "-n",
                env_data.environment_name,
                f"python={env_data.python_version}",
            ],
            capture_output=True,
        )
    msg.good("\nEnvironment Created")

    if env_data.requirements_txt_gist:
        run_gh_cli_checks()
        msg.info(
            f"Downloading & Installing requirements.txt"
            f" from {env_data.requirements_txt_gist}"
        )
        requirements_txt_path = get_requirements_from_gist(
            env_data.requirements_txt_gist, folder_path
        )
        with msg.loading("Installing..."):
            run(
                [
                    "conda",
                    "run",
                    "-n",
                    env_data.environment_name,
                    "python",
                    "-m",
                    "pip",
                    "install",
                    "-r",
                    str(requirements_txt_path),
                ],
                capture_output=True,
            )
        msg.good("Packages Installed in Environment")

    srsly.write_yaml(folder_path / ".dispenv.yaml", env_data.dict())
    msg.good(
        f"Created Environment {env_data.environment_name} in {env_data.folder_name}"
    )


def cleanup(dispenv_data: Dict[str, Any]) -> None:
    msg.info("Removing Folder")
    folder_path = Path(dispenv_data["folder_name"]).resolve()
    run(["rm", "-rf", str(folder_path)], capture_output=True)
    msg.info("Removing Environment")
    run(
        ["conda", "env", "remove", "-n", dispenv_data["environment_name"]],
        capture_output=True,
    )
    msg.good("Cleanup Complete.")
