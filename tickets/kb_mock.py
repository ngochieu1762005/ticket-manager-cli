from .kb_client import KBClient
from .kb_model import Document, SearchResult


class MockKBClient(KBClient):
    def __init__(self):
        self.docs = [
            Document(
                id="doc-001",
                title="Customer Response Template",
                content="This is an email response template for customer support.",
                node_path="/templates/email",
                tags=["template", "email", "support"],
            ),
            Document(
                id="doc-002",
                title="DevOps Team Schedule",
                content="This document contains the DevOps team weekly schedule.",
                node_path="/team/devops",
                tags=["team", "devops", "schedule"],
            ),
            Document(
                id="doc-003",
                title="Getting Started Guide",
                content="This guide explains how to start using the internal tools.",
                node_path="/docs/guides",
                tags=["guide", "docs"],
            ),
        ]

    def search(self, query, top_k=5):
        query = query.lower()
        results = []

        for doc in self.docs:
            text = " ".join(
                [
                    doc.title,
                    doc.content,
                    doc.node_path,
                    " ".join(doc.tags),
                ]
            ).lower()

            if query in text:
                results.append(
                    SearchResult(
                        id=doc.id,
                        title=doc.title,
                        node_path=doc.node_path,
                    )
                )

        return results[:top_k]

    def list(self, node_path, limit=10):
        results = []

        for doc in self.docs:
            if doc.node_path == node_path:
                results.append(doc)

        return results[:limit]

    def retrieve(self, doc_id):
        for doc in self.docs:
            if doc.id == doc_id:
                return doc

        raise ValueError("Document not found")

    def add(self, title, content, node_path, tags):
        new_id = f"doc-{len(self.docs) + 1:03d}"

        doc = Document(
            id=new_id,
            title=title,
            content=content,
            node_path=node_path,
            tags=tags,
        )

        self.docs.append(doc)
        return doc    
