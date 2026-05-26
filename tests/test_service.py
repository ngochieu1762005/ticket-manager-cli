import pytest
from tickets.service import TicketService


class FakeStorage:
    def __init__(self):
        self.data = []

    def load(self):
        return self.data

    def save(self, tickets):
        self.data = tickets


def test_create_ticket_success():
    storage = FakeStorage()
    service = TicketService(storage)

    ticket = service.create(
        title="Fix bug",
        description="Fix login bug",
        priority="high",
        tags=["bug"],
    )

    assert ticket.id == 1
    assert ticket.title == "Fix bug"
    assert ticket.description == "Fix login bug"
    assert ticket.status == "open"
    assert ticket.priority == "high"
    assert ticket.tags == ["bug"]


def test_create_ticket_auto_id():
    storage = FakeStorage()
    service = TicketService(storage)

    ticket1 = service.create("Task 1", "Description 1")
    ticket2 = service.create("Task 2", "Description 2")

    assert ticket1.id == 1
    assert ticket2.id == 2


def test_create_ticket_without_title_should_fail():
    storage = FakeStorage()
    service = TicketService(storage)

    with pytest.raises(ValueError):
        service.create("", "Description")


def test_create_ticket_without_description_should_fail():
    storage = FakeStorage()
    service = TicketService(storage)

    with pytest.raises(ValueError):
        service.create("Task", "")


def test_create_ticket_with_invalid_priority_should_fail():
    storage = FakeStorage()
    service = TicketService(storage)

    with pytest.raises(ValueError):
        service.create("Task", "Description", priority="urgent")


def test_list_ticket_by_status():
    storage = FakeStorage()
    service = TicketService(storage)

    ticket1 = service.create("Task 1", "Description 1")
    ticket2 = service.create("Task 2", "Description 2")

    service.update(ticket2.id, "done")

    result = service.list(status="done")

    assert len(result) == 1
    assert result[0].id == ticket2.id


def test_list_ticket_by_priority():
    storage = FakeStorage()
    service = TicketService(storage)

    service.create("Task 1", "Description 1", priority="low")
    service.create("Task 2", "Description 2", priority="high")

    result = service.list(priority="high")

    assert len(result) == 1
    assert result[0].title == "Task 2"


def test_list_ticket_by_tag():
    storage = FakeStorage()
    service = TicketService(storage)

    service.create("Task 1", "Description 1", tags=["web"])
    service.create("Task 2", "Description 2", tags=["api"])

    result = service.list(tag="api")

    assert len(result) == 1
    assert result[0].title == "Task 2"


def test_get_ticket_success():
    storage = FakeStorage()
    service = TicketService(storage)

    ticket = service.create("Task", "Description")

    result = service.get(ticket.id)

    assert result.title == "Task"


def test_get_ticket_not_found_should_fail():
    storage = FakeStorage()
    service = TicketService(storage)

    with pytest.raises(ValueError):
        service.get(99)


def test_update_ticket_success():
    storage = FakeStorage()
    service = TicketService(storage)

    ticket = service.create("Task", "Description")

    result = service.update(ticket.id, "doing")

    assert result.status == "doing"


def test_update_ticket_with_invalid_status_should_fail():
    storage = FakeStorage()
    service = TicketService(storage)

    ticket = service.create("Task", "Description")

    with pytest.raises(ValueError):
        service.update(ticket.id, "finished")


def test_update_ticket_not_found_should_fail():
    storage = FakeStorage()
    service = TicketService(storage)

    with pytest.raises(ValueError):
        service.update(99, "done")
