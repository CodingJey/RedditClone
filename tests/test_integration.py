
import pytest
from fastapi.testclient import TestClient
from main import app  # Replace with the correct path to your app if needed
from infra.database import get_test_db

# Replace the database dependency with the in-memory test database
def override_get_db():
    yield from get_test_db()

app.dependency_overrides[get_test_db] = override_get_db

@pytest.fixture(scope="module")
def test_client():
    """Provides a test client for the FastAPI app."""
    client = TestClient(app)
    yield client

# Example integration test
def test_create_and_read_item(test_client):
    # Replace with your actual API endpoint and payload
    response = test_client.post(
        "/items/", json={"name": "Test Item", "description": "A test item", "price": 9.99, "available": True}
    )
    assert response.status_code == 201
    created_item = response.json()
    assert created_item["name"] == "Test Item"

    # Fetch the created item
    response = test_client.get(f"/items/{created_item['id']}")
    assert response.status_code == 200
    fetched_item = response.json()
    assert fetched_item["id"] == created_item["id"]
    assert fetched_item["name"] == "Test Item"


