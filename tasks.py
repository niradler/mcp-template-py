#!/usr/bin/env python3
"""Development tasks script for MCP template."""

import asyncio
import shutil
import subprocess
import sys
from pathlib import Path


def run_command(cmd: str, check: bool = True) -> int:
    """Run a shell command."""
    print(f"➤ {cmd}")
    return subprocess.run(cmd, shell=True, check=check).returncode


def task_install():
    """Install dependencies."""
    print("📦 Installing dependencies...")
    run_command("uv sync")
    print("✅ Dependencies installed")


def task_test():
    """Run tests."""
    print("🧪 Running tests...")
    run_command("uv run pytest tests/ -v")


def task_test_unit():
    """Run unit tests only."""
    print("🧪 Running unit tests...")
    run_command("uv run pytest tests/unit/ -v")


def task_test_e2e():
    """Run E2E tests only."""
    print("🧪 Running E2E tests...")
    run_command("uv run pytest tests/e2e/ -v")


def task_test_coverage():
    """Run tests with coverage."""
    print("🧪 Running tests with coverage...")
    run_command(
        "uv run pytest --cov=mcp_template --cov-report=html --cov-report=term")


def task_lint():
    """Run linting."""
    print("🔍 Running linters...")
    run_command("uv run ruff check src/ tests/")
    run_command("uv run mypy src/")


def task_format():
    """Format code."""
    print("🎨 Formatting code...")
    run_command("uv run black src/ tests/")
    run_command("uv run ruff check src/ tests/ --fix")


def task_run():
    """Run the server in stdio mode."""
    print("🚀 Starting MCP server (stdio)...")
    run_command("uv run mcp-template")


def task_run_http():
    """Run the server in HTTP mode."""
    print("🚀 Starting MCP server (HTTP)...")
    run_command("uv run mcp-template --transport http --port 8000")


def task_test_client():
    """Run the test client."""
    print("🧪 Running test client...")
    run_command("uv run python scripts/test_client.py")


def task_inspector():
    """Run MCP Inspector."""
    print("🔍 Starting MCP Inspector...")
    run_command("npx @modelcontextprotocol/inspector uv run mcp-template")


def task_examples():
    """Run usage examples."""
    print("📖 Running usage examples...")
    run_command("uv run python examples/usage_examples.py")


def task_clean():
    """Clean build artifacts."""
    print("🧹 Cleaning build artifacts...")

    paths_to_clean = [
        "__pycache__",
        ".pytest_cache",
        ".mypy_cache",
        ".coverage",
        "htmlcov",
        "dist",
        "build",
        "*.egg-info"
    ]

    for path in paths_to_clean:
        for p in Path(".").rglob(path):
            if p.is_dir():
                shutil.rmtree(p)
                print(f"  Removed {p}")
            elif p.is_file():
                p.unlink()
                print(f"  Removed {p}")


def task_dev_setup():
    """Setup development environment."""
    print("🛠️  Setting up development environment...")
    task_install()
    run_command("uv run pre-commit install", check=False)
    print("✅ Development environment ready!")


def task_help():
    """Show available tasks."""
    print("📋 Available tasks:")
    tasks = {
        "install": "Install dependencies",
        "test": "Run all tests",
        "test-unit": "Run unit tests only",
        "test-e2e": "Run E2E tests only",
        "test-coverage": "Run tests with coverage",
        "lint": "Run linting",
        "format": "Format code",
        "run": "Run server (stdio)",
        "run-http": "Run server (HTTP)",
        "test-client": "Run test client",
        "inspector": "Run MCP Inspector",
        "examples": "Run usage examples",
        "clean": "Clean build artifacts",
        "dev-setup": "Setup development environment",
        "help": "Show this help"
    }

    for task, description in tasks.items():
        print(f"  {task:<15} - {description}")


def main():
    """Main task runner."""
    if len(sys.argv) < 2:
        task_help()
        return

    task = sys.argv[1].replace("-", "_")
    task_func = globals().get(f"task_{task}")

    if task_func:
        try:
            task_func()
        except KeyboardInterrupt:
            print("\n❌ Task interrupted")
            sys.exit(1)
        except Exception as e:
            print(f"❌ Task failed: {e}")
            sys.exit(1)
    else:
        print(f"❌ Unknown task: {sys.argv[1]}")
        task_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
