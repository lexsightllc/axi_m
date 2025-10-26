# SPDX-License-Identifier: MIT
from fastapi.testclient import TestClient
from api import app

client = TestClient(app)

def test_health_endpoint():
    resp = client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "message": "Nexus SaaS API is operational."}

