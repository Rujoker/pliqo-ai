from fastapi import FastAPI
from routers.chat import router as chat_router
from routers.analyze import router as analyze_router

app = FastAPI(title="Pliqo AI", version="0.1.0")

app.include_router(chat_router, prefix="/api")
app.include_router(analyze_router, prefix="/api")

@app.get("/health")
async def health():
    return {"status": "ok"}