import json
from urllib import request, error

from .kb_client import KBClient
from .kb_model import Document, SearchResult


class HTTPKBClient(KBClient):
    def __init__(self, base_url):
        if not base_url:
            raise ValueError("KB_API_URL is required for HTTP client")

        self.base_url = base_url.rstrip("/")

    def _post(self, path, payload):
        url = self.base_url + path

        data = json.dumps(payload).encode("utf-8")

        req = request.Request(
            url,
            data=data,
            headers={"Content-Type": "application/json"},
            method="POST",
        )

        try:
            with request.urlopen(req, timeout=10) as response:
                body = response.read().decode("utf-8")
                if not body:
                    return {}
                return json.loads(body)

        except error.HTTPError as exc:
            raise ValueError(f"KB API error: {exc.code}") from exc

        except error.URLError as exc:
            raise ValueError(f"Cannot connect to KB API: {exc.reason}") from exc

        except json.JSONDecodeError as exc:
            raise ValueError("Invalid JSON response from KB API") from exc

    def search(self, query, top_k=5):
        data = self._post(
            "/search",
            {
                "query": query,
                "topK": top_k,
            },
        )

        results = []

        for item in data.get("results", []):
            results.append(
                SearchResult(
                    id=item["id"],
                    title=item["title"],
                    node_path=item.get("nodePath") or item.get("node_path"),
                )
            )

        return results

    def list(self, node_path, limit=10):
        data = self._post(
            "/list",
            {
                "nodePath": node_path,
                "limit": limit,
            },
        )

        docs = data.get("documents", data.get("results", []))

        return [self._to_document(item) for item in docs]

    def retrieve(self, doc_id):
        data = self._post(
            "/retrieve",
            {
                "docId": doc_id,
            },
        )

        doc = data.get("document", data)

        if not doc:
            raise ValueError("Document not found")

        return self._to_document(doc)

    def add(self, title, content, node_path, tags):
        data = self._post(
            "/add",
            {
                "title": title,
                "content": content,
                "nodePath": node_path,
                "tags": tags,
            },
        )

        doc = data.get("document", data)

        return self._to_document(doc)

    def _to_document(self, item):
        return Document(
            id=item["id"],
            title=item["title"],
            content=item.get("content", ""),
            node_path=item.get("nodePath") or item.get("node_path"),
            tags=item.get("tags", []),
        )

