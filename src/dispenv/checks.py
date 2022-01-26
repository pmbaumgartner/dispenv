from subprocess import run
from functools import partial

run_capture = partial(run, capture_output=True)


def gh_cli_installed() -> bool:
    which_gh = run_capture(["which", "gh"])
    return which_gh.returncode == 0


def gh_cli_auth() -> bool:
    # You are not logged into any GitHub hosts. Run gh auth login to authenticate.
    gh_cli_auth = run_capture(["gh", "auth", "status"])
    needs_auth = (
        "You are not logged into any GitHub hosts" in gh_cli_auth.stdout.decode("utf-8")
    )
    return not needs_auth


def run_gh_cli_checks():
    if not gh_cli_installed():
        raise ValueError("GitHub CLI not installed.")
    if not gh_cli_auth():
        raise ValueError("Not Authenticated to GitHub through CLI. Run `gh auth login`")


def conda_installed() -> bool:
    which_conda = run_capture(["which", "conda"])
    return which_conda.returncode == 0


def run_conda_checks():
    if not conda_installed():
        raise ValueError(
            "Conda is not installed.\n"
            "https://docs.conda.io/projects/conda/en/latest/user-guide/install/download.html"
        )


def docker_installed() -> bool:
    which_docker = run_capture(["which", "docker"])
    return which_docker.returncode == 0


def docker_running() -> bool:
    docker_running = run_capture(["docker", "info"])
    return docker_running.returncode == 0


def run_docker_checks():
    if not docker_installed():
        raise ValueError("Docker is not installed.")
    if not docker_running():
        raise ValueError("Docker is not running.")
