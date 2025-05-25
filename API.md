# Subscription Management Service - API Documentation

## Overview

This document provides comprehensive documentation for the Subscription Management Service API. The service provides RESTful endpoints for managing user subscriptions, plans, and authentication.

**Base URL:** `http://127.0.0.1:8000/api/v1`  
**Interactive Documentation:** `http://127.0.0.1:8000/docs`  
**Health Check:** `http://127.0.0.1:8000/health`

## Authentication

The API uses JWT (JSON Web Token) authentication. Include the token in the Authorization header:

```
Authorization: Bearer <your_jwt_token>
```

### Get Authentication Token

**Endpoint:** `POST /api/v1/auth/token`

**Request Body:**
```json
{
  "username": "user@example.com",
  "password": "your_password"
}
```

**Response:**
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer"
}
```

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/auth/token" \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test@example.com&password=testpassword"
```

## Plans Management

### Get All Plans

**Endpoint:** `GET /api/v1/plans/`  
**Authentication:** Required

**Response:**
```json
[
  {
    "id": 1,
    "name": "Basic",
    "description": "Basic subscription plan",
    "price": 9.99,
    "duration_days": 30,
    "created_at": "2025-05-26T03:00:00Z",
    "updated_at": "2025-05-26T03:00:00Z"
  },
  {
    "id": 2,
    "name": "Premium",
    "description": "Premium subscription plan",
    "price": 19.99,
    "duration_days": 30,
    "created_at": "2025-05-26T03:00:00Z",
    "updated_at": "2025-05-26T03:00:00Z"
  }
]
```

**Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/plans/" \
  -H "Authorization: Bearer <your_token>"
```

### Create Plan (Admin Only)

**Endpoint:** `POST /api/v1/plans/`  
**Authentication:** Required (Admin)

**Request Body:**
```json
{
  "name": "Enterprise",
  "description": "Enterprise subscription plan",
  "price": 49.99,
  "duration_days": 30
}
```

**Response:**
```json
{
  "id": 3,
  "name": "Enterprise",
  "description": "Enterprise subscription plan",
  "price": 49.99,
  "duration_days": 30,
  "created_at": "2025-05-26T03:00:00Z",
  "updated_at": "2025-05-26T03:00:00Z"
}
```

## Subscription Management

### Create Subscription

**Endpoint:** `POST /api/v1/subscriptions/`  
**Authentication:** Required

**Request Body:**
```json
{
  "user_id": 1,
  "plan_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "plan_id": 1,
  "status": "ACTIVE",
  "start_date": "2025-05-26T03:00:00Z",
  "end_date": "2025-06-25T03:00:00Z",
  "created_at": "2025-05-26T03:00:00Z",
  "updated_at": "2025-05-26T03:00:00Z",
  "plan": {
    "id": 1,
    "name": "Basic",
    "description": "Basic subscription plan",
    "price": 9.99,
    "duration_days": 30
  }
}
```

**Example:**
```bash
curl -X POST "http://127.0.0.1:8000/api/v1/subscriptions/" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"user_id": 1, "plan_id": 1}'
```

### Get User Subscription

**Endpoint:** `GET /api/v1/subscriptions/{userId}`  
**Authentication:** Required

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "plan_id": 1,
  "status": "ACTIVE",
  "start_date": "2025-05-26T03:00:00Z",
  "end_date": "2025-06-25T03:00:00Z",
  "created_at": "2025-05-26T03:00:00Z",
  "updated_at": "2025-05-26T03:00:00Z",
  "plan": {
    "id": 1,
    "name": "Basic",
    "description": "Basic subscription plan",
    "price": 9.99,
    "duration_days": 30
  }
}
```

**Example:**
```bash
curl -X GET "http://127.0.0.1:8000/api/v1/subscriptions/1" \
  -H "Authorization: Bearer <your_token>"
```

### Update Subscription

**Endpoint:** `PUT /api/v1/subscriptions/{userId}`  
**Authentication:** Required

**Request Body:**
```json
{
  "plan_id": 2,
  "status": "ACTIVE"
}
```

**Response:**
```json
{
  "id": 1,
  "user_id": 1,
  "plan_id": 2,
  "status": "ACTIVE",
  "start_date": "2025-05-26T03:00:00Z",
  "end_date": "2025-06-25T03:00:00Z",
  "created_at": "2025-05-26T03:00:00Z",
  "updated_at": "2025-05-26T03:00:00Z",
  "plan": {
    "id": 2,
    "name": "Premium",
    "description": "Premium subscription plan",
    "price": 19.99,
    "duration_days": 30
  }
}
```

