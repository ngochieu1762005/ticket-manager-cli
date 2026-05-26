import json
from pathlib import Path
from .model import Ticket


class JsonStorage:
    def __init__(self, path="tickets.json"):
        self.path = Path(path)

    def load(self):
        if not self.path.exists():
            return []

        try:
            with open(self.path, "r", encoding="utf-8") as file:
                data = json.load(file)
        except json.JSONDecodeError:
            raise ValueError("Corrupted JSON file")

        return [Ticket.from_dict(ticket) for ticket in data]

    def save(self, tickets):
        data = [ticket.to_dict() for ticket in tickets]

        with open(self.path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=2)
