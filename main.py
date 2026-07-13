from fastapi import FastAPI
from routers.chat import router as chat_router
from routers.analyze import router as analyze_router
from routers.upload import router as upload_router
from services.embeddings import get_chroma_client, get_collection, index_corpus

app = FastAPI(title="Pliqo AI", version="0.1.0")

app.include_router(chat_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")
app.include_router(upload_router, prefix="/api")

@app.on_event("startup")
async def startup():
    client = get_chroma_client()
    collection = get_collection(client)
    if collection.count() == 0:
        print("Corpus empty, indexing...")
        index_corpus()
        print("Corpus indexed.")

@app.get("/health")
async def health():
    return {"status": "ok"}