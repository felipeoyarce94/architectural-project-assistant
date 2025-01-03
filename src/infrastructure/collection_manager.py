"""This module provides a Qdrant collection manager."""

from qdrant_client import QdrantClient, models
from langchain_qdrant import FastEmbedSparse
from langchain_huggingface import HuggingFaceEmbeddings
from src.settings import QDRANT_COLLECTION_URL, QDRANT_API_KEY, DENSE_EMBEDDINGS_MODEL, SPARSE_EMBEDDINGS_MODEL, DENSE_EMBEDDINGS_DIMENSION
from src.models import Item
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

class QdrantCollectionManager:
    """This class is a Qdrant collection manager.
    
    Args:
        collection_name: The name of the collection to manage.
    
    Attributes:
        client: The Qdrant client.
        collection_name: The name of the collection to manage.
    """
    def __init__(self):
        self.client = QdrantClient(url=QDRANT_COLLECTION_URL, api_key=QDRANT_API_KEY)
        self.dense_embeddings = HuggingFaceEmbeddings(model_name=DENSE_EMBEDDINGS_MODEL)
        self.sparse_embeddings = FastEmbedSparse(model_name=SPARSE_EMBEDDINGS_MODEL)
        self._list_collections()

        
    def create_collection(self, collection_name: str):
        """Create a new collection.
        
        Args:
            collection_name: The name of the collection to create.
        """
        try:
            if self.client.collection_exists(collection_name=collection_name):
                logging.warning(f"Collection {collection_name} already exists")
                return
            
            logging.info(f"Creating collection {collection_name}")
            self.client.create_collection(
                collection_name=collection_name,
                vectors_config={
                    DENSE_EMBEDDINGS_MODEL: models.VectorParams(
                            size=DENSE_EMBEDDINGS_DIMENSION,
                            distance=models.Distance.COSINE,
                        ),
                    },
                    sparse_vectors_config={
                        SPARSE_EMBEDDINGS_MODEL: models.SparseVectorParams(
                            modifier=models.Modifier.IDF,
                        )
                    }
                )
            logging.info(f"Collection {collection_name} created successfully")
        except Exception as e:
            logging.error(f"Error creating collection {collection_name}: {e}")
            raise e
        
    def update_collection(self, collection_name: str, item: list[Item]):
        """Update an existing collection."""
        logging.info(f"Updating collection {collection_name} with item {item}")
        self.client.upsert(collection_name=collection_name, points=item)
        
    def delete_collection(self, collection_name: str):
        """Delete an existing collection.
        
        Args:
            collection_name: The name of the collection to delete.
        """
        try:
            if not self.client.collection_exists(collection_name=collection_name):
                logging.warning(f"Collection {collection_name} does not exist")
                return
            
            logging.info(f"Deleting collection {collection_name}")
            self.client.delete_collection(collection_name=collection_name)
            logging.info(f"Collection {collection_name} deleted successfully")
        except Exception as e:
            logging.error(f"Error deleting collection {collection_name}: {e}")
            raise e
    
    def _list_collections(self):
        """List all available collections."""
        try:
            collections = self.client.get_collections().collections
            if collections:
                logging.info("Available collections:")
                for collection in collections:
                    logging.info(f"- {collection.name}")
            else:
                logging.info("No collections available")
        except Exception as e:
            logging.error(f"Error listing collections: {e}")
            raise e
