from fastapi import FastAPI
from src.api.collection_endpoint import router as collection_router

app = FastAPI(title="Qdrant API", version="1.0.0")
app.include_router(collection_router)

@app.get("/")
async def root():
    return {"message": "Welcome to Qdrant Collection Manager API"}