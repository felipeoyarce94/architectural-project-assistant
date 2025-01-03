from models import Item
from typing import Protocol
from langchain.docstore.document import Document

class Extractor(Protocol):
    
    def __init__(self, file_path: str, prompt_path: str, model: str):
        ...
    
    def load_pdf(self, file_path: str) -> list[Document]:
        ...
    
    def extract_items(self, docs: list[Document]) -> list[Item]:
        ...
