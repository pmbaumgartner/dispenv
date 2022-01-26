import json
import shutil
from pathlib import Path
from subprocess import run
from typing import Any, Dict, Optional, NewType, Tuple

from .consts import ALL_ISSUE_ELEMENTS, HR_NEWLINE
from ._types import URLString


def get_requirements_from_gist(url: URLString, output_dir: Optional[Path] = None):
    if output_dir is None:
        output_dir = Path.cwd()
    requirements_txt_path = output_dir / "requirements.txt"
    if requirements_txt_path.exists():
        raise ValueError(f"requirements.txt already exists at {requirements_txt_path}")
    run(["gh", "gist", "clone", url, "--", "--depth=1"], capture_output=True)
    _id = url.split("/")[-1]
    cloned_requirements_txt_path = Path(_id) / "requirements.txt"
    shutil.copy(cloned_requirements_txt_path, requirements_txt_path)
    shutil.rmtree(_id)
    if requirements_txt_path.exists():
        return requirements_txt_path
    else:
        raise ValueError("reqirements.txt not found")


# The rest of this is WIP


def get_issue_json(url: URLString) -> Dict[str, Any]:
    result = run(
        ["gh", "issue", "view", url, "--json", ALL_ISSUE_ELEMENTS], capture_output=True
    )
    result_json = json.loads(result.stdout.decode("utf-8"))
    return result_json


def issue_to_md(issue_json: Dict[str, Any]) -> None:
    body = issue_json["body"]
    author = issue_json["author"]["login"]
    title = issue_json["title"]
    created_at = issue_json["createdAt"]
    state = issue_json["state"]
    original_issue_header_md = f"# {title} - {author}\n## {created_at} - {state}"
    original_issue_body_md = body
    original_issue_md = (
        f"{original_issue_header_md}\n\n{original_issue_body_md}{HR_NEWLINE}"
    )
    comments_md = HR_NEWLINE.join(
        [
            f"## {c['author']['login']} - {c['createdAt']}\n\n{c['body']}"
            for c in issue_json["comments"]
        ]
    )
    issue_md = original_issue_md + comments_md
    Path("issue.md").write_text(issue_md)


def parse_issue_url(url: str) -> Tuple[str, str, str]:
    parts = [p for p in url.split("/") if p]
    issue_id = parts[-1]
    repo = parts[-3]
    owner = parts[-4]
    return owner, repo, issue_id


def slugify_issue(url: str, prefix: str = "dispenv", sep: str = ".") -> str:
    return sep.join([prefix] + list(parse_issue_url(url)))
