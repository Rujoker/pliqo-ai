import chromadb
from pathlib import Path

CORPUS_DIR = Path(__file__).parent.parent / "corpus"
CHROMA_DIR = Path(__file__).parent.parent / ".chroma"

def get_chroma_client():
    return chromadb.PersistentClient(path=str(CHROMA_DIR))

def get_collection(client: chromadb.Client):
    return client.get_or_create_collection(name="pliqo_corpus")

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def index_corpus():
    client = get_chroma_client()
    collection = get_collection(client)

    for file in CORPUS_DIR.glob("*.md"):
        text = file.read_text()
        chunks = chunk_text(text)
        
        collection.upsert(
            documents=chunks,
            ids=[f"{file.stem}_{i}" for i in range(len(chunks))]
        )
        print(f"Indexed {file.name}: {len(chunks)} chunks")

if __name__ == "__main__":
    index_corpus()