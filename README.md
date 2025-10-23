### Auto DevOps CLI Tool Overview

- The Auto DevOps CLI Tool is a Python-based command-line utility designed to automate the setup of new Python projects, including folder creation, file generation, Git initialization, GitHub repository creation, and more, making it ideal for developers to quickly start projects with best practices.
- It supports flags like `--include-tests`, `--license MIT`, `--git`, and `--github` to customize setups, with secure integration for GitHub via personal access tokens (PATs).
- Key benefits include time-saving automation, reduced setup errors, and professional project structures, suitable for beginners or experienced developers aiming for efficiency.
- To use, install via pip (once published), set up a virtual environment, and configure a GitHub PAT with "repo" scope for full functionality.

#### Installation (SOON WELL BE AVAILABLE ON PIPI)
Install the tool using pip (assuming future PyPI publication):
```
pip install autodev-cli
```
For development, clone the repo from GitHub and install locally:
```
git clone https://github.com/yourusername/autodev-cli.git
cd autodev-cli
pip install -e .
```

#### Requirements
- **Python**: 3.9 or higher (tested on 3.12).
- **Dependencies**: typer, rich, gitpython, requests, python-dotenv (installed automatically via pip).
- **Git**: Installed on your system for local repo management (e.g., `sudo apt install git` on Ubuntu).
- **GitHub PAT**: Required for `--github` flag; generate with "repo" scope for creating and pushing to repositories.

#### GitHub PAT Setup
1. Go to GitHub > Settings > Developer settings > Personal access tokens > Generate new token (classic).
2. Select scopes: "repo" (full control for creating/pushing repos), "workflow" (for future CI/CD), "delete_repo" (optional).
3. Copy the token (ghp_...) and add to a `.env` file in your project root:
   ```
   GITHUB_TOKEN=ghp_XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
   ```
4. Ensure `.env` is in `.gitignore` to avoid committing secrets.

#### Usage
Run commands like:
```
autodev new my_project --include-tests --license MIT --git --github
```
- `--include-tests`: Adds a `tests/` folder with sample files.
- `--license MIT`: Adds MIT LICENSE file.
- `--git`: Initializes local Git repo and commits.
- `--github`: Creates remote GitHub repo and pushes.

The tool provides visual feedback with spinners, tables, and checks for created items.

#### How It's Helpful
- **Efficiency**: Automates repetitive setup, saving time for coding.
- **Best Practices**: Enforces standard structures (e.g., .gitignore, tests, license).
- **Scalability**: Modular for adding CI/CD (Phase 5) or packaging (Phase 6).
- **For PyPI**: Once published, users can pip install and use instantly for project bootstrapping, ideal for teams or open-source.

---

The Auto DevOps CLI Tool is a versatile Python utility that streamlines project initialization by automating directory creation, file templating, Git setup, and GitHub integration, reducing manual effort and ensuring consistent structures for Python development. It leverages libraries like Typer for CLI commands, Rich for enhanced terminal output, GitPython for local version control, and Requests for GitHub API interactions, all managed securely with python-dotenv for token handling. This makes it particularly useful for developers who frequently start new projects, as it enforces best practices like including .gitignore for Python-specific ignores (e.g., __pycache__/, .venv/), optional test directories, and licenses, while providing visual feedback through spinners, tables, and status checks to guide the user.

For installation, begin with Python 3.9+ in a virtual environment (`python -m venv .venv; source .venv/bin/activate`). Once published to PyPI, use `pip install autodev`; for now, clone the GitHub repo and install editable mode with `pip install -e .`. Dependencies are automatically handled, but ensure Git is installed system-wide for local repo operations. The tool's modular design (e.g., separate modules for project creation, Git ops, GitHub API, and UI output) allows easy extension, such as adding CI/CD in future phases.

To set up GitHub integration, generate a classic personal access token (PAT) with "repo" scope for creating and pushing to repositories, "workflow" for CI/CD workflows, and optionally "delete_repo" for cleanup. Add it to .env as `GITHUB_TOKEN=ghp_...`—this enables the `--github` flag to create remote repos via POST /user/repos and push code, with error handling for issues like existing repos (422) or permission denials (403). Without the token, the CLI gracefully falls back to local operations, printing warnings.

In usage, the `new` command is central: it validates the project name (no empty or invalid chars), creates files with a loading spinner for progress, displays a table of items (directories/files with paths), shows checks for optional features (e.g., ✓ Added tests directory, ✓ Added MIT license), executes Git init/add/commit if flagged (printing equivalent shell commands), and handles GitHub creation/push. For example, `autodev new my_project --include-tests --license MIT --git --github` automates the entire workflow, from local setup to remote deployment, with delays for polished display.

This tool is helpful for productivity: it saves time on boilerplate (e.g., manual git init/commit), reduces errors in setup (e.g., forgetting .gitignore), and promotes collaboration via instant GitHub repos. For PyPI publication, it's ready with pyproject.toml for packaging, making it accessible for teams or open-source contributors. Future phases can add YAML for CI (GitHub Actions) and PyPI deployment, turning it into a full DevOps starter.

**Key Citations:**
- [Creating a repository for the authenticated user - GitHub Docs](https://docs.github.com/en/rest/repos/repos#create-a-repository-for-the-authenticated-user)  
- [Managing your personal access tokens - GitHub Docs](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/managing-your-personal-access-tokens)  
- [GitPython Tutorial — GitPython 3.1.45 documentation](https://gitpython.readthedocs.io/en/stable/tutorial.html)  
- [Typer - https://typer.tiangolo.com/](https://typer.tiangolo.com/)  
- [The Python Rich Package: Unleash the Power of Console Text](https://realpython.com/python-rich-package/)