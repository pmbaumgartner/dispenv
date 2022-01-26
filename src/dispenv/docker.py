import re
import shutil
from pathlib import Path
from subprocess import CompletedProcess, run
from typing import Any, Dict, List, NewType, Optional, Tuple

import srsly
from ._types import EnvData, URLString
from .checks import docker_installed, docker_running, run_docker_checks
from .consts import (
    DEVCONTAINER_TEMPLATE,
    DOCKERFILE_TEMPLATE,
    DOCKERFILE_TEMPLATE_WITH_REQUIREMENTS,
)
from .github import get_requirements_from_gist
from wasabi import msg


def create(env_data: EnvData):
    run_docker_checks()

    folder_path = Path(env_data.folder_name).resolve()
    msg.info(f"Creating Folder: {folder_path}")
    folder_path.mkdir(parents=True, exist_ok=False)

    msg.info(f"Creating Environment: {env_data.environment_name}")
    (folder_path / ".devcontainer").mkdir(exist_ok=False)
    (folder_path / ".devcontainer" / "devcontainer.json").write_text(
        DEVCONTAINER_TEMPLATE.format(environment_name=env_data.environment_name)
    )
    dockerfile_path = folder_path / "Dockerfile"
    if env_data.requirements_txt_gist:
        get_requirements_from_gist(env_data.requirements_txt_gist, folder_path)
        dockerfile_path.write_text(
            DOCKERFILE_TEMPLATE_WITH_REQUIREMENTS.format(
                python_version=env_data.python_version
            )
        )
    else:
        dockerfile_path.write_text(
            DOCKERFILE_TEMPLATE.format(python_version=env_data.python_version)
        )
    if env_data.options.build_image:
        msg.info("Building Docker Image")
        run(
            [
                "docker",
                "build",
                "-f",
                str(dockerfile_path),
                "-t",
                str(env_data.environment_name),
                str(folder_path),
            ]
        )
        msg.good("Built Docker Image")

    srsly.write_yaml(folder_path / ".dispenv.yaml", env_data.dict())


def cleanup(dispenv_data: Dict[str, Any]) -> None:
    msg.info("Removing Folder")
    folder_path = Path(dispenv_data["folder_name"]).resolve()
    run(["rm", "-rf", str(folder_path)], capture_output=True)
    msg.info("Stopping containers running image.")
    docker_ps_output = run(["docker", "ps", "-a"], capture_output=True)
    container_ids = get_containers_running_image(
        docker_ps_output, dispenv_data["environment_name"]
    )
    for cid in container_ids:
        run(["docker", "stop", cid], capture_output=True)
        run(["docker", "rm", cid], capture_output=True)

    msg.info("Removing image.")
    docker_ps_output = run(["docker", "images"], capture_output=True)
    for image in get_images(docker_ps_output, dispenv_data["environment_name"]):
        run(["docker", "rmi", image])
    msg.good("Cleanup Complete.")


def _imagecheck(input_image: str, reference_image: str):
    # vscode-dev container start with `vsc`
    input_image = input_image.strip()
    vsc_image = input_image.startswith(f"vsc-{reference_image}")
    default_image = input_image == reference_image
    return vsc_image or default_image


def get_containers_running_image(
    docker_ps_process: CompletedProcess, image_name: str
) -> List[str]:
    lines = [
        line.split()
        for line in docker_ps_process.stdout.decode().split("\n")[1:]
        if line.strip()
    ]
    container_ids_running_image = [
        line[0].strip() for line in lines if _imagecheck(line[1], image_name)
    ]
    return container_ids_running_image


def get_images(docker_images_process, image_name):
    lines = [
        line.split()
        for line in docker_images_process.stdout.decode().split("\n")[1:]
        if line.strip()
    ]
    images = [line[0].strip() for line in lines if _imagecheck(line[0], image_name)]
    return images
