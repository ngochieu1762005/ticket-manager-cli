from tickets.kb_mock import MockKBClient


def test_mock_kb_search():
    client = MockKBClient()

    results = client.search("response", top_k=3)

    assert len(results) == 1
    assert results[0].id == "doc-001"
    assert "Template" in results[0].title


def test_mock_kb_list():
    client = MockKBClient()

    docs = client.list("/templates/email", limit=10)

    assert len(docs) == 1
    assert docs[0].node_path == "/templates/email"


def test_mock_kb_retrieve():
    client = MockKBClient()

    doc = client.retrieve("doc-001")

    assert doc.id == "doc-001"
    assert doc.title == "Customer Response Template"


def test_mock_kb_add():
    client = MockKBClient()

    doc = client.add(
        title="SMS Template",
        content="Hello customer",
        node_path="/templates/sms",
        tags=["sms", "template"],
    )

    assert doc.id == "doc-004"
    assert doc.title == "SMS Template"

    docs = client.list("/templates/sms", limit=10)

    assert len(docs) == 1
    assert docs[0].id == "doc-004"


def test_mock_kb_retrieve_missing_doc():
    client = MockKBClient()

    try:
        client.retrieve("missing")
        assert False
    except ValueError as error:
        assert "Document not found" in str(error)
