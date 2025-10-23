import time
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

console = Console()

def show_spinner(message: str = "Creating project files…"):
    """Display spinner during file creation."""
    with Progress(SpinnerColumn(), TextColumn(f"[progress.description]{message}"), transient=True) as progress:
        task = progress.add_task(f"[cyan]{message}", total=None)
        time.sleep(0.3)  # Simulate work
        progress.update(task, completed=True)
    time.sleep(0.3)  # Pause for polish

def show_command_panel(command: str):
    """Display executing command in panel."""
    console.print(Panel(f"[bold blue]Executing:[/bold blue] {command}", border_style="blue"))
    time.sleep(0.3)

def show_created_table(items: list[tuple[str, str]]):
    """Display table of created items."""
    table = Table(title="Created Items", show_header=True, header_style="bold magenta")
    table.add_column("Item", style="cyan")
    table.add_column("Path", style="green")
    for name, path in items:
        table.add_row(name, path)
    console.print(table)
    time.sleep(0.3)

def show_optional_actions(include_tests: bool, license_type: str | None):
    """Display checks for optional features."""
    if include_tests:
        console.print("[bold cyan]✓ Added tests directory (`tests/`).[/bold cyan]")
        time.sleep(0.3)
    if license_type and license_type.upper() == "MIT":
        console.print("[bold cyan]✓ Added MIT license (`LICENSE`).[/bold cyan]")
        time.sleep(0.3)

def show_success(project_name: str):
    """Display final success message."""
    console.print(f"\n[bold green]Success:[/bold green] Created project '{project_name}' with default files.")

def show_git_success(msg: str):
    """Display Git success message."""
    console.print(f"[bold green]Git:[/bold green] {msg}")