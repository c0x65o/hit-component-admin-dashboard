"""UI Specifications for Admin Dashboard.

These functions return UI spec dictionaries that match the Hit SDK UI types.
The frontend SDK renders these specs as React components.
"""

from typing import Any


def get_dashboard_spec(
    total_users: int,
    verified_users: int,
    recent_users: list[dict[str, Any]],
) -> dict[str, Any]:
    """Generate the main dashboard page UI spec."""
    return {
        "type": "Page",
        "title": "Admin Dashboard",
        "description": "Overview of your application",
        "actions": [
            {
                "type": "Button",
                "label": "Add User",
                "variant": "primary",
                "icon": "+",
                "onClick": {
                    "type": "openModal",
                    "modal": {
                        "type": "Modal",
                        "title": "Add New User",
                        "size": "md",
                        "children": [
                            {
                                "type": "Form",
                                "endpoint": "/api/users",
                                "method": "POST",
                                "submitText": "Create User",
                                "cancelText": "Cancel",
                                "fields": [
                                    {
                                        "type": "TextField",
                                        "name": "email",
                                        "label": "Email",
                                        "inputType": "email",
                                        "required": True,
                                        "placeholder": "user@example.com",
                                    },
                                    {
                                        "type": "TextField",
                                        "name": "password",
                                        "label": "Password",
                                        "inputType": "password",
                                        "required": True,
                                    },
                                    {
                                        "type": "Checkbox",
                                        "name": "email_verified",
                                        "label": "Email Verified",
                                        "checkboxLabel": "Mark email as verified",
                                    },
                                ],
                                "onSuccess": {"type": "refresh"},
                            }
                        ],
                    },
                },
            }
        ],
        "children": [
            # Stats Grid
            {
                "type": "StatsGrid",
                "columns": 4,
                "items": [
                    {
                        "label": "Total Users",
                        "value": total_users,
                        "icon": "👥",
                        "onClick": {"type": "navigate", "to": "/admin/users"},
                    },
                    {
                        "label": "Verified",
                        "value": verified_users,
                        "icon": "✓",
                        "change": (
                            round(verified_users / total_users * 100)
                            if total_users > 0
                            else 0
                        ),
                        "changeType": "neutral",
                    },
                    {
                        "label": "Unverified",
                        "value": total_users - verified_users,
                        "icon": "⏳",
                    },
                    {
                        "label": "Active Today",
                        "value": "—",
                        "icon": "📊",
                    },
                ],
            },
            # Recent Users Card
            {
                "type": "Card",
                "title": "Recent Users",
                "subtitle": "Latest registered users",
                "className": "mt-6",
                "children": [
                    {
                        "type": "DataTable",
                        "endpoint": "/api/users",
                        "pagination": False,
                        "searchable": False,
                        "columns": [
                            {"key": "email", "label": "Email"},
                            {
                                "key": "email_verified",
                                "label": "Verified",
                                "type": "boolean",
                            },
                            {
                                "key": "created_at",
                                "label": "Created",
                                "type": "datetime",
                            },
                        ],
                        "rowActions": [
                            {
                                "type": "Button",
                                "label": "View",
                                "variant": "ghost",
                                "size": "sm",
                                "onClick": {
                                    "type": "navigate",
                                    "to": "/admin/users/{email}",
                                },
                            }
                        ],
                        "emptyMessage": "No users yet",
                    }
                ],
                "footer": [
                    {
                        "type": "Link",
                        "label": "View all users →",
                        "href": "/admin/users",
                    }
                ],
            },
            # Quick Actions Card
            {
                "type": "Card",
                "title": "Quick Actions",
                "className": "mt-6",
                "children": [
                    {
                        "type": "Row",
                        "gap": 12,
                        "children": [
                            {
                                "type": "Button",
                                "label": "Export Users",
                                "variant": "outline",
                                "onClick": {
                                    "type": "api",
                                    "method": "GET",
                                    "endpoint": "/api/users/export",
                                },
                            },
                            {
                                "type": "Button",
                                "label": "Invite Users",
                                "variant": "outline",
                                "onClick": {
                                    "type": "openModal",
                                    "modal": {
                                        "type": "Modal",
                                        "title": "Invite Users",
                                        "children": [
                                            {
                                                "type": "Text",
                                                "content": "Bulk invite functionality coming soon.",
                                                "variant": "muted",
                                            }
                                        ],
                                    },
                                },
                            },
                            {
                                "type": "Button",
                                "label": "View Logs",
                                "variant": "outline",
                                "onClick": {"type": "navigate", "to": "/admin/logs"},
                            },
                        ],
                    }
                ],
            },
        ],
    }


