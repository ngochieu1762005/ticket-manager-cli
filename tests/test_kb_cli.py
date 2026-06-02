import os
import subprocess
import sys


def run_cli(*args):
    env = os.environ.copy()
    env["KB_CLIENT"] = "mock"

    return subprocess.run(
        [
            sys.executable,
            "-m",
            "tickets",
            *args,
        ],
        capture_output=True,
        text=True,
        env=env,
    )


def test_cli_kb_search():
    result = run_cli("kb", "search", "response", "--top-k", "3")

    assert result.returncode == 0
    assert "doc-001" in result.stdout
    assert "Customer Response Template" in result.stdout


def test_cli_kb_list():
    result = run_cli("kb", "list", "--node", "/templates/email", "--limit", "10")

    assert result.returncode == 0
    assert "doc-001" in result.stdout
    assert "/templates/email" in result.stdout


def test_cli_kb_retrieve():
    result = run_cli("kb", "retrieve", "doc-001")

    assert result.returncode == 0
    assert "ID: doc-001" in result.stdout
    assert "Customer Response Template" in result.stdout
    assert "Content:" in result.stdout


def test_cli_kb_add(tmp_path):
    file_path = tmp_path / "new-template.md"
    file_path.write_text("This is a new email template.", encoding="utf-8")

    result = run_cli(
        "kb",
        "add",
        "--file",
        str(file_path),
        "--path",
        "/templates/email",
        "--tags",
        "template,email",
        "--title",
        "New Email Template",
    )

    assert result.returncode == 0
    assert "Added document" in result.stdout
    assert "New Email Template" in result.stdout
