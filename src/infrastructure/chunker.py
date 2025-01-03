"""This module contains the implementation of the Chunker protocol."""

# from src.protocols.chunking import Chunker
import PyPDF2
from langchain.embeddings import OpenAIEmbeddings
from src.settings.common import TEXT_EMBEDDING_MODEL

class Chunker:
    
    def __init__(self, 
                path: str,
                model: str = TEXT_EMBEDDING_MODEL):
        self.document = document
        self.embeddings = OpenAIEmbeddings(model=model)

    def _split_sentences(self, document: str) -> list[str]:
        pass

    def _combine_sentences(self, sentences: list[str], buffer_size: int = 1) -> str:
        pass

