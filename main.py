from fastapi import FastAPI

app = FastAPI(title="Pliqo AI", version="0.1.0")

@app.get("/health")
async def health():
    return {"status": "ok"}