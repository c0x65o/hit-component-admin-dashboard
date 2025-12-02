"""Test health and manifest endpoints."""

import pytest
from fastapi.testclient import TestClient

from app.main import app


@pytest.fixture
def client():
    """Create test client."""
    return TestClient(app)


def test_health_endpoint(client):
    """Health endpoint returns ok status."""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["component"] == "admin-dashboard"
    assert "version" in data


def test_manifest_endpoint(client):
    """Manifest endpoint returns component metadata."""
    response = client.get("/manifest")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "admin-dashboard"
    assert "version" in data
    assert "nav" in data
    assert "routes" in data
    assert len(data["nav"]) >= 2  # Dashboard and Users
    assert len(data["routes"]) >= 3  # /, /users, /users/:email

