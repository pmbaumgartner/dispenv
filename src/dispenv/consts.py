ALL_ISSUE_ELEMENTS = ",".join(
    [
        "assignees",
        "author",
        "body",
        "closed",
        "closedAt",
        "comments",
        "createdAt",
        "id",
        "labels",
        "milestone",
        "number",
        "projectCards",
        "reactionGroups",
        "state",
        "title",
        "updatedAt",
        "url",
    ]
)


HR = "————————"
HR_NEWLINE = f"\n\n{{HR}}\n\n"


DEVCONTAINER_TEMPLATE = """// For format details, see https://aka.ms/devcontainer.json. For config options, see the README at:
// https://github.com/microsoft/vscode-dev-containers/tree/v0.187.0/containers/python-3
{{
	"name": "{environment_name}",
	"build": {{
		"dockerfile": "../Dockerfile",
		"context": "../.",
	}},
	// Set *default* container specific settings.json values on container create.
	"settings": {{
		"python.pythonPath": "/usr/local/bin/python",
		"python.languageServer": "Pylance",
		"python.linting.enabled": true,
		"python.linting.pylintEnabled": true,
	}},
	// Add the IDs of extensions you want installed when the container is created.
	"extensions": [
		"ms-python.python",
		"ms-python.vscode-pylance",
	],
}}"""


DOCKERFILE_TEMPLATE = """FROM python:{python_version}

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1
"""


DOCKERFILE_TEMPLATE_WITH_REQUIREMENTS = """FROM python:{python_version}

WORKDIR /app
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

COPY requirements.txt .
RUN python -m pip install -r requirements.txt
"""
