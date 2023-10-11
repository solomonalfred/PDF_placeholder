from api import app
from fastapi.testclient import TestClient

client = TestClient(app)

def test_test():
    response = client.get("/")
    assert response.status_code == 200