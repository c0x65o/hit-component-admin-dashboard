"""Test API endpoints with mocked auth service."""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient
import httpx

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


@pytest.fixture
def mock_auth_users():
    """Sample user data from auth service."""
    return [
        {
            "email": "user1@example.com",
            "email_verified": True,
            "two_factor_enabled": False,
            "metadata": {},
            "created_at": "2024-01-01T00:00:00",
            "updated_at": "2024-01-02T00:00:00",
        },
        {
            "email": "user2@example.com",
            "email_verified": False,
            "two_factor_enabled": False,
            "metadata": {},
            "created_at": "2024-01-03T00:00:00",
            "updated_at": "2024-01-03T00:00:00",
        },
    ]


class MockResponse:
    """Mock httpx Response."""
    
    def __init__(self, json_data, status_code=200):
        self._json_data = json_data
        self.status_code = status_code
    
    def json(self):
        return self._json_data


class MockAsyncClient:
    """Mock httpx AsyncClient for testing."""
    
    def __init__(self, responses=None):
        self.responses = responses or {}
    
    async def __aenter__(self):
        return self
    
    async def __aexit__(self, *args):
        pass
    
    async def get(self, path):
        if path in self.responses:
            return self.responses[path]
        return MockResponse([], 404)
    
    async def post(self, path, json=None):
        if path in self.responses:
            return self.responses[path]
        return MockResponse({"detail": "Not found"}, 404)
    
    async def put(self, path, json=None):
        if path in self.responses:
            return self.responses[path]
        return MockResponse({"detail": "Not found"}, 404)
    
    async def delete(self, path):
        if path in self.responses:
            return self.responses[path]
        return MockResponse({"detail": "Not found"}, 404)


def test_api_users_returns_list(client, mock_auth_users):
    """GET /api/users returns user list from auth service."""
    mock_client = MockAsyncClient({
        "/users": MockResponse(mock_auth_users, 200)
    })
    
    async def mock_get_client():
        return mock_client
    
    with patch("app.main.get_auth_client", mock_get_client):
        response = client.get("/api/users")
    
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["email"] == "user1@example.com"


def test_api_users_handles_auth_failure(client):
    """GET /api/users returns empty list when auth fails."""
    mock_client = MockAsyncClient({
        "/users": MockResponse([], 500)
    })
    
    async def mock_get_client():
        return mock_client
    
    with patch("app.main.get_auth_client", mock_get_client):
        response = client.get("/api/users")
    
    assert response.status_code == 200
    assert response.json() == []


def test_api_get_user(client, mock_auth_users):
    """GET /api/users/{email} returns single user."""
    user = mock_auth_users[0]
    mock_client = MockAsyncClient({
        f"/users/{user['email']}": MockResponse(user, 200)
    })
    
    async def mock_get_client():
        return mock_client
    
    with patch("app.main.get_auth_client", mock_get_client):
        response = client.get(f"/api/users/{user['email']}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "user1@example.com"


def test_api_get_user_not_found(client):
    """GET /api/users/{email} returns 404 for unknown user."""
    mock_client = MockAsyncClient({})  # No responses configured
    
    async def mock_get_client():
        return mock_client
    
    with patch("app.main.get_auth_client", mock_get_client):
        response = client.get("/api/users/unknown@example.com")
    
    assert response.status_code == 404


def test_api_create_user(client):
    """POST /api/users creates user via auth service."""
    new_user = {
        "email": "new@example.com",
        "password": "secret123",
        "email_verified": True,
    }
    created_user = {
        "email": "new@example.com",
        "email_verified": True,
        "two_factor_enabled": False,
        "metadata": {},
        "created_at": "2024-01-05T00:00:00",
        "updated_at": "2024-01-05T00:00:00",
    }
    
    mock_client = MockAsyncClient({
        "/users": MockResponse(created_user, 201)
    })
    
    async def mock_get_client():
        return mock_client
    
    with patch("app.main.get_auth_client", mock_get_client):
        response = client.post("/api/users", json=new_user)
    
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "new@example.com"


def test_api_update_user(client, mock_auth_users):
    """PUT /api/users/{email} updates user via auth service."""
    user = mock_auth_users[0]
    updated_user = {**user, "email_verified": False}
    
    mock_client = MockAsyncClient({
        f"/users/{user['email']}": MockResponse(updated_user, 200)
    })
    
    async def mock_get_client():
        return mock_client
    
    with patch("app.main.get_auth_client", mock_get_client):
        response = client.put(
            f"/api/users/{user['email']}",
            json={"email_verified": False}
        )
    
    assert response.status_code == 200
    data = response.json()
    assert data["email_verified"] is False


def test_api_delete_user(client, mock_auth_users):
    """DELETE /api/users/{email} deletes user via auth service."""
    user = mock_auth_users[0]
    
    mock_client = MockAsyncClient({
        f"/users/{user['email']}": MockResponse({}, 204)
    })
    
    async def mock_get_client():
        return mock_client
    
    with patch("app.main.get_auth_client", mock_get_client):
        response = client.delete(f"/api/users/{user['email']}")
    
    assert response.status_code == 200
    assert response.json()["status"] == "deleted"


def test_api_stats(client, mock_auth_users):
    """GET /api/stats returns computed statistics."""
    mock_client = MockAsyncClient({
        "/users": MockResponse(mock_auth_users, 200)
    })
    
    async def mock_get_client():
        return mock_client
    
    with patch("app.main.get_auth_client", mock_get_client):
        response = client.get("/api/stats")
    
    assert response.status_code == 200
    data = response.json()
    assert data["total_users"] == 2
    assert data["verified_users"] == 1  # Only user1 is verified
    assert data["unverified_users"] == 1

