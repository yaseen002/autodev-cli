from pathlib import Path
from ..templates import (
    README_TEMPLATE, GITIGNORE_TEMPLATE, REQUIREMENTS_TEMPLATE,
    MAIN_PY_TEMPLATE, TEST_INIT_TEMPLATE, TEST_MAIN_TEMPLATE, MIT_LICENSE_TEMPLATE
)

def create_project_files(
    project_dir: Path,
    project_name: str,
    include_tests: bool = False,
    license_type: str | None = None
) -> list[tuple[str, str]]:
    """Create all project files and return list of (name, path) tuples."""
    items = []

    # Core files
    project_dir.mkdir(parents=True, exist_ok=False)
    items.append(("Directory", str(project_dir)))

    (project_dir / "README.md").write_text(README_TEMPLATE.format(project_name=project_name))
    items.append(("README.md", str(project_dir / "README.md")))

    (project_dir / ".gitignore").write_text(GITIGNORE_TEMPLATE)
    items.append((".gitignore", str(project_dir / ".gitignore")))

    (project_dir / "requirements.txt").write_text(REQUIREMENTS_TEMPLATE)
    items.append(("requirements.txt", str(project_dir / "requirements.txt")))

    (project_dir / "main.py").write_text(MAIN_PY_TEMPLATE.format(project_name=project_name))
    items.append(("main.py", str(project_dir / "main.py")))

    # Optional: Tests
    if include_tests:
        (project_dir / "tests").mkdir()
        items.append(("Directory", str(project_dir / "tests")))
        (project_dir / "tests" / "__init__.py").write_text(TEST_INIT_TEMPLATE)
        items.append(("tests/__init__.py", str(project_dir / "tests" / "__init__.py")))
        (project_dir / "tests" / "test_main.py").write_text(TEST_MAIN_TEMPLATE)
        items.append(("tests/test_main.py", str(project_dir / "tests" / "test_main.py")))

    # Optional: License
    if license_type and license_type.upper() == "MIT":
        (project_dir / "LICENSE").write_text(MIT_LICENSE_TEMPLATE.format(year=2025))
        items.append(("LICENSE", str(project_dir / "LICENSE")))

    return items