# 🚀 GEESP-Angola REST API Tutorial

**Version**: 1.0 | **Date**: February 2026  
**API Base URL**: `http://localhost:8000` (development) or `https://api.geesp-angola.org` (production)

---

## **Quick Start (5 minutes)**

### **1. Start the API locally**
```bash
cd "Coding parts/geesp-angola"
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install fastapi uvicorn numpy pandas
python -m uvicorn scripts.api:app --reload
```

### **2. Open interactive docs**
```
http://localhost:8000/docs  ← Swagger UI (try-it-out)
http://localhost:8000/redoc ← ReDoc (read-only formatting)
```

### **3. Try your first API call**
```bash
curl http://localhost:8000/health
# Response:
# {"status":"ok","timestamp":"2026-02-10T14:30:00.123456","version":"1.0.0","available_layers":["mapa_irradiacao","mapa_populacao",...]}
```

---

## **API Endpoints Reference**

### **Health Check**
```http
GET /health
```
**Purpose**: Verify API is running and check available resources  
**Response** (200 OK):
```json
{
  "status": "ok",
  "timestamp": "2026-02-10T14:30:00.123456",
  "version": "1.0.0",
  "available_layers": [
    "mapa_irradiacao",
    "mapa_populacao",
    "mapa_distanciarede",
    "mapa_declividade",
    "mapa_ndvi"
  ]
}
```

---

### **List Available Layers**
```http
GET /layers
```
**Purpose**: Get detailed info about raster layers available for analysis  
**Response** (200 OK):
```json
{
  "available": [
    "mapa_irradiacao",
    "mapa_populacao",
    "mapa_distanciarede",
    "mapa_declividade",
    "mapa_ndvi"
  ],
  "count": 5,
  "descriptions": {
    "mapa_irradiacao": "Solar irradiance (kWh/m²/day) - higher = better for solar",
    "mapa_populacao": "Population density (people/km²) - higher = more demand",
    "mapa_distanciarede": "Distance to electrical grid (km) - lower = better",
    "mapa_declividade": "Slope (degrees) - low/moderate = easier installation",
    "mapa_ndvi": "Vegetation index (-1 to 1) - moderate = suitable land cover"
  }
}
```

---

### **Compute MCDA Weighted Overlay**
```http
POST /mcda
Content-Type: application/json

{
  "weights": {
    "mapa_irradiacao": 0.35,
    "mapa_populacao": 0.25,
    "mapa_distanciarede": 0.20,
    "mapa_declividade": 0.10,
    "mapa_ndvi": 0.10
  }
}
```

**Purpose**: Compute weighted suitability overlay from raster maps  
**Request Body**:
- `weights` (object, required): Dictionary mapping layer names to weights (0-1 range)
  - Will be automatically normalized if they don't sum to 1.0
  - All layers are optional; only specified layers used in computation

**Response** (200 OK):
```json
{
  "status": "success",
  "summary": {
    "min": 0.15,
    "max": 0.89,
    "mean": 0.62,
    "std": 0.15
  },
  "saved_path": "/path/to/data/processed/api_mapa_aptidao.npy",
  "weights_used": {
    "mapa_irradiacao": 0.35,
    "mapa_populacao": 0.25,
    "mapa_distanciarede": 0.20,
    "mapa_declividade": 0.10,
    "mapa_ndvi": 0.10
  },
  "timestamp": "2026-02-10T14:30:00.123456"
}
```

**Error Response** (400 Bad Request):
```json
{
  "detail": "Weights must sum to non-zero value"
}
```

---

## **Python Code Examples**

### **Example 1: Basic Health Check**
```python
import requests

BASE_URL = "http://localhost:8000"

# Check if API is ready
response = requests.get(f"{BASE_URL}/health")
if response.status_code == 200:
    print("✓ API is healthy")
    data = response.json()
    print(f"  Version: {data['version']}")
    print(f"  Available layers: {len(data['available_layers'])}")
else:
    print(f"✗ API error: {response.status_code}")
```

### **Example 2: Compute MCDA Overlay**
```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Define weights (AHP analysis results)
weights = {
    "mapa_irradiacao": 0.35,    # Solar potential (highest priority)
    "mapa_populacao": 0.25,      # Demand/population
    "mapa_distanciarede": 0.20,  # Grid access
    "mapa_declividade": 0.10,    # Installation difficulty
    "mapa_ndvi": 0.10            # Land cover suitability
}

# Send request to API
response = requests.post(
    f"{BASE_URL}/mcda",
    json={"weights": weights}
)

if response.status_code == 200:
    result = response.json()
    print(f"✓ MCDA computation successful")
    print(f"  Result statistics:")
    print(f"    Min aptitude: {result['summary']['min']:.3f}")
    print(f"    Max aptitude: {result['summary']['max']:.3f}")
    print(f"    Mean aptitude: {result['summary']['mean']:.3f}")
    print(f"    Std deviation: {result['summary']['std']:.3f}")
    print(f"  Output saved to: {result['saved_path']}")
else:
    print(f"✗ Error: {response.status_code}")
    print(f"  Details: {response.json()}")
```

### **Example 3: Sensitivity Analysis via API**
```python
import requests

BASE_URL = "http://localhost:8000"
base_weights = {
    "mapa_irradiacao": 0.35,
    "mapa_populacao": 0.25,
    "mapa_distanciarede": 0.20,
    "mapa_declividade": 0.10,
    "mapa_ndvi": 0.10
}

# Test variations on solar irradiance weight
print("Testing sensitivity to solar irradiance weight changes:")
print("Weight | Max Suitability")
print("-------|----------------")

for variation in [-20, -10, 0, 10, 20]:
    # Modify solar irradiance weight
    test_weights = base_weights.copy()
    test_weights["mapa_irradiacao"] *= (1 + variation/100)
    
    # Normalize to sum to 1.0
    total = sum(test_weights.values())
    test_weights = {k: v/total for k, v in test_weights.items()}
    
    # Compute overlay
    response = requests.post(
        f"{BASE_URL}/mcda",
        json={"weights": test_weights}
    )
    
    if response.status_code == 200:
        max_suitability = response.json()["summary"]["max"]
        print(f"{test_weights['mapa_irradiacao']:5.2f} | {max_suitability:6.3f}")
```

