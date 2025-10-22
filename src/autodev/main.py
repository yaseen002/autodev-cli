import typer
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from pathlib import Path
import git
import time                     # <-- NEW
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
    """Say hello to someone with style"""
    console.print(f"Hello, [bold green]{name}[/bold green]! Welcome to AutoDev")


@app.command()
def new(
    project_name: str,
    include_tests: bool = typer.Option(False, "--include-tests", help="Include a tests directory"),
    license: str = typer.Option(None, "--license", help="Add a license file (e.g., MIT)"),
    git_flag: bool = typer.Option(False, "--git", help="Initialize Git repository and commit files"),
):
    """Create a new project with the given name."""
    try:
        # ---------- Build command string ----------
        command = f"autodev new {project_name}"
        if include_tests:
            command += " --include-tests"
        if license:
            command += f" --license {license}"
        if git_flag:
            command += " --git"

        # ---------- Validate ----------
        if not project_name.strip():
            console.print("[bold red]Error:[/bold red] Project name cannot be empty.")
            raise typer.Exit(code=1)
        if any(c in project_name for c in r'<>:"/\|?*'):
            console.print("[bold red]Error:[/bold red] Invalid characters in project name.")
            raise typer.Exit(code=1)

        project_dir = Path(project_name).resolve()
        if project_dir.exists():
            console.print(f"[bold red]Error:[/bold red] Directory '{project_name}' already exists.")
            raise typer.Exit(code=1)

        # ---------- 1. Loading spinner ----------
        created_items = []
        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        ) as progress:
            task = progress.add_task("[cyan]Creating project files…", total=None)

            project_dir.mkdir(parents=True, exist_ok=False)
            created_items.append(("Directory", str(project_dir)))

            (project_dir / "README.md").write_text(README_TEMPLATE.format(project_name=project_name))
            created_items.append(("README.md", str(project_dir / "README.md")))

            (project_dir / ".gitignore").write_text(GITIGNORE_TEMPLATE)
            created_items.append((".gitignore", str(project_dir / ".gitignore")))

            (project_dir / "requirements.txt").write_text(REQUIREMENTS_TEMPLATE)
            created_items.append(("requirements.txt", str(project_dir / "requirements.txt")))

            (project_dir / "main.py").write_text(MAIN_PY_TEMPLATE.format(project_name=project_name))
            created_items.append(("main.py", str(project_dir / "main.py")))

            if include_tests:
                (project_dir / "tests").mkdir()
                created_items.append(("Directory", str(project_dir / "tests")))
                (project_dir / "tests" / "__init__.py").write_text(TEST_INIT_TEMPLATE)
                created_items.append(("tests/__init__.py", str(project_dir / "tests" / "__init__.py")))
                (project_dir / "tests" / "test_main.py").write_text(TEST_MAIN_TEMPLATE)
                created_items.append(("tests/test_main.py", str(project_dir / "tests" / "test_main.py")))

            if license and license.upper() == "MIT":
                (project_dir / "LICENSE").write_text(MIT_LICENSE_TEMPLATE.format(year=2025))
                created_items.append(("LICENSE", str(project_dir / "LICENSE")))

            progress.update(task, completed=True)

        # tiny pause – feels professional
        time.sleep(0.3)

        # ---------- 2. Show command & table ----------
        console.print(Panel(f"[bold blue]Executing:[/bold blue] {command}", border_style="blue"))
        time.sleep(0.3)

        table = Table(title="Created Items", show_header=True, header_style="bold magenta")
        table.add_column("Item", style="cyan")
        table.add_column("Path", style="green")
        for name, path in created_items:
            table.add_row(name, path)
        console.print(table)
        time.sleep(0.3)

        # ---------- 3. Optional actions ----------
        if include_tests:
            console.print("[bold cyan]Checkmark Added tests directory (`tests/`).")
            time.sleep(0.3)
        if license and license.upper() == "MIT":
            console.print("[bold cyan]Checkmark Added MIT license (`LICENSE`).")
            time.sleep(0.3)

        # ---------- 4. Git ----------
        git_status = ""
        if git_flag:
            try:
                repo = git.Repo.init(project_dir)
                repo.index.add([str(p) for p in project_dir.iterdir() if p.name != ".git"])
                commit_msg = "Initial commit: Project setup with AutoDev CLI"
                repo.index.commit(commit_msg)

                console.print("\n[bold cyan]Git commands executed:[/bold cyan]")
                console.print("  git init")
                console.print("  git add .")
                console.print(f'  git commit -m "{commit_msg}"')
                time.sleep(0.3)

                git_status = f"Initialized repository and committed with message '{commit_msg}'."
            except Exception as e:
                console.print(f"[bold yellow]Warning:[/bold yellow] Git init failed: {e}")
                console.print("    Files were created – run `git init` manually later.")
                git_status = ""

        # ---------- 5. Final success ----------
        console.print(f"\n[bold green]Success:[/bold green] Created project '{project_name}' with default files.")
        if git_status:
            console.print(f"[bold green]Git:[/bold green] {git_status}")

    except typer.Exit:
        raise
    except PermissionError:
        console.print("[bold red]Error:[/bold red] Permission denied while creating files.")
        raise typer.Exit(code=1)
    except Exception as e:
        console.print(f"[bold red]Error:[/bold red] Unexpected error: {e}")
        raise typer.Exit(code=1)


if __name__ == "__main__":
    app()