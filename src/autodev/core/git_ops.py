import git
from pathlib import Path
from rich.console import Console

console = Console()

def init_and_commit(project_dir: Path, commit_msg: str = "Initial commit: Project setup with AutoDev CLI") -> bool:
    """Initialize Git repo, stage files, and commit. Returns True on success."""
    try:
        repo = git.Repo.init(project_dir)
        
        # Fix: Convert working_dir (str) to Path for iterdir()
        working_dir = Path(repo.working_dir)
        repo.index.add([str(p) for p in working_dir.iterdir() if p.name != ".git"])
        
        repo.index.commit(commit_msg)
        
        console.print("\n[bold cyan]Git commands executed:[/bold cyan]")
        console.print("  git init")
        console.print("  git add .")
        console.print(f'  git commit -m "{commit_msg}"')
        
        return True
    except Exception as e:
        console.print(f"[bold yellow]Warning:[/bold yellow] Git init failed: {e}")
        console.print("    Files created – run `git init` manually.")
        return False