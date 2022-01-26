from pathlib import Path
import srsly
import typer
from . import conda
from . import docker
from .questions import ask_environment_questions

app = typer.Typer()


@app.command()
def create():
    env_data = ask_environment_questions()
    if env_data.environment_type == "conda":
        conda.create(env_data)
    elif env_data.environment_type.startswith("docker"):
        docker.create(env_data)


@app.command()
def cleanup(
    dispenv_dir: Path = typer.Argument(
        ...,
        exists=True,
        file_okay=False,
        dir_okay=True,
        resolve_path=True,
    )
):
    resolved_path = dispenv_dir.resolve()
    dispenv_yaml = resolved_path / ".dispenv.yaml"
    if not dispenv_yaml.exists():
        raise ValueError(
            "No .dispenv.yaml file in this folder. "
            "Was this folder created by dispenv?"
        )
    dispenv_data = srsly.read_yaml(dispenv_yaml)
    if dispenv_data["environment_type"] == "conda":
        conda.cleanup(dispenv_data)
    elif dispenv_data["environment_type"] == "docker":
        docker.cleanup(dispenv_data)


if __name__ == "__main__":
    app()
