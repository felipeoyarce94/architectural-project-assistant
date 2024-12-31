"""This protocol defines the methods that a collection manager must implement."""

from typing import Protocol
from models import Item

class CollectionManager(Protocol):
    """This class is a protocol for a collection manager.
    It defines the methods that a collection manager must implement.
    """
    def __init__(self, collection_name: str):
        ...
    
    def create_collection(self, collection_name: str):
        """Create a new collection."""
        ...
    
    def update_collection(self, collection_name: str, item: Item):
        """Update an existing collection."""
        ...
    
    def delete_collection(self, collection_name: str):
        """Delete an existing collection."""
        ...