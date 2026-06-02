import os

from .kb_mock import MockKBClient
from .kb_http import HTTPKBClient


def create_kb_client():
    client_type = os.environ.get("KB_CLIENT", "mock").lower()

    if client_type == "mock":
        return MockKBClient()

    if client_type == "http":
        base_url = os.environ.get("KB_API_URL")
        return HTTPKBClient(base_url)

    raise ValueError("Invalid KB_CLIENT. Use 'mock' or 'http'")