def get_users_list_spec() -> dict[str, Any]:
    """Generate the users list page UI spec."""
    return {
        "type": "Page",
        "title": "Users",
        "description": "Manage user accounts",
        "actions": [
            {
                "type": "Button",
                "label": "Add User",
                "variant": "primary",
                "icon": "+",
                "onClick": {
                    "type": "openModal",
                    "modal": {
                        "type": "Modal",
                        "title": "Add New User",
                        "size": "md",
                        "children": [
                            {
                                "type": "Form",
                                "endpoint": "/api/users",
                                "method": "POST",
                                "submitText": "Create User",
                                "cancelText": "Cancel",
                                "fields": [
                                    {
                                        "type": "TextField",
                                        "name": "email",
                                        "label": "Email",
                                        "inputType": "email",
                                        "required": True,
                                    },
                                    {
                                        "type": "TextField",
                                        "name": "password",
                                        "label": "Password",
                                        "inputType": "password",
                                        "required": True,
                                    },
                                    {
                                        "type": "Checkbox",
                                        "name": "email_verified",
                                        "checkboxLabel": "Mark email as verified",
                                    },
                                ],
                                "onSuccess": {"type": "refresh"},
                            }
                        ],
                    },
                },
            }
        ],
        "children": [
            {
                "type": "Card",
                "children": [
                    {
                        "type": "DataTable",
                        "endpoint": "/api/users",
                        "pagination": True,
                        "pageSize": 20,
                        "searchable": True,
                        "sortable": True,
                        "columns": [
                            {"key": "email", "label": "Email", "sortable": True},
                            {
                                "key": "email_verified",
                                "label": "Verified",
                                "type": "boolean",
                                "sortable": True,
                            },
                            {
                                "key": "two_factor_enabled",
                                "label": "2FA",
                                "type": "boolean",
                            },
                            {
                                "key": "created_at",
                                "label": "Created",
                                "type": "datetime",
                                "sortable": True,
                            },
                            {
                                "key": "updated_at",
                                "label": "Updated",
                                "type": "datetime",
                            },
                        ],
                        "rowActions": [
                            {
                                "type": "Button",
                                "label": "Edit",
                                "variant": "ghost",
                                "size": "sm",
                                "onClick": {
                                    "type": "navigate",
                                    "to": "/admin/users/{email}",
                                },
                            },
                            {
                                "type": "Button",
                                "label": "Delete",
                                "variant": "danger",
                                "size": "sm",
                                "onClick": {
                                    "type": "api",
                                    "method": "DELETE",
                                    "endpoint": "/api/users/{email}",
                                    "confirm": "Are you sure you want to delete this user?",
                                    "onSuccess": {"type": "refresh"},
                                },
                            },
                        ],
                        "emptyMessage": "No users found",
                    }
                ],
            }
        ],
    }


def get_user_edit_spec(user: dict[str, Any]) -> dict[str, Any]:
    """Generate the user edit page UI spec."""
    return {
        "type": "Page",
        "title": f"Edit User",
        "description": user.get("email", ""),
        "actions": [
            {
                "type": "Button",
                "label": "Back to Users",
                "variant": "outline",
                "onClick": {"type": "navigate", "to": "/admin/users"},
            }
        ],
        "children": [
            {
                "type": "Card",
                "title": "User Details",
                "children": [
                    {
                        "type": "Form",
                        "endpoint": f"/api/users/{user.get('email', '')}",
                        "method": "PUT",
                        "submitText": "Save Changes",
                        "initialValues": {
                            "email_verified": user.get("email_verified", False),
                            "two_factor_enabled": user.get("two_factor_enabled", False),
                        },
                        "fields": [
                            {
                                "type": "TextField",
                                "name": "email",
                                "label": "Email",
                                "inputType": "email",
                                "readOnly": True,
                                "placeholder": user.get("email", ""),
                            },
                            {
                                "type": "Checkbox",
                                "name": "email_verified",
                                "label": "Email Status",
                                "checkboxLabel": "Email verified",
                            },
                            {
                                "type": "Checkbox",
                                "name": "two_factor_enabled",
                                "label": "Two-Factor Auth",
                                "checkboxLabel": "2FA enabled",
                            },
                        ],
                        "onSuccess": {
                            "type": "navigate",
                            "to": "/admin/users",
                        },
                    }
                ],
            },
            {
                "type": "Card",
                "title": "Metadata",
                "className": "mt-6",
                "children": [
                    {
                        "type": "Row",
                        "gap": 24,
                        "children": [
                            {
                                "type": "Column",
                                "children": [
                                    {
                                        "type": "Text",
                                        "content": "Created",
                                        "variant": "small",
                                    },
                                    {
                                        "type": "Text",
                                        "content": user.get("created_at", "—"),
                                        "variant": "body",
                                    },
                                ],
                            },
                            {
                                "type": "Column",
                                "children": [
                                    {
                                        "type": "Text",
                                        "content": "Last Updated",
                                        "variant": "small",
                                    },
                                    {
                                        "type": "Text",
                                        "content": user.get("updated_at", "—"),
                                        "variant": "body",
                                    },
                                ],
                            },
                        ],
                    }
                ],
            },
            {
                "type": "Card",
                "title": "Danger Zone",
                "className": "mt-6",
                "children": [
                    {
                        "type": "Alert",
                        "variant": "warning",
                        "message": "Deleting a user is permanent and cannot be undone.",
                    },
                    {
                        "type": "Button",
                        "label": "Delete User",
                        "variant": "danger",
                        "className": "mt-4",
                        "onClick": {
                            "type": "api",
                            "method": "DELETE",
                            "endpoint": f"/api/users/{user.get('email', '')}",
                            "confirm": f"Are you sure you want to delete {user.get('email', 'this user')}?",
                            "onSuccess": {"type": "navigate", "to": "/admin/users"},
                        },
                    },
                ],
            },
        ],
    }

