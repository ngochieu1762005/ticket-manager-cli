from .model import Ticket


VALID_STATUS = ["open", "doing", "done"]
VALID_PRIORITY = ["low", "medium", "high"]


class TicketService:
    def __init__(self, storage):
        self.storage = storage

    def create(self, title, description, priority="medium", tags=None):
        if not title or title.strip() == "":
            raise ValueError("Title is required")

        if not description or description.strip() == "":
            raise ValueError("Description is required")

        if priority not in VALID_PRIORITY:
            raise ValueError("Invalid priority")

        tickets = self.storage.load()

        new_id = 1
        if tickets:
            new_id = max(ticket.id for ticket in tickets) + 1

        ticket = Ticket(
            id=new_id,
            title=title,
            description=description,
            status="open",
            priority=priority,
            tags=tags or [],
        )

        tickets.append(ticket)
        self.storage.save(tickets)

        return ticket

    def list(self, status=None, priority=None, tag=None):
        tickets = self.storage.load()

        if status:
            tickets = [ticket for ticket in tickets if ticket.status == status]

        if priority:
            tickets = [ticket for ticket in tickets if ticket.priority == priority]

        if tag:
            tickets = [ticket for ticket in tickets if tag in ticket.tags]

        return tickets

    def get(self, ticket_id):
        tickets = self.storage.load()

        for ticket in tickets:
            if ticket.id == ticket_id:
                return ticket

        raise ValueError("Ticket not found")

    def update(self, ticket_id, status):
        if status not in VALID_STATUS:
            raise ValueError("Invalid status")

        tickets = self.storage.load()

        for ticket in tickets:
            if ticket.id == ticket_id:
                ticket.status = status
                self.storage.save(tickets)
                return ticket

        raise ValueError("Ticket not found")