---

## **JavaScript/Node.js Examples**

### **Example 1: Fetch with Node.js**
```javascript
const BASE_URL = "http://localhost:8000";

async function computeMCDA() {
  const weights = {
    "mapa_irradiacao": 0.35,
    "mapa_populacao": 0.25,
    "mapa_distanciarede": 0.20,
    "mapa_declividade": 0.10,
    "mapa_ndvi": 0.10
  };

  try {
    const response = await fetch(`${BASE_URL}/mcda`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({ weights })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const result = await response.json();
    console.log("✓ MCDA Result:");
    console.log(`  Mean aptitude: ${result.summary.mean.toFixed(3)}`);
    console.log(`  Output: ${result.saved_path}`);
  } catch (error) {
    console.error("✗ Error:", error);
  }
}

computeMCDA();
```

---

## **cURL Examples**

### **Get Available Layers**
```bash
curl -X GET "http://localhost:8000/layers" \
  -H "accept: application/json"
```

### **Compute MCDA with Custom Weights**
```bash
curl -X POST "http://localhost:8000/mcda" \
  -H "Content-Type: application/json" \
  -d '{
    "weights": {
      "mapa_irradiacao": 0.40,
      "mapa_populacao": 0.30,
      "mapa_distanciarede": 0.20,
      "mapa_declividade": 0.05,
      "mapa_ndvi": 0.05
    }
  }'
```

---

## **Integration with MCDA Application**

### **Workflow: API-driven analysis**
```python
import requests
import numpy as np
import subprocess

BASE_URL = "http://localhost:8000"

# Step 1: Get list of available layers
layers_resp = requests.get(f"{BASE_URL}/layers")
layers = layers_resp.json()["available"]
print(f"Available layers: {layers}")

# Step 2: Generate baseline weights from AHP
# (In production, read from database or config)
weights = {layer: 1/len(layers) for layer in layers}  # Equal weights as baseline

# Step 3: Compute MCDA overlay
mcda_resp = requests.post(f"{BASE_URL}/mcda", json={"weights": weights})
result = mcda_resp.json()

# Step 4: Load result for further analysis
overlap_array = np.load(result["saved_path"])

# Step 5: Run LCOE analysis on top sites
top_indices = np.argsort(overlap_array.flatten())[-10:]  # Top 10 locations
print(f"Top 10 locations identified for LCOE analysis")

# Step 6: (Optional) Call external LCOE calculator
subprocess.run(["python", "scripts/lcoe_calculator.py", 
                "--input", result["saved_path"]])
```

---

## **Error Handling**

### **Common Errors & Solutions**

| Status | Error | Cause | Solution |
|--------|-------|-------|----------|
| **400** | "No maps found" | Raster files missing | Run `python scripts/generate_maps_simple.py` |
| **400** | "Weights must sum to non-zero" | All weights are zero | Provide at least one non-zero weight |
| **500** | "Overlay computation failed" | NaN in input data | Check data quality (`scripts/validation_pipeline.py`) |
| **503** | Connection refused | API not running | Run `python -m uvicorn scripts.api:app` |

---

## **Advanced: Deployment**

### **Docker Deployment**
```bash
docker build -t geesp-api .
docker run -p 8000:8000 geesp-api
# API available at http://localhost:8000
```

### **Kubernetes Deployment**
```bash
kubectl apply -f k8s/geesp-app-deployment.yaml
# Exposes API at http://geesp-api.default.svc.cluster.local:8000
```

### **Production with Gunicorn (multi-worker)**
```bash
pip install gunicorn
gunicorn scripts.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

---

## **Monitoring & Troubleshooting**

### **Check API Health**
```bash
# Local health check
curl http://localhost:8000/health

# With JSON output
curl -s http://localhost:8000/health | python -m json.tool
```

### **Monitor Logs**
```bash
# If running with uvicorn
python -m uvicorn scripts.api:app --reload --log-level debug

# If running with Docker
docker logs -f <container_id>
```

### **Performance Testing**
```bash
# Install Apache Bench
sudo apt-get install apache2-utils  # Ubuntu/Debian
brew install httpd   # macOS

# Run load test: 1000 requests, 10 concurrent
ab -n 1000 -c 10 http://localhost:8000/health
```

---

## **API Versioning**

Current version: **1.0.0**

**Future versions** will maintain backward compatibility:
- v1.1 (planned): Add batch processing endpoint
- v2.0 (future): Possible breaking changes with advanced features

---

## **FAQ**

**Q: Can I use the API without Docker?**  
A: Yes! Just install dependencies: `pip install -r requirements.txt` and run with uvicorn.

**Q: What authentication does the API use?**  
A: Current version is open (no auth). For production, add OAuth2/JWT in deployment.

**Q: Can I submit custom raster data?**  
A: Not in v1.0. Currently reads from `data/processed/*.npy` files.

**Q: Is the API thread-safe?**  
A: Yes, with caveats. Use proper ASGI server (Gunicorn/Uvicorn) for production.

**Q: What's the maximum request payload?**  
A: Default 25 MB. Configure in Uvicorn if needed.

---

**Need help?** Contact: api-support@geesp-angola.org
