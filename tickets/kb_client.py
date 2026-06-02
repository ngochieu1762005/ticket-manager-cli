from abc import ABC, abstractmethod


class KBClient(ABC):
    @abstractmethod
    def search(self, query, top_k=5):
        pass

    @abstractmethod
    def list(self, node_path, limit=10):
        pass

    @abstractmethod
    def retrieve(self, doc_id):
        pass

    @abstractmethod
    def add(self, title, content, node_path, tags):
        pass
