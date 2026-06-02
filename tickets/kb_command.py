from .kb_factory import create_kb_client


def add_kb_parser(commands):
    kb_cmd = commands.add_parser("kb")
    kb_commands = kb_cmd.add_subparsers(dest="kb_command")

    search_cmd = kb_commands.add_parser("search")
    search_cmd.add_argument("query")
    search_cmd.add_argument("--top-k", type=int, default=5)

    list_cmd = kb_commands.add_parser("list")
    list_cmd.add_argument("--node", required=True)
    list_cmd.add_argument("--limit", type=int, default=10)

    retrieve_cmd = kb_commands.add_parser("retrieve")
    retrieve_cmd.add_argument("doc_id")

    add_cmd = kb_commands.add_parser("add")
    add_cmd.add_argument("--file", required=True)
    add_cmd.add_argument("--path", required=True)
    add_cmd.add_argument("--tags", default="")
    add_cmd.add_argument("--title")


def handle_kb_command(args):
    client = create_kb_client()

    if args.kb_command == "search":
        results = client.search(args.query, args.top_k)

        if not results:
            print("No documents found")
            return

        for item in results:
            print(f"{item.id} | {item.title} | {item.node_path}")

    elif args.kb_command == "list":
        docs = client.list(args.node, args.limit)

        if not docs:
            print("No documents found")
            return

        for doc in docs:
            print(f"{doc.id} | {doc.title} | {doc.node_path}")

    elif args.kb_command == "retrieve":
        doc = client.retrieve(args.doc_id)

        print(f"ID: {doc.id}")
        print(f"Title: {doc.title}")
        print(f"Node: {doc.node_path}")
        print(f"Tags: {', '.join(doc.tags)}")
        print("Content:")
        print(doc.content)

    elif args.kb_command == "add":
        with open(args.file, "r", encoding="utf-8") as file:
            content = file.read()

        tags = []
        if args.tags:
            tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]

        title = args.title
        if not title:
            title = args.file.split("/")[-1]

        doc = client.add(
            title=title,
            content=content,
            node_path=args.path,
            tags=tags,
        )

        print(f"Added document {doc.id}")
        print(f"Title: {doc.title}")

    else:
        print("Missing kb command")
