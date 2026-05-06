# 🚨 Error Code Reference Guide

**Complete documentation of all possible API error codes, HTTP statuses, and solutions**

---

## HTTP Status Code Summary

| Code | Name | Meaning | Common Causes |
|------|------|---------|---------------|
| **200** | OK | Request successful | ✅ Normal operation |
| **201** | Created | Resource created | ✅ New user/scenario |
| **400** | Bad Request | Invalid input | ❌ Missing field, validation error |
| **401** | Unauthorized | Authentication failed | ❌ Invalid token, expired token |
| **403** | Forbidden | No permission | ❌ Insufficient role |
| **404** | Not Found | Resource doesn't exist | ❌ Wrong ID |
| **409** | Conflict | State conflict | ❌ Duplicate email |
| **429** | Too Many Requests | Rate limit exceeded | ❌ Too many login attempts |
| **500** | Server Error | Unexpected error | ❌ Database down, bug |

---

## Authentication Errors (4xx)

### 401 - Invalid Credentials
```
Error Code: AUTH_001
HTTP: 401 Unauthorized
Message: "Invalid email or password"

Causes:
✗ Email not found in database
✗ Password doesn't match hash
✗ User account deleted

Solution:
→ Verify email is spelled correctly
→ Check password is correct
→ If forgot password: implement password reset (T2+)

Example Response:
{
  "success": false,
  "error": "AUTH_001",
  "message": "Invalid email or password"
}
```

### 401 - Token Expired
```
Error Code: AUTH_002
HTTP: 401 Unauthorized
Message: "Token has expired"

Causes:
✗ Access token > 15 minutes old
✗ Refresh token > 7 days old

Solution:
→ If access token expired: Call POST /api/auth/refresh with refreshToken
→ If refresh token expired: User must login again (POST /api/auth/login)

Example Response:
{
  "success": false,
  "error": "AUTH_002",
  "message": "Token has expired. Use refresh endpoint or login again"
}
```

### 401 - Invalid Token
```
Error Code: AUTH_003
HTTP: 401 Unauthorized
Message: "Invalid or malformed token"

Causes:
✗ Token corrupted during transmission
✗ Wrong format in Authorization header
✗ Token from different service

Solution:
→ Verify Authorization header format: "Bearer <token>"
→ Don't include quotes around token
→ Login again to get fresh token

Example Response:
{
  "success": false,
  "error": "AUTH_003",
  "message": "Invalid token format or signature"
}
```

### 401 - Missing Token
```
Error Code: AUTH_004
HTTP: 401 Unauthorized
Message: "Authorization token required"

Causes:
✗ No Authorization header provided
✗ Authorization header empty
✗ Accessing protected endpoint without token

Solution:
→ Add Authorization header: -H "Authorization: Bearer <token>"
→ Get token from login endpoint first
→ Check header is not misspelled

Example Response:
{
  "success": false,
  "error": "AUTH_004",
  "message": "Missing Authorization header"
}
```

### 403 - Insufficient Permissions
```
Error Code: AUTH_005
HTTP: 403 Forbidden
Message: "You do not have permission to perform this action"

Causes:
✗ User role too low (VIEWER can't edit)
✗ Trying to access another user's private data
✗ Admin-only endpoint

Solution:
→ Request appropriate role from admin
→ Only access your own scenarios
→ Check TIER 2.1.1 for RBAC documentation

Example Response:
{
  "success": false,
  "error": "AUTH_005",
  "message": "Insufficient permissions. Required role: ADMIN"
}
```

---

## Validation Errors (400)

### 400 - Missing Required Field
```
Error Code: VALIDATION_001
HTTP: 400 Bad Request
Message: "Field required: <fieldname>"

Causes:
✗ Email field missing in registration
✗ Password field missing in login
✗ Required JSON field absent

Solution:
→ Check which field is missing (see error message)
→ Add field to request body
→ Validate JSON syntax

Example Response:
{
  "success": false,
  "error": "VALIDATION_001",
  "message": "Field required: email",
  "details": {
    "field": "email"
  }
}
```

### 400 - Invalid Email Format
```
Error Code: VALIDATION_002
HTTP: 400 Bad Request
Message: "Invalid email format"

Causes:
✗ Missing @ symbol
✗ No domain (.com, .org, etc)
✗ Invalid characters

Valid formats:
✓ user@example.com
✓ john.doe@company.co.uk
✓ info+test@domain.org

Solution:
→ Use standard email format
→ Include @ and domain
→ Check for typos

Example Response:
{
  "success": false,
  "error": "VALIDATION_002",
  "message": "Invalid email format",
  "details": {
    "field": "email",
    "format": "user@domain.com"
  }
}
```

### 400 - Weak Password
```
Error Code: VALIDATION_003
HTTP: 400 Bad Request
Message: "Password does not meet strength requirements"

Causes:
✗ Password < 8 characters
✗ Missing uppercase letter
✗ Missing lowercase letter
✗ Missing number
✗ Missing special character

Requirements:
✓ 8+ characters minimum
✓ At least 1 uppercase (A-Z)
✓ At least 1 lowercase (a-z)
✓ At least 1 number (0-9)
✓ At least 1 special char (!@#$%^&*)

Solution:
→ See 'feedback' array in error for specifics
→ Check password strength: 0-30=Weak, 31-60=Fair, 61-80=Good, 81-100=Strong
→ Example strong password: "MyPass2026!@#"

Example Response:
{
  "success": false,
  "error": "VALIDATION_003",
  "message": "Password does not meet strength requirements",
  "details": {
    "score": 25,
    "feedback": [
      "Password is too short (minimum 8 characters)",
      "Password must contain an uppercase letter",
      "Password must contain a number",
      "Password must contain a special character"
    ]
  }
}
```

### 400 - Invalid JSON
```
Error Code: VALIDATION_004
HTTP: 400 Bad Request
Message: "Invalid JSON format"

Causes:
✗ Malformed JSON (missing quote, comma)
✗ Wrong data type (number as string)
✗ Syntax error in body

Solution:
→ Validate JSON with jsonlint.com
→ Check for matching quotes and braces
→ Example valid JSON:
   {
     "email": "user@example.com",
     "password": "Pass123!"
   }

Example Response:
{
  "success": false,
  "error": "VALIDATION_004",
  "message": "Invalid JSON in request body"
}
```

### 400 - Invalid Weights Sum
```
Error Code: VALIDATION_005
HTTP: 400 Bad Request
Message: "Weights must sum to 1.0"

Causes:
✗ Weights sum to 0.95 (too low)
✗ Weights sum to 1.05 (too high)
✗ Missing one of 6 criteria

Required weights (must total 1.0):
- ghi: 0.0 - 1.0
- terrain: 0.0 - 1.0
- population: 0.0 - 1.0
- grid_distance: 0.0 - 1.0
- ndvi: 0.0 - 1.0
- nightlights: 0.0 - 1.0

Solution:
→ Adjust weights to sum to 1.0
→ Example: 0.25 + 0.15 + 0.20 + 0.20 + 0.15 + 0.05 = 1.0
→ Use calculator to verify sum

Example Response:
{
  "success": false,
  "error": "VALIDATION_005",
  "message": "Weights sum to 0.95, must be 1.0",
  "details": {
    "provided_sum": 0.95,
    "required_sum": 1.0
  }
}
```

---

## Resource Errors (4xx)

### 404 - Scenario Not Found
```
Error Code: SCENARIO_001
HTTP: 404 Not Found
Message: "Scenario not found"

Causes:
✗ Scenario ID doesn't exist
✗ Scenario was deleted
✗ Wrong scenario ID

Solution:
→ Get List of scenarios: GET /api/scenarios
→ Copy correct scenario ID
→ Verify you have access to this scenario

Example Response:
{
  "success": false,
  "error": "SCENARIO_001",
  "message": "Scenario not found",
  "details": {
    "scenario_id": "123e4567-e89b-12d3-a456-426614174000"
  }
}
```

### 409 - Email Already Exists
```
Error Code: USER_001
HTTP: 409 Conflict
Message: "Email already registered"

Causes:
✗ Account with email already exists
✗ User tried to register twice with same email

Solution:
→ Use different email address
→ If you forgot password: Implement password reset (T2+)
→ Check if you already have account

Example Response:
{
  "success": false,
  "error": "USER_001",
  "message": "Email already registered",
  "details": {
    "email": "user@example.com"
  }
}
```

### 409 - Scenario Name Exists
```
Error Code: SCENARIO_002
HTTP: 409 Conflict
Message: "Scenario name already exists"

Causes:
✗ User already has scenario with this name
✗ Name must be unique per user

Solution:
→ Use different scenario name
→ Example: "Climate 2026" → "Climate 2026 v2"
→ Delete old scenario if no longer needed

Example Response:
{
  "success": false,
  "error": "SCENARIO_002",
  "message": "Scenario name already exists",
  "details": {
    "name": "Climate-First Policy 2026"
  }
}
```

---

## Rate Limiting Errors (429)

### 429 - Too Many Login Attempts
```
Error Code: RATE_LIMIT_001
HTTP: 429 Too Many Requests
Message: "Too many login attempts. Try again in 15 minutes"

Causes:
✗ 5+ failed login attempts in 15 minutes
✗ Brute-force attack protection triggered

Solution:
→ Wait 15 minutes before trying again
→ Verify email and password are correct
→ Check CAPS LOCK
→ Implement password reset (T2+)

Response Headers:
X-RateLimit-Limit: 5
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 2026-03-06T11:00:00Z

Example Response:
{
  "success": false,
  "error": "RATE_LIMIT_001",
  "message": "Too many login attempts. Try again after 15 minutes",
  "details": {
    "retry_after_seconds": 900
  }
}
```

### 429 - Too Many Registration Attempts
```
Error Code: RATE_LIMIT_002
HTTP: 429 Too Many Requests
Message: "Too many registration attempts. Try again in 1 hour"

Causes:
✗ 3+ registration attempts in 1 hour
✗ Spam prevention triggered

Solution:
→ Wait 1 hour before registering again
→ Use different email if needed
→ Check confirmation email (if implemented)

Example Response:
{
  "success": false,
  "error": "RATE_LIMIT_002",
  "message": "Too many registration attempts",
  "details": {
    "retry_after_seconds": 3600
  }
}
```

### 429 - API Rate Limit Exceeded
```
Error Code: RATE_LIMIT_003
HTTP: 429 Too Many Requests
Message: "API rate limit exceeded"

Causes:
✗ 1000+ requests per hour (global limit)
✗ 100+ requests per hour on heavy endpoints (/filter-communities)

Solution:
→ Reduce request frequency
→ Implement caching on client
→ Batch requests where possible
→ For legitimate high-volume: Contact support

Response Headers:
X-RateLimit-Limit: 1000
X-RateLimit-Remaining: 0
X-RateLimit-Reset: 2026-03-06T11:00:00Z

Example Response:
{
  "success": false,
  "error": "RATE_LIMIT_003",
  "message": "Rate limit exceeded. Max 1000 requests/hour",
  "details": {
    "limit": 1000,
    "window_seconds": 3600
  }
}
```

---

## Server Errors (5xx)

