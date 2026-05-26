from dataclasses import dataclass, asdict


@dataclass
class Ticket:
    id: int
    title: str
    description: str
    status: str
    priority: str
    tags: list[str]

    def to_dict(self):
        return asdict(self)

    @staticmethod
    def from_dict(data):
        return Ticket(
            id=data["id"],
            title=data["title"],
            description=data["description"],
            status=data.get("status", "open"),
            priority=data.get("priority", "medium"),
            tags=data.get("tags", []),
        )
