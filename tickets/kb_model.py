from dataclasses import dataclass


@dataclass
class Document:
    id: str
    title: str
    content: str
    node_path: str
    tags: list[str]

@dataclass
class SearchResult:
    id: str
    title: str
    node_path: str

