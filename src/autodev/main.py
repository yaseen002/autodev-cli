import typer
from rich.console import Console
from pathlib import Path
from .templates import (
    README_TEMPLATE,
    GITIGNORE_TEMPLATE,
    REQUIREMENTS_TEMPLATE,
    MAIN_PY_TEMPLATE,
    TEST_INIT_TEMPLATE,
    TEST_MAIN_TEMPLATE,
    MIT_LICENSE_TEMPLATE,
)

console = Console()
app = typer.Typer()

@app.command()
def greet(name: str):
    """Say hello to someone with style 😎"""
    console.print(f"👋 Hello, [bold green]{name}[/bold green]! Welcome to AutoDev 🚀")

@app.command()
def new(
    project_name: str,
    include_tests: bool = typer.Option(False, "--include-tests", help="Include a tests directory"),
    license: str = typer.Option(None, "--license", help="Add a license file (e.g., MIT)"),
):
    """Create a new project with the given name."""
    try:
        # Validate project name
        if not project_name.strip():
            console.print("[bold red]Error:[/bold red] Project name cannot be empty.")
            raise typer.Exit(code=1)
        if any(c in project_name for c in r'<>:"/\|?*'):
            console.print("[bold red]Error:[/bold red] Invalid characters in project name.")
            raise typer.Exit(code=1)

        # Create project directory
        project_dir = Path(project_name)
        if project_dir.exists():
            console.print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists.")
            raise typer.Exit(code=1)
        project_dir.mkdir()

        # Create default files
        (project_dir / "README.md").write_text(README_TEMPLATE.format(project_name=project_name))
        (project_dir / ".gitignore").write_text(GITIGNORE_TEMPLATE)
        (project_dir / "requirements.txt").write_text(REQUIREMENTS_TEMPLATE)
        (project_dir / "main.py").write_text(MAIN_PY_TEMPLATE.format(project_name=project_name))

        # Create tests directory if flag is set
        if include_tests:
            (project_dir / "tests").mkdir()
            (project_dir / "tests" / "__init__.py").write_text(TEST_INIT_TEMPLATE)
            (project_dir / "tests" / "test_main.py").write_text(TEST_MAIN_TEMPLATE)

        # Add license file if specified
        if license and license.upper() == "MIT":
            (project_dir / "LICENSE").write_text(MIT_LICENSE_TEMPLATE.format(year=2025))

        console.print(f"[bold green]Success:[/bold green] Created project '{project_name}' with default files.")

    except typer.Exit:
        raise  # Re-raise typer.Exit to avoid catching it in the generic handler
    except PermissionError:
        console.print("[bold red]Error:[/bold red] Permission denied while creating files.")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] An unexpected error occurred: {str(e)}")
        raise typer.Exit(code=1)

if __name__ == "__main__":
    app()