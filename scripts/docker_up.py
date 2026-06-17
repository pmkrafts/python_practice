"""Start shared infrastructure (Postgres + Redis)."""

import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Start Docker Compose services."""
    compose_file = Path(__file__).resolve().parent.parent / "docker" / "docker-compose.yml"
    if not compose_file.exists():
        print("❌ docker-compose.yml not found")
        sys.exit(1)

    print("🐳 Starting Postgres and Redis...")
    subprocess.run(
        ["docker-compose", "-f", str(compose_file), "up", "-d"],
        check=True,
    )
    print("✅ Postgres and Redis started")
    print("  Postgres: localhost:5432")
    print("  Redis:    localhost:6379")


if __name__ == "__main__":
    main()
