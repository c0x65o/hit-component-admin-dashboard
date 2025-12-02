"""Test UI specification generators."""

import pytest

from app.ui_specs import (
    get_dashboard_spec,
    get_users_list_spec,
    get_user_edit_spec,
)


def test_dashboard_spec_structure():
    """Dashboard spec has required structure."""
    spec = get_dashboard_spec(
        total_users=10,
        verified_users=8,
        recent_users=[],
    )
    
    assert spec["type"] == "Page"
    assert spec["title"] == "Admin Dashboard"
    assert "children" in spec
    assert "actions" in spec
    
    # Should have StatsGrid
    stats_grid = next(
        (c for c in spec["children"] if c["type"] == "StatsGrid"),
        None,
    )
    assert stats_grid is not None
    assert len(stats_grid["items"]) == 4


def test_dashboard_spec_stats_calculation():
    """Dashboard spec calculates stats correctly."""
    spec = get_dashboard_spec(
        total_users=10,
        verified_users=7,
        recent_users=[],
    )
    
    stats_grid = next(c for c in spec["children"] if c["type"] == "StatsGrid")
    items = stats_grid["items"]
    
    # Find stats by label
    total = next(i for i in items if i["label"] == "Total Users")
    verified = next(i for i in items if i["label"] == "Verified")
    unverified = next(i for i in items if i["label"] == "Unverified")
    
    assert total["value"] == 10
    assert verified["value"] == 7
    assert unverified["value"] == 3


def test_dashboard_spec_handles_zero_users():
    """Dashboard spec handles zero users without division error."""
    spec = get_dashboard_spec(
        total_users=0,
        verified_users=0,
        recent_users=[],
    )
    
    stats_grid = next(c for c in spec["children"] if c["type"] == "StatsGrid")
    verified = next(i for i in stats_grid["items"] if i["label"] == "Verified")
    
    # Should not crash and should show 0% or 0
    assert verified["change"] == 0


def test_users_list_spec_structure():
    """Users list spec has required structure."""
    spec = get_users_list_spec()
    
    assert spec["type"] == "Page"
    assert spec["title"] == "Users"
    assert "children" in spec
    assert "actions" in spec
    
    # Should have a Card with DataTable
    card = spec["children"][0]
    assert card["type"] == "Card"
    
    data_table = card["children"][0]
    assert data_table["type"] == "DataTable"
    assert data_table["endpoint"] == "/api/users"
    assert data_table["searchable"] is True
    assert data_table["pagination"] is True


def test_users_list_spec_columns():
    """Users list spec has correct columns."""
    spec = get_users_list_spec()
    
    data_table = spec["children"][0]["children"][0]
    columns = data_table["columns"]
    column_keys = [c["key"] for c in columns]
    
    assert "email" in column_keys
    assert "email_verified" in column_keys
    assert "created_at" in column_keys


def test_users_list_spec_row_actions():
    """Users list spec has edit and delete row actions."""
    spec = get_users_list_spec()
    
    data_table = spec["children"][0]["children"][0]
    row_actions = data_table["rowActions"]
    action_labels = [a["label"] for a in row_actions]
    
    assert "Edit" in action_labels
    assert "Delete" in action_labels


def test_user_edit_spec_structure():
    """User edit spec has required structure."""
    user = {
        "email": "test@example.com",
        "email_verified": True,
        "two_factor_enabled": False,
        "created_at": "2024-01-01T00:00:00",
        "updated_at": "2024-01-02T00:00:00",
    }
    
    spec = get_user_edit_spec(user)
    
    assert spec["type"] == "Page"
    assert "Edit User" in spec["title"]
    assert spec["description"] == "test@example.com"
    assert "children" in spec


def test_user_edit_spec_form():
    """User edit spec has form with correct fields."""
    user = {
        "email": "test@example.com",
        "email_verified": True,
        "two_factor_enabled": False,
    }
    
    spec = get_user_edit_spec(user)
    
    # Find form in first card
    details_card = spec["children"][0]
    form = details_card["children"][0]
    
    assert form["type"] == "Form"
    assert form["method"] == "PUT"
    assert "test@example.com" in form["endpoint"]
    
    # Check initial values
    assert form["initialValues"]["email_verified"] is True
    assert form["initialValues"]["two_factor_enabled"] is False


def test_user_edit_spec_danger_zone():
    """User edit spec has danger zone with delete button."""
    user = {"email": "test@example.com"}
    
    spec = get_user_edit_spec(user)
    
    # Find danger zone card
    danger_card = next(
        (c for c in spec["children"] if c.get("title") == "Danger Zone"),
        None,
    )
    assert danger_card is not None
    
    # Should have delete button
    delete_btn = next(
        (c for c in danger_card["children"] if c["type"] == "Button" and c.get("label") == "Delete User"),
        None,
    )
    assert delete_btn is not None
    assert delete_btn["variant"] == "danger"

