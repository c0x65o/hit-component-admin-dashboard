# Hit Component: Admin Dashboard

A Server-Driven UI component that provides an admin dashboard for managing users and viewing application statistics.

## Overview

This component uses Hit's Server-Driven UI system. Instead of shipping React components, it returns UI specifications that the Hit SDK renders on the frontend.

## How It Works

```
┌──────────────────────────────────────────────────────────────┐
│                  Admin Dashboard Component                    │
│                                                               │
│   GET /ui/dashboard → Returns UI Spec (JSON)                 │
│   GET /ui/users     → Returns UI Spec (JSON)                 │
│   GET /api/users    → Returns Data (JSON)                    │
│                                                               │
└──────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌──────────────────────────────────────────────────────────────┐
│                    Host Frontend App                          │
│                                                               │
│   import { HitUIRenderer } from '@hit/sdk';                   │
│                                                               │
│   <HitUIRenderer                                              │
│     spec={dashboardSpec}                                      │
│     apiBase="/admin"                                          │
│   />                                                          │
│                                                               │
└──────────────────────────────────────────────────────────────┘
```

## Usage

### 1. Add to your project's hit.yaml

```yaml
components:
  - name: admin-dashboard
    version: 1.0
```

### 2. Use in your frontend

```tsx
import { HitUIFromEndpoint } from '@hit/sdk';
import '@hit/sdk/ui/styles.css';

function AdminDashboard() {
  return (
    <Layout>
      <HitUIFromEndpoint
        endpoint="/ui/dashboard"
        apiBase="/admin"
        onNavigate={(path) => router.push(path)}
      />
    </Layout>
  );
}
```

### 3. Theme customization

Override CSS variables in your app:

```css
:root {
  --hit-primary: #8b5cf6;
  --hit-bg: #0f172a;
  --hit-text: #f1f5f9;
}
```

## API Endpoints

### UI Spec Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /ui/dashboard` | Main dashboard page spec |
| `GET /ui/users` | Users list page spec |
| `GET /ui/users/{email}` | User edit page spec |

### Data Endpoints

| Endpoint | Description |
|----------|-------------|
| `GET /api/users` | List all users |
| `GET /api/users/{email}` | Get user by email |
| `PUT /api/users/{email}` | Update user |
| `DELETE /api/users/{email}` | Delete user |
| `GET /api/stats` | Dashboard statistics |

## Dependencies

- **auth module**: Required for user data

## Development

```bash
# Install dependencies
uv sync

# Run locally
uv run uvicorn app.main:app --reload --port 8200

# Set auth module URL
export HIT_AUTH_URL=http://localhost:8001
```