**Example:**
```bash
curl -X PUT "http://127.0.0.1:8000/api/v1/subscriptions/1" \
  -H "Authorization: Bearer <your_token>" \
  -H "Content-Type: application/json" \
  -d '{"plan_id": 2, "status": "ACTIVE"}'
```

### Cancel Subscription

**Endpoint:** `DELETE /api/v1/subscriptions/{userId}`  
**Authentication:** Required

**Response:**
```json
{
  "message": "Subscription cancelled successfully",
  "subscription_id": 1
}
```

**Example:**
```bash
curl -X DELETE "http://127.0.0.1:8000/api/v1/subscriptions/1" \
  -H "Authorization: Bearer <your_token>"
```

## Health Check

### Service Health

**Endpoint:** `GET /health`  
**Authentication:** Not Required

**Response:**
```json
{
  "status": "healthy",
  "timestamp": 1748210647.614436,
  "services": {
    "database": "up",
    "redis": "up",
    "celery": "up"
  }
}
```

**Example:**
```bash
curl -X GET "http://127.0.0.1:8000/health"
```

## Status Codes

| Code | Description |
|------|-------------|
| 200 | OK - Request successful |
| 201 | Created - Resource created successfully |
| 400 | Bad Request - Invalid request data |
| 401 | Unauthorized - Authentication required |
| 403 | Forbidden - Insufficient permissions |
| 404 | Not Found - Resource not found |
| 409 | Conflict - Resource already exists |
| 422 | Unprocessable Entity - Validation error |
| 429 | Too Many Requests - Rate limit exceeded |
| 500 | Internal Server Error - Server error |

## Subscription Status Values

| Status | Description |
|--------|-------------|
| ACTIVE | Subscription is currently active |
| INACTIVE | Subscription is inactive |
| CANCELLED | Subscription has been cancelled |
| EXPIRED | Subscription has expired |

## Error Response Format

```json
{
  "detail": "Error message description",
  "error_code": "SPECIFIC_ERROR_CODE",
  "timestamp": "2025-05-26T03:00:00Z"
}
```

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- **Limit:** 100 requests per minute per IP
- **Headers:** Rate limit information is included in response headers
- **Exceeded:** Returns 429 status code when limit is exceeded

## Testing Credentials

For testing purposes, use these credentials:

**Regular User:**
- Email: `test@example.com`
- Password: `testpassword`

**Admin User:**
- Email: `admin@example.com`
- Password: `adminpassword`

## Interactive Documentation

Visit `http://127.0.0.1:8000/docs` for interactive API documentation with Swagger UI, where you can:

- Explore all endpoints
- Test API calls directly
- View request/response schemas
- Authenticate and try protected endpoints

## SDK Examples

### Python Example

```python
import requests

# Get authentication token
auth_response = requests.post(
    "http://127.0.0.1:8000/api/v1/auth/token",
    data={"username": "test@example.com", "password": "testpassword"}
)
token = auth_response.json()["access_token"]

# Set headers for authenticated requests
headers = {"Authorization": f"Bearer {token}"}

# Get all plans
plans = requests.get(
    "http://127.0.0.1:8000/api/v1/plans/",
    headers=headers
).json()

# Create subscription
subscription = requests.post(
    "http://127.0.0.1:8000/api/v1/subscriptions/",
    headers=headers,
    json={"user_id": 1, "plan_id": 1}
).json()
```

### JavaScript Example

```javascript
// Get authentication token
const authResponse = await fetch('http://127.0.0.1:8000/api/v1/auth/token', {
  method: 'POST',
  headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
  body: 'username=test@example.com&password=testpassword'
});
const { access_token } = await authResponse.json();

// Set headers for authenticated requests
const headers = { 'Authorization': `Bearer ${access_token}` };

// Get all plans
const plansResponse = await fetch('http://127.0.0.1:8000/api/v1/plans/', { headers });
const plans = await plansResponse.json();

// Create subscription
const subscriptionResponse = await fetch('http://127.0.0.1:8000/api/v1/subscriptions/', {
  method: 'POST',
  headers: { ...headers, 'Content-Type': 'application/json' },
  body: JSON.stringify({ user_id: 1, plan_id: 1 })
});
const subscription = await subscriptionResponse.json();
```

## Support

For technical support or questions about the API:

- **Documentation:** `http://127.0.0.1:8000/docs`
- **Health Check:** `http://127.0.0.1:8000/health`
- **Repository:** Check the README.md for setup instructions 