# `dispenv` - Disposable Python Environments

⚠️ WIP  

Need to make an environment to work on a GitHub issue? Want to try out a new package and not leave the clutter of a virtual environment behind? `dispenv` is here to save the day! 

```
pip install git+https://github.com/pmbaumgartner/dispenv.git
```

To get started after install, type `dispenv create` in the parent folder of where you'd like your environment folder to go. Then, you'll be walked through a series of questions about your environment.

Example:

```
$ dispenv create

? What python version would you like to use? 3.8
? What type of virtual environment are you creating? (Use arrow keys)
 » conda
   docker (VSCode devcontainer)
? What should the folder be named? ba186b77-46bf-4506-9e8d-f9ba71377471
? What should the environment be named? ba186b77-46bf-4506-9e8d-f9ba71377471
? Paste link to a requirements.txt in a gist.  Optional https://gist.github.com/pmbaumgartner/af700cc2e009da40b1816cae66881e60
```

When you're done, `dispenv cleanup <folder>` will remove that folder and clean up any environment artifacts. 


**Features**:
- Supports [`conda`](https://docs.conda.io/projects/conda/en/latest/user-guide/concepts/environments.html#virtual-environments) and `docker` virtual environments
  - `docker` environments are setup to be run with VSCode as a [devcontainer](https://code.visualstudio.com/docs/remote/containers)
- When asked, if you paste a link to a GitHub Gist that contains a `requirements.txt`, `dispenv` will install those packages inside your environment after creation.
  - Requires the [GitHub CLI](https://cli.github.com/) to be installed.
  - Requires you to be authenticated through the GitHub CLI
- `dispenv cleanup` will automatically delete the `conda` environment or shut down and remove the containers and images if it's a `docker` environment.