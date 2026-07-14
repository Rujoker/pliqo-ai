from fastapi.testclient import TestClient

from main import app


def test_health_returns_ok():
    # No context manager on purpose: the startup handler (which indexes the
    # corpus via ChromaDB) only runs in context-manager mode, so this test
    # stays fast and offline and never touches the vector store or the API.
    client = TestClient(app)
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}