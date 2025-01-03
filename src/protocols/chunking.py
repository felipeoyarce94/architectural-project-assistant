"""This protocol defines the interface for chunking documents."""

from abc import ABC, abstractmethod
from langchain_core.documents import Document

class Chunker(ABC):
    @abstractmethod
    def chunk(self, document: Document) -> list[Document]:
        pass
    
    def _split_sentences(self, document: str) -> list[str]:
        pass
    
    def _combine_sentences(self, sentences: list[str], buffer_size: int = 1) -> str:
        pass

    def _embed_sentences(self, sentences: list[str]) -> list[list[float]]:
