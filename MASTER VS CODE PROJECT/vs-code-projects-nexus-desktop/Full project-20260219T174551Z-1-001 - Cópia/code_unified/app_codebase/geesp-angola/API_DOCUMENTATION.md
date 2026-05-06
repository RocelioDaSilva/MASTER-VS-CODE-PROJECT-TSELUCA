# 📚 API DOCUMENTATION
## GEESP-Angola Backend REST API Reference
### FastAPI + Async Job Queue

---

## 🌐 API BASE URL

```
Development:  http://localhost:8000
Production:   https://api.geesp-angola.example.com

Interactive Docs: http://localhost:8000/docs
```

---

## 🔑 AUTHENTICATION

All endpoints (except `/health`) require authentication via JWT token.

### Login

**Endpoint**: `POST /auth/login`

**Request**:
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

**Response** (200):
```json
{
  "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
  "token_type": "bearer",
  "expires_in": 3600
}
```

### Header Format

Include token in all requests:
```http
Authorization: Bearer <your_token>
```

---

## 📋 ENDPOINTS

### 1️⃣ Health & Status

#### GET `/health`
Service health check (no auth required)

**Response** (200):
```json
{
  "status": "healthy",
  "timestamp": "2026-03-07T10:30:00Z",
  "version": "1.0.0"
}
```

**Error** (503):
```json
{
  "status": "unhealthy",
  "reason": "Database connection failed"
}
```

---

### 2️⃣ Layer Management

#### GET `/layers`
List all available spatial layers

**Query Parameters**:
- `category` (optional): Filter by category (solar, irradiance, terrain)
- `resolution` (optional): Filter by resolution (30, 100, 500)

**Response** (200):
```json
{
  "layers": [
    {
      "id": "solar_potential",
      "name": "Solar Potential Index",
      "category": "solar",
      "resolution": 30,
      "units": "kWh/m²/day",
      "description": "Average daily solar irradiance"
    },
    {
      "id": "terrain_slope",
      "name": "Terrain Slope",
      "category": "terrain",
      "resolution": 100,
      "units": "degrees",
      "description": "Slope angle in degrees"
    }
  ],
  "total": 2
}
```

#### GET `/layers/{layer_id}`
Get specific layer details

**Path Parameters**:
- `layer_id` (required): Layer identifier

**Response** (200):
```json
{
  "id": "solar_potential",
  "name": "Solar Potential Index",
  "category": "solar",
  "resolution": 30,
  "units": "kWh/m²/day",
  "description": "Average daily solar irradiance",
  "bounds": {
    "north": -4.0,
    "south": -18.0,
    "east": 24.0,
    "west": 11.0
  },
  "data_type": "float32",
  "metadata": {
    "source": "Google Earth Engine",
    "last_updated": "2026-01-15"
  }
}
```

---

### 3️⃣ MCDA Analysis (Synchronous)

#### POST `/mcda`
Compute MCDA ranking synchronously (for small datasets)

**Request**:
```json
{
  "alternatives": [
    {
      "name": "Site A",
      "criteria": {
        "solar_potential": 0.85,
        "accessibility": 0.72,
        "environmental_impact": 0.65
      }
    },
    {
      "name": "Site B",
      "criteria": {
        "solar_potential": 0.92,
        "accessibility": 0.58,
        "environmental_impact": 0.78
      }
    }
  ],
  "weights": {
    "solar_potential": 0.5,
    "accessibility": 0.3,
    "environmental_impact": 0.2
  },
  "method": "weighted_sum"
}
```

**Response** (200):
```json
{
  "status": "success",
  "rankings": [
    {
      "rank": 1,
      "alternative": "Site B",
      "score": 0.86
    },
    {
      "rank": 2,
      "alternative": "Site A",
      "score": 0.76
    }
  ],
  "computation_time_ms": 125,
  "timestamp": "2026-03-07T10:35:00Z"
}
```

**Error** (400):
```json
{
  "error": "Invalid criteria weights",
  "detail": "Weights must sum to 1.0"
}
```

#### GET `/mcda/inputs`
Get MCDA input schema and constraints

**Response** (200):
```json
{
  "methods": ["weighted_sum", "topsis", "vikor"],
  "criteria": {
    "solar_potential": {
      "min": 0.0,
      "max": 1.0,
      "unit": "normalized"
    },
    "accessibility": {
      "min": 0.0,
      "max": 1.0,
      "unit": "normalized"
    },
    "environmental_impact": {
      "min": 0.0,
      "max": 1.0,
      "unit": "normalized"
    }
  },
  "max_alternatives": 1000
}
```

---

### 4️⃣ Async Job Queue (for Long-Running Tasks)

#### POST `/mcda/jobs`
Submit MCDA analysis to async job queue

