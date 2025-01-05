
import pytest
from fastapi.testclient import TestClient
from main import app  # Adjust the path if needed
from infra.database import get_test_db
import sys
import os

# Add the project root to PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Override the database dependency to use the in-memory test database
def override_get_db():
    yield from get_test_db()

# Apply the override globally
app.dependency_overrides[get_test_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    """
    Provides a FastAPI TestClient for integration testing.
    """
    client = TestClient(app)
    yield client

