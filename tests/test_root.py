from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def teste_root_ok():
    r = client.get("/")
    assert r.status_code == 200
    body = r.json()
    assert body.get("ok") is True