**Use for**: Large datasets, complex analyses

**Request**:
```json
{
  "name": "Angola Sites Analysis",
  "dataset": {
    "alternatives": [...],  // Large array
    "weights": {...},
    "method": "topsis"
  },
  "priority": "normal"
}
```

**Response** (202 Accepted):
```json
{
  "job_id": "job_12345abcde",
  "status": "queued",
  "created_at": "2026-03-07T10:35:00Z",
  "estimated_time_seconds": 120
}
```

#### GET `/mcda/jobs/{job_id}`
Get job status and results

**Path Parameters**:
- `job_id` (required): Job identifier from submission

**Response** (200) - Still Processing:
```json
{
  "job_id": "job_12345abcde",
  "status": "processing",
  "progress": 65,
  "progress_message": "Computing rankings...",
  "created_at": "2026-03-07T10:35:00Z",
  "started_at": "2026-03-07T10:35:05Z",
  "estimated_completion": "2026-03-07T10:36:00Z"
}
```

**Response** (200) - Complete:
```json
{
  "job_id": "job_12345abcde",
  "status": "completed",
  "progress": 100,
  "created_at": "2026-03-07T10:35:00Z",
  "started_at": "2026-03-07T10:35:05Z",
  "completed_at": "2026-03-07T10:36:15Z",
  "computation_time_ms": 75000,
  "results": {
    "rankings": [
      {
        "rank": 1,
        "alternative": "Site B",
        "score": 0.86
      }
    ]
  }
}
```

**Response** (200) - Failed:
```json
{
  "job_id": "job_12345abcde",
  "status": "failed",
  "error": "Invalid criteria weights",
  "error_detail": "Weights must sum to 1.0",
  "failed_at": "2026-03-07T10:36:15Z"
}
```

#### GET `/mcda/jobs`
List all jobs (with pagination)

**Query Parameters**:
- `status` (optional): Filter by status (queued, processing, completed, failed)
- `limit` (optional): Maximum results (default: 20, max: 100)
- `offset` (optional): Pagination offset (default: 0)
- `sort` (optional): Sort by field (created_at, status)

**Response** (200):
```json
{
  "jobs": [
    {
      "job_id": "job_12345abcde",
      "status": "completed",
      "created_at": "2026-03-07T10:35:00Z",
      "computation_time_ms": 75000
    },
    {
      "job_id": "job_54321fedcba",
      "status": "processing",
      "created_at": "2026-03-07T10:34:00Z",
      "progress": 45
    }
  ],
  "total": 42,
  "limit": 20,
  "offset": 0
}
```

#### GET `/mcda/stats`
Queue statistics and performance metrics

**Response** (200):
```json
{
  "queue_size": 5,
  "jobs_completed_today": 127,
  "jobs_failed_today": 3,
  "average_computation_time_ms": 45000,
  "max_computation_time_ms": 180000,
  "min_computation_time_ms": 5000,
  "processing_capacity": "75%",
  "estimated_wait_time_ms": 30000
}
```

---

### 5️⃣ Batch Processing

#### POST `/batch/process`
Process multiple analyses in batch (through job queue)

**Request**:
```json
{
  "name": "Batch Analysis 2026",
  "jobs": [
    {
      "job_name": "Region A Analysis",
      "dataset": {...}
    },
    {
      "job_name": "Region B Analysis",
      "dataset": {...}
    }
  ],
  "run_sequential": false
}
```

**Response** (202 Accepted):
```json
{
  "batch_id": "batch_abc123",
  "status": "submitted",
  "total_jobs": 2,
  "job_ids": ["job_001", "job_002"],
  "created_at": "2026-03-07T10:35:00Z"
}
```

#### GET `/batch/{batch_id}`
Get batch status

**Response** (200):
```json
{
  "batch_id": "batch_abc123",
  "status": "processing",
  "total_jobs": 2,
  "completed": 1,
  "failed": 0,
  "progress": 50,
  "jobs": [
    {"job_id": "job_001", "status": "completed"},
    {"job_id": "job_002", "status": "processing"}
  ]
}
```

---

## 🔄 Request/Response Models

### MCDARequest
```python
{
  "alternatives": List[Alternative],
  "weights": Dict[str, float],
  "method": "weighted_sum" | "topsis" | "vikor",
  "metadata": Optional[Dict]
}
```

### MCDAResponse
```python
{
  "status": "success" | "error",
  "rankings": List[Ranking],
  "computation_time_ms": int,
  "timestamp": datetime
}
```

### JobData
```python
{
  "job_id": str,
  "status": "queued" | "processing" | "completed" | "failed",
  "progress": int (0-100),
  "created_at": datetime,
  "started_at": Optional[datetime],
  "completed_at": Optional[datetime],
  "error": Optional[str],
  "results": Optional[Any]
}
```

