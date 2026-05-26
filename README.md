# Simple Ticket CLI

A simple Ticket Manager CLI project built for TDD practice.

## Features

- Create ticket
- List tickets
- Show ticket details
- Update ticket status
- Store tickets in JSON
- Unit tests
- CLI integration tests

## Project Structure

```text
tickets/
  __init__.py
  __main__.py
  model.py
  service.py
  storage.py

tests/
  test_service.py
  test_cli.py
```

## Install

```bash
pip install pytest
```

## Run Tests

```bash
pytest
```

## Usage

Create a ticket:

```bash
python -m tickets create --title "Fix bug" --description "Fix login bug" --priority high --tags bug,backend
```

List tickets:

```bash
python -m tickets list
```

List by status:

```bash
python -m tickets list --status open
```

List by priority:

```bash
python -m tickets list --priority high
```

List by tag:

```bash
python -m tickets list --tag backend
```

Show one ticket:

```bash
python -m tickets show 1
```

Update ticket status:

```bash
python -m tickets update 1 --status done
```

## Valid Status

```text
open
doing
done
```

## Valid Priority

```text
low
medium
high
```

## TDD Workflow

This project follows:

```text
Failing test -> Small implementation -> Passing test -> Refactor
```

## Unit Tests

Unit tests check ticket logic:

- Create ticket
- Validate title
- Validate description
- Validate priority
- List tickets
- Get ticket
- Update ticket

## Integration Tests

Integration tests check CLI and JSON storage:

- Create ticket from CLI
- List ticket from CLI
- Show ticket from CLI
- Update ticket from CLI
- Handle empty JSON file
- Handle corrupted JSON file
