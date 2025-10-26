import os
import sys
import pytest

# Ensure modules under root-project are importable
ROOT_DIR = os.path.dirname(os.path.dirname(__file__))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from fastapi.testclient import TestClient
from api import app

@pytest.fixture(scope="session")
def client():
    return TestClient(app)
