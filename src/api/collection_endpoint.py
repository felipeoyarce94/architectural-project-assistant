from fastapi import APIRouter, HTTPException
from src.infrastructure.collection_manager import QdrantCollectionManager
from src.models.item import Item

router = APIRouter(prefix="/collections", tags=["collections"])
collection_manager = QdrantCollectionManager()

@router.post("/{collection_name}")
async def create_collection(collection_name: str):
    try:
        collection_manager.create_collection(collection_name)
        return {"message": f"Collection {collection_name} created successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.put("/{collection_name}")
async def update_collection(collection_name: str, items: list[Item]):
    try:
        collection_manager.update_collection(collection_name, items)
        return {"message": f"Collection {collection_name} updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.delete("/{collection_name}")
async def delete_collection(collection_name: str):
    try:
        collection_manager.delete_collection(collection_name)
        return {"message": f"Collection {collection_name} deleted successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
