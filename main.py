import typer
from rich.console import Console

console = Console()
app = typer.Typer()

@app.command()
def greet(name: str):
    """Say hello to someone with style 😎"""
    console.print(f"👋 Hello, [bold green]{name}[/bold green]! Welcome to AutoDev 🚀")

if __name__ == "__main__":
    app()