---

## ❌ ERROR RESPONSES

### HTTP Status Codes

| Code | Meaning | Example |
|------|---------|---------|
| 200 | Success | Request completed |
| 202 | Accepted | Job submitted to queue |
| 400 | Bad Request | Invalid parameters |
| 401 | Unauthorized | Missing/invalid token |
| 403 | Forbidden | No permission |
| 404 | Not Found | Resource doesn't exist |
| 500 | Server Error | Internal error |
| 503 | Service Unavailable | System overloaded |

### Error Response Format

```json
{
  "error": "Invalid criteria weights",
  "code": "INVALID_WEIGHTS",
  "detail": "Weights must sum to 1.0",
  "timestamp": "2026-03-07T10:35:00Z",
  "request_id": "req_12345"
}
```

---

## 🔐 SECURITY

### Rate Limiting
- 100 requests per minute per user
- Batch jobs: 5 concurrent per user

### Token Expiration
- Access tokens: 1 hour
- Refresh tokens: 7 days

### CORS Policy
```
Allowed Origins: https://yourdomain.com
Allowed Methods: GET, POST, PUT, DELETE
Allowed Headers: Authorization, Content-Type
```

---

## 📊 EXAMPLES

### Example 1: Simple MCDA Analysis

```bash
curl -X POST http://localhost:8000/mcda \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "alternatives": [
      {
        "name": "Site A",
        "criteria": {
          "solar_potential": 0.85,
          "accessibility": 0.72
        }
      }
    ],
    "weights": {
      "solar_potential": 0.6,
      "accessibility": 0.4
    },
    "method": "weighted_sum"
  }'
```

### Example 2: Submit Long-Running Job

```bash
curl -X POST http://localhost:8000/mcda/jobs \
  -H "Authorization: Bearer <token>" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Large Region Analysis",
    "dataset": {...},
    "priority": "normal"
  }'
```

Returns: `{"job_id": "job_abc123"}`

### Example 3: Check Job Status

```bash
curl http://localhost:8000/mcda/jobs/job_abc123 \
  -H "Authorization: Bearer <token>"
```

---

## 🧪 TESTING ENDPOINTS

### Using curl

```bash
# Check health
curl http://localhost:8000/health

# Get layers
curl -X GET http://localhost:8000/layers \
  -H "Authorization: Bearer <token>"

# Run MCDA analysis
curl -X POST http://localhost:8000/mcda \
  -H "Authorization: Bearer <token>"
  -H "Content-Type: application/json" \
  -d '@mcda_request.json'
```

### Using Python requests

```python
import requests

headers = {"Authorization": f"Bearer {token}"}

# Health check
response = requests.get("http://localhost:8000/health")

# Get layers
response = requests.get("http://localhost:8000/layers", headers=headers)
print(response.json())

# MCDA analysis
data = {
  "alternatives": [...],
  "weights": {...},
  "method": "weighted_sum"
}
response = requests.post("http://localhost:8000/mcda", json=data, headers=headers)
print(response.json())
```

### Using JavaScript/Fetch

```javascript
const token = "your_token";
const headers = {
  "Authorization": `Bearer ${token}`,
  "Content-Type": "application/json"
};

// Health check
fetch("http://localhost:8000/health")
  .then(r => r.json())
  .then(data => console.log(data));

// Get layers
fetch("http://localhost:8000/layers", { headers })
  .then(r => r.json())
  .then(data => console.log(data));

// MCDA analysis
const mcda_data = {
  alternatives: [...],
  weights: {...},
  method: "weighted_sum"
};

fetch("http://localhost:8000/mcda", {
  method: "POST",
  headers,
  body: JSON.stringify(mcda_data)
})
.then(r => r.json())
.then(data => console.log(data));
```

---

## 📖 SWAGGER/OPENAPI

Interactive API documentation available at:
```
http://localhost:8000/docs          # Swagger UI
http://localhost:8000/redoc         # ReDoc
http://localhost:8000/openapi.json  # OpenAPI JSON
```

---

## 🚀 PERFORMANCE TIPS

- **Use async endpoints** for large datasets (> 1000 items)
- **Batch multiple jobs** together for efficiency
- **Cache layer data** using Content-Type: application/ndjson
- **Monitor job queue stats** (`/mcda/stats`) before submitting
- **Use pagination** when listing jobs (`?limit=50&offset=0`)

---

## ✅ CHANGELOG

### Version 1.0.0 (2026-03-07)
- Initial API release
- Sync MCDA endpoint
- Async job queue
- Batch processing
- Authentication

---

**API Documentation Complete** ✅

