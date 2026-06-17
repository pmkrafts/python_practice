"""Set up the development environment."""

import subprocess
import sys
from pathlib import Path


def run(cmd: list[str], *, cwd: Path | None = None) -> None:
    """Run a command and print it."""
    print("$ " + " ".join(cmd))
    subprocess.run(cmd, check=True, cwd=cwd)


def main() -> None:
    """Create venv, install deps, and copy .env example if needed."""
    repo_root = Path(__file__).resolve().parent.parent
    venv_dir = repo_root / ".venv"

    if not venv_dir.exists():
        print("📦 Creating virtual environment...")
        run([sys.executable, "-m", "venv", str(venv_dir)])

    # Determine pip path (Windows vs Unix)
    pip = venv_dir / "Scripts" / "pip.exe"
    if not pip.exists():
        pip = venv_dir / "bin" / "pip"

    print("📦 Upgrading pip...")
    run([str(pip), "install", "--upgrade", "pip"])

    print("📦 Installing dependencies...")
    requirements = repo_root / "requirements.txt"
    if requirements.exists():
        run([str(pip), "install", "-r", str(requirements)])
    else:
        print("⚠️ requirements.txt not found, skipping dependency install")

    if not (repo_root / ".env").exists() and (repo_root / ".env.example").exists():
        print("📝 Creating .env from .env.example...")
        (repo_root / ".env").write_text((repo_root / ".env.example").read_text())

    print("✅ Setup complete")
    print(f"Activate the environment: {venv_dir}")


if __name__ == "__main__":
    main()
