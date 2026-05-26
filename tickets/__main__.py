import argparse
from .storage import JsonStorage
from .service import TicketService


def main():
    parser = argparse.ArgumentParser(prog="tickets")
    parser.add_argument("--file", default="tickets.json")

    commands = parser.add_subparsers(dest="command")

    create_cmd = commands.add_parser("create")
    create_cmd.add_argument("--title", required=True)
    create_cmd.add_argument("--description", required=True)
    create_cmd.add_argument("--priority", default="medium", choices=["low", "medium", "high"])
    create_cmd.add_argument("--tags", default="")

    list_cmd = commands.add_parser("list")
    list_cmd.add_argument("--status", choices=["open", "doing", "done"])
    list_cmd.add_argument("--priority", choices=["low", "medium", "high"])
    list_cmd.add_argument("--tag")

    show_cmd = commands.add_parser("show")
    show_cmd.add_argument("id", type=int)

    update_cmd = commands.add_parser("update")
    update_cmd.add_argument("id", type=int)
    update_cmd.add_argument("--status", required=True, choices=["open", "doing", "done"])

    args = parser.parse_args()

    storage = JsonStorage(args.file)
    service = TicketService(storage)

    try:
        if args.command == "create":
            tags = []
            if args.tags:
                tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]

            ticket = service.create(
                title=args.title,
                description=args.description,
                priority=args.priority,
                tags=tags,
            )

            print(f"Created ticket #{ticket.id}")
            print(f"Title: {ticket.title}")

        elif args.command == "list":
            tickets = service.list(
                status=args.status,
                priority=args.priority,
                tag=args.tag,
            )

            if not tickets:
                print("No tickets found")
                return

            for ticket in tickets:
                print(f"#{ticket.id} {ticket.title} [{ticket.status}] [{ticket.priority}]")

        elif args.command == "show":
            ticket = service.get(args.id)

            print(f"ID: {ticket.id}")
            print(f"Title: {ticket.title}")
            print(f"Description: {ticket.description}")
            print(f"Status: {ticket.status}")
            print(f"Priority: {ticket.priority}")
            print(f"Tags: {', '.join(ticket.tags)}")

        elif args.command == "update":
            ticket = service.update(args.id, args.status)

            print(f"Updated ticket #{ticket.id}")
            print(f"Status: {ticket.status}")

        else:
            parser.print_help()

    except ValueError as error:
        print(f"Error: {error}")


if __name__ == "__main__":
    main()
