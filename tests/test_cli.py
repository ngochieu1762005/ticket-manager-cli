import subprocess
import sys


def run_cli(file_path, *args):
    return subprocess.run(
        [
            sys.executable,
            "-m",
            "tickets",
            "--file",
            str(file_path),
            *args,
        ],
        capture_output=True,
        text=True,
    )


def test_cli_create_ticket(tmp_path):
    file_path = tmp_path / "tickets.json"

    result = run_cli(
        file_path,
        "create",
        "--title",
        "CLI task",
        "--description",
        "Created by CLI",
        "--priority",
        "high",
        "--tags",
        "cli,test",
    )

    assert "Created ticket #1" in result.stdout
    assert "CLI task" in result.stdout
    assert file_path.exists()


def test_cli_list_ticket(tmp_path):
    file_path = tmp_path / "tickets.json"

    run_cli(
        file_path,
        "create",
        "--title",
        "List task",
        "--description",
        "For list command",
    )

    result = run_cli(file_path, "list")

    assert "List task" in result.stdout
    assert "[open]" in result.stdout


def test_cli_show_ticket(tmp_path):
    file_path = tmp_path / "tickets.json"

    run_cli(
        file_path,
        "create",
        "--title",
        "Show task",
        "--description",
        "For show command",
        "--tags",
        "demo",
    )

    result = run_cli(file_path, "show", "1")

    assert "Title: Show task" in result.stdout
    assert "Description: For show command" in result.stdout
    assert "Tags: demo" in result.stdout


def test_cli_update_ticket(tmp_path):
    file_path = tmp_path / "tickets.json"

    run_cli(
        file_path,
        "create",
        "--title",
        "Update task",
        "--description",
        "For update command",
    )

    result = run_cli(
        file_path,
        "update",
        "1",
        "--status",
        "done",
    )

    assert "Updated ticket #1" in result.stdout
    assert "Status: done" in result.stdout


def test_cli_empty_list(tmp_path):
    file_path = tmp_path / "tickets.json"

    result = run_cli(file_path, "list")

    assert "No tickets found" in result.stdout


def test_cli_corrupted_json(tmp_path):
    file_path = tmp_path / "tickets.json"
    file_path.write_text("{bad json", encoding="utf-8")

    result = run_cli(file_path, "list")

    assert "Corrupted JSON file" in result.stdout
