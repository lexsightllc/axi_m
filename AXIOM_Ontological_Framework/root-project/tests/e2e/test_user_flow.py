from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_user_creation_flow():
    user_data = {"name": "Flow User", "email": "flow@example.com", "password": "Pass1234"}
    r = client.post("/v1/users", json=user_data)
    assert r.status_code == 201
    uid = r.json()["id"]
    r2 = client.get(f"/v1/users/{uid}")
    assert r2.status_code == 200
    assert r2.json()["email"] == "flow@example.com"

