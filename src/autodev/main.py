import typer
from pathlib import Path
from .core.project import create_project_files
from .core.git_ops import init_and_commit
from .core.github import create_github_repo, push_to_github
from .ui.output import (
    show_spinner, show_command_panel, show_created_table,
    show_optional_actions, show_success, show_git_success
)

app = typer.Typer()

@app.command()
def greet(name: str):
    """Say hello to someone with style 😎"""
    from rich.console import Console
    console = Console()
    console.print(f"👋 Hello, [bold green]{name}[/bold green]! Welcome to AutoDev 🚀")

@app.command()
def new(
    project_name: str,
    include_tests: bool = typer.Option(False, "--include-tests", help="Include a tests directory"),
    license: str = typer.Option(None, "--license", help="Add a license file (e.g., MIT)"),
    git_flag: bool = typer.Option(False, "--git", help="Initialize Git repository and commit files"),
    github: bool = typer.Option(False, "--github", help="Create GitHub repo and push code"),
):
    """Create a new project with the given name."""
    try:
        # Build command string
        cmd_parts = [f"autodev new {project_name}"]
        if include_tests: cmd_parts.append("--include-tests")
        if license: cmd_parts.append(f"--license {license}")
        if git_flag: cmd_parts.append("--git")
        if github: cmd_parts.append("--github")
        command = " ".join(cmd_parts)

        # Validate
        if not project_name.strip():
            from rich.console import Console
            Console().print("[bold red]Error:[/bold red] Project name cannot be empty.")
            raise typer.Exit(code=1)
        if any(c in project_name for c in r'<>:"/\|?*'):
            from rich.console import Console
            Console().print("[bold red]Error:[/bold red] Invalid characters in project name.")
            raise typer.Exit(code=1)

        project_dir = Path(project_name).resolve()
        if project_dir.exists():
            from rich.console import Console
            Console().print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists.")
            raise typer.Exit(code=1)

        # 1. Create files (with spinner)
        show_spinner()
        items = create_project_files(project_dir, project_name, include_tests, license)

        # 2. Show output
        show_command_panel(command)
        show_created_table(items)
        show_optional_actions(include_tests, license)

        # 3. Git (if flagged)
        git_msg = ""
        if git_flag:
            success = init_and_commit(project_dir)
            if success:
                git_msg = "Initialized repository and committed with message 'Initial commit: Project setup with AutoDev CLI'."
                show_git_success(git_msg)

        # 4. GitHub (if flagged)
        if github:
            if not git_flag:
                from rich.console import Console
                console = Console()
                console.print("[bold yellow]Warning:[/bold yellow] --github requires --git. Enabling local repo init...")
                init_and_commit(project_dir)
            remote_url = create_github_repo(project_name)
            if remote_url:
                push_to_github(project_dir, remote_url)

        # 5. Final success
        show_success(project_name)
        if git_msg and not github:
            show_git_success(git_msg)

    except typer.Exit:
        raise
    except PermissionError:
        from rich.console import Console
        Console().print("[bold red]Error:[/bold red] Permission denied while creating files.")
        raise typer.Exit(code=1)
    except Exception as e:
        from rich.console import Console
        Console().print(f"[bold red]Error:[/bold red] Unexpected error: {e}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()