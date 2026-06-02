import json
import threading
from http.server import BaseHTTPRequestHandler, HTTPServer

from tickets.kb_http import HTTPKBClient


class FakeKBHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length).decode("utf-8")

        if body:
            json.loads(body)

        if self.path == "/search":
            data = {
                "results": [
                    {
                        "id": "doc-001",
                        "title": "Customer Response Template",
                        "nodePath": "/templates/email",
                    }
                ]
            }

        elif self.path == "/list":
            data = {
                "documents": [
                    {
                        "id": "doc-001",
                        "title": "Customer Response Template",
                        "content": "Email content",
                        "nodePath": "/templates/email",
                        "tags": ["template", "email"],
                    }
                ]
            }

        elif self.path == "/retrieve":
            data = {
                "document": {
                    "id": "doc-001",
                    "title": "Customer Response Template",
                    "content": "Email content",
                    "nodePath": "/templates/email",
                    "tags": ["template", "email"],
                }
            }

        elif self.path == "/add":
            data = {
                "document": {
                    "id": "doc-004",
                    "title": "New Template",
                    "content": "New content",
                    "nodePath": "/templates/email",
                    "tags": ["template"],
                }
            }

        else:
            self.send_response(404)
            self.end_headers()
            return

        response = json.dumps(data).encode("utf-8")

        self.send_response(200)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(response)))
        self.end_headers()
        self.wfile.write(response)

    def log_message(self, format, *args):
        pass


def make_server():
    server = HTTPServer(("127.0.0.1", 0), FakeKBHandler)
    thread = threading.Thread(target=server.serve_forever)
    thread.daemon = True
    thread.start()
    return server


def test_http_kb_search():
    server = make_server()

    try:
        client = HTTPKBClient(f"http://127.0.0.1:{server.server_port}")

        results = client.search("response", top_k=3)

        assert len(results) == 1
        assert results[0].id == "doc-001"

    finally:
        server.shutdown()


def test_http_kb_list():
    server = make_server()

    try:
        client = HTTPKBClient(f"http://127.0.0.1:{server.server_port}")

        docs = client.list("/templates/email", limit=10)

        assert len(docs) == 1
        assert docs[0].node_path == "/templates/email"

    finally:
        server.shutdown()


def test_http_kb_retrieve():
    server = make_server()

    try:
        client = HTTPKBClient(f"http://127.0.0.1:{server.server_port}")

        doc = client.retrieve("doc-001")

        assert doc.id == "doc-001"
        assert doc.title == "Customer Response Template"

    finally:
        server.shutdown()


def test_http_kb_add():
    server = make_server()

    try:
        client = HTTPKBClient(f"http://127.0.0.1:{server.server_port}")

        doc = client.add(
            title="New Template",
            content="New content",
            node_path="/templates/email",
            tags=["template"],
        )

        assert doc.id == "doc-004"
        assert doc.title == "New Template"

    finally:
        server.shutdown()

