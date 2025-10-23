import os
import requests
from pathlib import Path
from dotenv import load_dotenv
from rich.console import Console
import git

load_dotenv()
console = Console()

GITHUB_API = "https://api.github.com"
TOKEN = os.getenv("GITHUB_TOKEN")

def _get_repo_info(project_name: str) -> dict | None:
    """Return repo JSON if it exists, else None."""
    if not TOKEN:
        console.print("[bold red]Error:[/bold red] GITHUB_TOKEN missing from .env")
        return None

    url = f"{GITHUB_API}/repos/{os.getenv('GITHUB_USERNAME', '')}/{project_name}"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AutoDev-CLI"
    }
    try:
        r = requests.get(url, headers=headers, timeout=10)
        if r.status_code == 200:
            return r.json()
        return None
    except Exception:
        return None

def create_github_repo(project_name: str) -> str | None:
    """Create repo if it doesn't exist. Return clone URL or None."""
    if not TOKEN:
        console.print("[bold red]Error:[/bold red] GITHUB_TOKEN missing from .env")
        return None

    # 1. Check if repo already exists
    existing = _get_repo_info(project_name)
    if existing:
        clone_url = existing["clone_url"]
        console.print(f"[bold yellow]Warning:[/bold yellow] Repo already exists: {existing['html_url']}")
        console.print(f"   Using existing repo for push → {clone_url}")
        return clone_url

    # 2. Create new repo
    url = f"{GITHUB_API}/user/repos"
    headers = {
        "Authorization": f"token {TOKEN}",
        "Accept": "application/vnd.github.v3+json",
        "User-Agent": "AutoDev-CLI"
    }
    data = {
        "name": project_name,
        "private": False,
        "auto_init": False
    }

    try:
        r = requests.post(url, json=data, headers=headers, timeout=10)
        if r.status_code == 201:
            repo_data = r.json()
            console.print(f"[bold green]GitHub:[/bold green] Created new repo: {repo_data['html_url']}")
            return repo_data["clone_url"]
        else:
            msg = r.json().get("message", "Unknown error")
            console.print(f"[bold red]GitHub Error ({r.status_code}):[/bold red] {msg}")
            return None
    except Exception as e:
        console.print(f"[bold red]Network error:[/bold red] {e}")
        return None

def push_to_github(project_dir: Path, clone_url: str) -> bool:
    """Push using HTTPS with embedded token."""
    try:
        # ------------------------------------------------------------------
        # 1. Build a push-ready URL: https://<TOKEN>@github.com/user/repo.git
        # ------------------------------------------------------------------
        if not TOKEN:
            console.print("[bold red]Error:[/bold red] GITHUB_TOKEN missing – cannot push.")
            return False

        # clone_url is https://github.com/user/repo.git
        # → replace "https://" with "https://<TOKEN>@"
        push_url = clone_url.replace("https://", f"https://{TOKEN}@")

        repo = git.Repo(project_dir)

        # Create or update origin
        if "origin" in repo.remotes:
            origin = repo.remotes.origin
            origin.set_url(push_url)
        else:
            origin = repo.create_remote("origin", push_url)

        # Push
        origin.push(refspec="HEAD:main", set_upstream=True)
        console.print(f"[bold green]GitHub:[/bold green] Pushed to {clone_url}")
        return True

    except Exception as e:
        console.print(f"[bold yellow]Push failed:[/bold yellow] {e}")
        return False