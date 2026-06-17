"""Run tests for all projects."""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Run pytest across all project directories."""
    projects_dir = Path(__file__).resolve().parent.parent / "projects"
    if not projects_dir.exists():
        print("❌ projects/ directory not found")
        sys.exit(1)

    test_dirs = [
        str(d) for d in projects_dir.iterdir() if d.is_dir() and (d / "tests").exists()
    ]
    if not test_dirs:
        print("No projects with tests found")
        return

    print(f"🧪 Running tests for {len(test_dirs)} project(s)...")
    subprocess.run([sys.executable, "-m", "pytest", *test_dirs, "-v"], check=True)


if __name__ == "__main__":
    main()