### 500 - Internal Server Error
```
Error Code: SERVER_001
HTTP: 500 Internal Server Error
Message: "Internal server error"

Causes:
✗ Database connection failed
✗ Unexpected exception in code
✗ File system error
✗ Out of memory

Solution:
→ Try request again (may be temporary)
→ Contact support with error ID
→ Check server status page
→ Check system logs

Example Response:
{
  "success": false,
  "error": "SERVER_001",
  "message": "Internal server error",
  "details": {
    "error_id": "5a3f8b2c-e29b-41d4-a716-446655440000",
    "timestamp": "2026-03-06T10:30:00Z"
  }
}

What to do:
→ Save the error_id
→ Report to support team with:
  - Error ID
  - Endpoint you were calling
  - Request data (sanitized)
  - Time it happened
```

### 503 - Service Unavailable
```
Error Code: SERVER_002
HTTP: 503 Service Unavailable
Message: "Service temporarily unavailable"

Causes:
✗ Server maintenance
✗ Database down
✗ High load/scaling happening
✗ Deployment in progress

Solution:
→ Wait 5-10 minutes
→ Check status page: https://status.geesp-angola.com
→ Retry with exponential backoff
→ Contact support if persists > 1 hour

Example Response:
{
  "success": false,
  "error": "SERVER_002",
  "message": "Service temporarily unavailable",
  "details": {
    "estimated_recovery": "2026-03-06T10:45:00Z"
  }
}
```

---

## Error Response Format

All error responses follow this standard format:

```json
{
  "success": false,
  "error": "ERROR_CODE_001",
  "message": "Human readable error message",
  "details": {
    // Additional context-specific fields
    // Examples: field name, validation feedback, limits, etc.
  }
}
```

---

## Troubleshooting Decision Tree

```
You get an error...
│
├─ HTTP 400?
│  └─ Check 'message' and 'details'
│     └─ Missing field? Add it
│     └─ Invalid format? Fix format
│     └─ Validation error? See VALIDATION_xxx codes above
│
├─ HTTP 401?
│  └─ Authorization issue
│     └─ Token expired? Use refresh endpoint (AUTH_002)
│     └─ Wrong password? Verify credentials (AUTH_001)
│     └─ No Authorization header? Add it (AUTH_004)
│
├─ HTTP 403?
│  └─ Permission issue (AUTH_005)
│     └─ Request role upgrade from admin
│     └─ Check you're accessing own data
│
├─ HTTP 404?
│  └─ Resource not found
│     └─ Check scenario/user ID exists
│     └─ Get list and verify ID
│
├─ HTTP 409?
│  └─ Conflict (duplicate, state error)
│     └─ Use different email (USER_001)
│     └─ Use different scenario name (SCENARIO_002)
│
├─ HTTP 429?
│  └─ Rate limit (too many requests)
│     └─ Wait before retrying
│     └─ Check X-RateLimit-Reset header
│
└─ HTTP 500?
   └─ Server error
      └─ Retry after 10 seconds
      └─ Contact support with error_id
```

---

## Quick Reference by Scenario

### "I can't login"
→ Check: AUTH_001 (wrong password), AUTH_002 (token expired), RATE_LIMIT_001 (too many attempts)

### "API says missing field"
→ Check: VALIDATION_001, verify all required fields in request

### "Email exists error"
→ Check: USER_001, use different email or login instead

### "Scenario not found"
→ Check: SCENARIO_001, get list first then use correct ID

### "Token invalid"
→ Check: AUTH_002 (refresh), AUTH_003 (malformed), AUTH_004 (missing)

### "Permission denied"
→ Check: AUTH_005, request upgrade or check you own the resource

### "Too many requests"
→ Check: RATE_LIMIT_001/002/003, wait before retrying

### "Server down"
→ Check: SERVER_001/002, retry after 10 seconds or wait for recovery

---

## Monitoring & Alerting

If you see errors > 5% of requests:
1. Check server logs
2. Check database connection
3. Check rate limiting not too aggressive
4. Contact ops team

---

**Last Updated:** March 6, 2026  
**T1.2.4 Status:** ✅ COMPLETE

**Next:** T2.1 User Management (RBAC, Profiles, Sharing, Admin Dashboard)
