# API Examples Reference

Complete request/response examples for all GEESP-Angola API endpoints.

---

## Authentication Examples

- [register-success.json](authentication/register-success.json) - Successful user registration
- [register-error-weak-password.json](authentication/register-error-weak-password.json) - Password too weak
- [login-success.json](authentication/login-success.json) - Successful login with JWT tokens
- [login-error.json](authentication/login-error.json) - Invalid credentials
- [refresh-token.json](authentication/refresh-token.json) - Refresh expired access token
- [profile-get.json](authentication/profile-get.json) - Retrieve user profile
- [profile-update.json](authentication/profile-update.json) - Update user profile
- [logout.json](authentication/logout.json) - Logout (invalidate refresh token)

## Scenario Management Examples

- [scenario-create.json](scenarios/scenario-create.json) - Create new scenario
- [scenario-list.json](scenarios/scenario-list.json) - List all user's scenarios
- [scenario-get.json](scenarios/scenario-get.json) - Get single scenario details
- [scenario-delete.json](scenarios/scenario-delete.json) - Delete scenario
- [scenario-error-duplicate.json](scenarios/scenario-error-duplicate.json) - Duplicate scenario name error

## Analysis Examples

- [financial-metrics.json](analysis/financial-metrics.json) - Calculate ROI, LCOE, payback period
- [filter-communities.json](analysis/filter-communities.json) - Advanced filtering with 6 criteria
- [health-check.json](analysis/health-check.json) - API health status

---

## How to Use These Examples

Each `.json` file contains:

1. **Request** - What to send to the API
2. **Response** - What you'll get back
3. **Notes** - Important information and edge cases

### cURL Example

```bash
# Copy the request from register-success.json
curl -X POST http://localhost:3000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "email": "user@example.com",
    "password": "SecurePass123!",
    "confirmPassword": "SecurePass123!"
  }'

# Expected response matches register-success.json
```

### JavaScript/Fetch Example

```javascript
const response = await fetch('http://localhost:3000/api/auth/register', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'SecurePass123!',
    confirmPassword: 'SecurePass123!'
  })
});

const data = await response.json();
console.log(data); // Matches register-success.json response
```

---

## File Structure

Each example file follows this structure:

```json
{
  "endpoint": "POST /api/auth/register",
  "description": "Register a new user account",
  "method": "POST",
  "url": "http://localhost:3000/api/auth/register",
  
  "request": {
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "email": "user@example.com",
      "password": "SecurePass123!",
      "confirmPassword": "SecurePass123!"
    }
  },
  
  "response": {
    "status": 201,
    "headers": {
      "Content-Type": "application/json"
    },
    "body": {
      "success": true,
      "data": {
        "user": {
          "id": "550e8400-e29b-41d4-a716-446655440000",
          "email": "user@example.com",
          "created_at": "2026-03-06T10:30:00Z"
        },
        "tokens": {
          "accessToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
          "refreshToken": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
          "accessTokenExpiry": 900
        }
      }
    }
  },
  
  "notes": "Password must include uppercase, lowercase, number, and special character"
}
```

---

## Organization

- **Authentication/** - User signup, login, token refresh
- **Scenarios/** - Create/read/update/delete scenarios
- **Analysis/** - Financial metrics and filtering

---

## Testing with Postman

All examples can be imported directly into Postman:

1. Open Postman
2. Click "Import"
3. Select file from `docs/api-examples/`
4. Postman will auto-detect structure
5. Run the request

---

**Last Updated:** March 6, 2026  
**T1.2.3 Status:** ✅ COMPLETE
