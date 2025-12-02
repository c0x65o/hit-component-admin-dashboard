"""Admin Dashboard Component.

Provides Server-Driven UI specs for rendering admin dashboard pages.
The frontend SDK renders these specs as React components.
"""

import os
from typing import Any

import httpx
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from app.ui_specs import (
    get_dashboard_spec,
    get_users_list_spec,
    get_user_edit_spec,
)

app = FastAPI(
    title="Hit Admin Dashboard Component",
    version="1.0.0",
    docs_url="/docs",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Auth module URL for fetching user data
AUTH_URL = os.environ.get("HIT_AUTH_URL", "http://localhost:8001")


async def get_auth_client() -> httpx.AsyncClient:
    """Get HTTP client for auth module."""
    return httpx.AsyncClient(base_url=AUTH_URL, timeout=10.0)


@app.get("/health")
async def health() -> dict[str, Any]:
    """Health check endpoint."""
    return {"status": "ok", "component": "admin-dashboard", "version": "1.0.0"}


@app.get("/manifest")
async def manifest() -> dict[str, Any]:
    """Component manifest - describes routes, nav items, and capabilities.
    
    Host apps fetch this to integrate the component into their navigation.
    """
    return {
        "name": "admin-dashboard",
        "version": "1.0.0",
        "description": "Admin dashboard for user management",
        "nav": [
            {"path": "/admin", "label": "Dashboard", "icon": "dashboard"},
            {"path": "/admin/users", "label": "Users", "icon": "users"},
        ],
        "routes": [
            {"path": "/", "ui": "/ui/dashboard"},
            {"path": "/users", "ui": "/ui/users"},
            {"path": "/users/:email", "ui": "/ui/users/:email"},
        ],
        "dependencies": {
            "modules": ["auth"],
        },
    }


# =============================================================================
# UI Spec Endpoints - Return UI specifications for the frontend to render
# =============================================================================


@app.get("/ui/dashboard")
async def ui_dashboard() -> dict[str, Any]:
    """Get UI spec for the main dashboard page."""
    async with await get_auth_client() as client:
        try:
            response = await client.get("/users")
            users = response.json() if response.status_code == 200 else []
        except Exception:
            users = []

    return get_dashboard_spec(
        total_users=len(users),
        verified_users=sum(1 for u in users if u.get("email_verified")),
        recent_users=users[:5] if users else [],
    )


@app.get("/ui/users")
async def ui_users() -> dict[str, Any]:
    """Get UI spec for the users list page."""
    return get_users_list_spec()


@app.get("/ui/users/{user_id}")
async def ui_user_edit(user_id: str) -> dict[str, Any]:
    """Get UI spec for the user edit page."""
    async with await get_auth_client() as client:
        try:
            response = await client.get(f"/users/{user_id}")
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="User not found")
            user = response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Auth service error: {e}")

    return get_user_edit_spec(user)


# =============================================================================
# API Endpoints - Data operations
# =============================================================================


@app.get("/api/users")
async def api_users() -> list[dict[str, Any]]:
    """Get all users from auth module."""
    async with await get_auth_client() as client:
        try:
            response = await client.get("/users")
            if response.status_code != 200:
                return []
            return response.json()
        except Exception:
            return []


@app.post("/api/users")
async def api_create_user(data: dict[str, Any]) -> dict[str, Any]:
    """Create a new user via auth module."""
    async with await get_auth_client() as client:
        try:
            response = await client.post("/users", json=data)
            if response.status_code not in (200, 201):
                error = response.json().get("detail", "Create failed")
                raise HTTPException(status_code=response.status_code, detail=error)
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Auth service error: {e}")


@app.get("/api/users/{email}")
async def api_user(email: str) -> dict[str, Any]:
    """Get a single user from auth module."""
    async with await get_auth_client() as client:
        try:
            response = await client.get(f"/users/{email}")
            if response.status_code != 200:
                raise HTTPException(status_code=404, detail="User not found")
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Auth service error: {e}")


@app.put("/api/users/{email}")
async def api_update_user(email: str, data: dict[str, Any]) -> dict[str, Any]:
    """Update a user via auth module."""
    async with await get_auth_client() as client:
        try:
            response = await client.put(f"/users/{email}", json=data)
            if response.status_code != 200:
                error = response.json().get("detail", "Update failed")
                raise HTTPException(status_code=response.status_code, detail=error)
            return response.json()
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Auth service error: {e}")


@app.delete("/api/users/{email}")
async def api_delete_user(email: str) -> dict[str, str]:
    """Delete a user via auth module."""
    async with await get_auth_client() as client:
        try:
            response = await client.delete(f"/users/{email}")
            if response.status_code not in (200, 204):
                error = response.json().get("detail", "Delete failed")
                raise HTTPException(status_code=response.status_code, detail=error)
            return {"status": "deleted"}
        except httpx.HTTPError as e:
            raise HTTPException(status_code=502, detail=f"Auth service error: {e}")


@app.get("/api/stats")
async def api_stats() -> dict[str, Any]:
    """Get dashboard statistics."""
    async with await get_auth_client() as client:
        try:
            response = await client.get("/users")
            users = response.json() if response.status_code == 200 else []
        except Exception:
            users = []

    return {
        "total_users": len(users),
        "verified_users": sum(1 for u in users if u.get("email_verified")),
        "unverified_users": sum(1 for u in users if not u.get("email_verified")),
        "two_factor_enabled": sum(1 for u in users if u.get("two_factor_enabled")),
    }

