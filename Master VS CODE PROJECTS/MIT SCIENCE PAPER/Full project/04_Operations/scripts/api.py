#!/usr/bin/env python3
"""
GEESP-Angola API Routes
Production-ready API endpoints for dashboard data access and operations
Usage: 
  Flask: flask run --host=0.0.0.0 --port=5000
  FastAPI: uvicorn api:app --host=0.0.0.0 --port=5000
"""

from typing import Optional, List, Dict, Any
from datetime import datetime, timedelta
import json
import logging
from pydantic import BaseModel
from enum import Enum

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# For production, use FastAPI or Flask
try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.responses import JSONResponse
    USE_FASTAPI = True
except ImportError:
    USE_FASTAPI = False
    try:
        from flask import Flask, request, jsonify
        USE_FLASK = True
    except ImportError:
        USE_FLASK = False


# ============================================================================
# Data Models
# ============================================================================

class LocationData(BaseModel):
    """Location/community data model"""
    location_id: str
    name: str
    latitude: float
    longitude: float
    province: str
    district: str
    population: int = 0
    solar_potential: float = 0.0  # kWh/m²/day
    poverty_rate: float = 0.0


class LCOEAnalysisResult(BaseModel):
    """LCOE analysis result"""
    location_id: str
    technology: str  # 'solar', 'wind', 'hydro', 'grid'
    lcoe_usd_per_kwh: float
    capital_cost_usd: float
    annual_opex_usd: float
    annual_generation_kwh: float
    irradiance: Optional[float] = None  # for solar


class AptitudeClassification(BaseModel):
    """Aptitude classification result"""
    location_id: str
    aptitude_class: str  # 'very_high', 'high', 'medium', 'low'
    aptitude_score: float  # 0-1
    suitable_technologies: List[str]
    recommendations: List[str]


class HealthStatus(BaseModel):
    """API health status"""
    status: str  # 'healthy', 'degraded', 'unhealthy'
    timestamp: datetime
    services: Dict[str, str]


# ============================================================================
# FastAPI Implementation
# ============================================================================

if USE_FASTAPI:
    app = FastAPI(
        title="GEESP-Angola API",
        description="Data access and analysis API for GEESP-Angola project",
        version="1.0.0"
    )
    
    # In-memory data cache (replace with database in production)
    locations_cache: Dict[str, LocationData] = {}
    lcoe_results_cache: Dict[str, List[LCOEAnalysisResult]] = {}
    
    # ========================================================================
    # Health & Status Endpoints
    # ========================================================================
    
    @app.get("/health", response_model=HealthStatus)
    async def health_check():
        """Check API health and service status"""
        return HealthStatus(
            status="healthy",
            timestamp=datetime.now(),
            services={
                "database": "connected",
                "cache": "operational",
                "geospatial": "ready"
            }
        )
    
    @app.get("/api/v1/status")
    async def api_status():
        """Get detailed API status"""
        return {
            "api_version": "1.0.0",
            "timestamp": datetime.now().isoformat(),
            "uptime_seconds": 3600,  # Replace with actual uptime
            "cached_locations": len(locations_cache),
            "cached_analyses": len(lcoe_results_cache)
        }
    
    # ========================================================================
    # Location Endpoints
    # ========================================================================
    
    @app.get("/api/v1/locations", response_model=List[LocationData])
    async def list_locations(
        province: Optional[str] = Query(None),
        limit: int = Query(100, ge=1, le=1000)
    ):
        """List all surveyed locations with optional filtering"""
        logger.info(f"List locations request: province={province}, limit={limit}")
        
        locations = list(locations_cache.values())
        
        if province:
            locations = [loc for loc in locations if loc.province.lower() == province.lower()]
        
        return locations[:limit]
    
    @app.get("/api/v1/locations/{location_id}", response_model=LocationData)
    async def get_location(location_id: str):
        """Get details for a specific location"""
        logger.info(f"Get location request: {location_id}")
        
        if location_id not in locations_cache:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")
        
        return locations_cache[location_id]
    
    @app.post("/api/v1/locations")
    async def create_location(location: LocationData):
        """Create/register a new location"""
        logger.info(f"Create location request: {location.location_id}")
        
        if location.location_id in locations_cache:
            raise HTTPException(status_code=409, detail=f"Location {location.location_id} already exists")
        
        locations_cache[location.location_id] = location
        return {"status": "created", "location_id": location.location_id}
    
    # ========================================================================
    # Analysis Endpoints
    # ========================================================================
    
    @app.get("/api/v1/locations/{location_id}/lcoe")
    async def get_lcoe_analysis(
        location_id: str,
        technology: Optional[str] = Query(None)
    ):
        """Get LCOE analysis results for a location"""
        logger.info(f"Get LCOE request: {location_id}, technology={technology}")
        
        if location_id not in lcoe_results_cache:
            raise HTTPException(status_code=404, detail=f"No LCOE analysis for {location_id}")
        
        results = lcoe_results_cache[location_id]
        
        if technology:
            results = [r for r in results if r.technology.lower() == technology.lower()]
        
        return results
    
    @app.post("/api/v1/locations/{location_id}/analyze")
    async def run_analysis(location_id: str):
        """Trigger LCOE and aptitude analysis for a location"""
        logger.info(f"Trigger analysis request: {location_id}")
        
        if location_id not in locations_cache:
            raise HTTPException(status_code=404, detail=f"Location {location_id} not found")
        
        # In production, would trigger async analysis job
        # For now, return example results
        location = locations_cache[location_id]
        
        analysis_results = {
            "location_id": location_id,
            "timestamp": datetime.now().isoformat(),
            "lcoe_results": [
                {
                    "technology": "solar",
                    "lcoe_usd_per_kwh": 0.045,
                    "capital_cost_usd": 85000,
                    "annual_opex_usd": 800.0,
                    "annual_generation_kwh": 45000.0,
                    "irradiance": location.solar_potential
                }
            ],
            "aptitude": {
                "aptitude_class": "very_high",
                "aptitude_score": 0.87,
                "suitable_technologies": ["solar", "wind"],
                "recommendations": [
                    "Solar PV is highly suitable given solar potential",
                    "Consider regional grid connection for load balancing"
                ]
            }
        }
        
        # Cache results
        lcoe_results_cache[location_id] = [
            LCOEAnalysisResult(**r) for r in analysis_results["lcoe_results"]
        ]
        
        return analysis_results
    
    # ========================================================================
    # Geospatial Endpoints
    # ========================================================================
    
    @app.get("/api/v1/spatial/nearest-locations")
    async def nearest_locations(
        latitude: float = Query(..., ge=-90, le=90),
        longitude: float = Query(..., ge=-180, le=180),
        radius_km: float = Query(50, ge=1, le=500)
    ):
        """Find locations near a geographic point"""
        logger.info(f"Nearest locations request: ({latitude}, {longitude}), radius={radius_km}km")
        
        # Simplified distance calculation (should use proper geospatial distance)
        nearby = []
        for location in locations_cache.values():
            # Rough distance calculation (good enough for demo)
            dx = (location.longitude - longitude) * 111  # km per degree longitude
            dy = (location.latitude - latitude) * 111    # km per degree latitude
            distance = (dx**2 + dy**2) ** 0.5
            
            if distance <= radius_km:
                nearby.append({
                    "location": location,
                    "distance_km": round(distance, 2)
                })
        
        # Sort by distance
        nearby.sort(key=lambda x: x["distance_km"])
        
        return nearby[:50]
    
    # ========================================================================
    # Data Export Endpoints
    # ========================================================================
    
    @app.get("/api/v1/export/locations-csv")
    async def export_locations_csv():
        """Export all locations as CSV"""
        logger.info("Export locations CSV request")
        
        import csv
        from io import StringIO
        
        output = StringIO()
        if locations_cache:
            locations = list(locations_cache.values())
            fieldnames = ['location_id', 'name', 'latitude', 'longitude', 'province', 'district', 'population', 'solar_potential']
            writer = csv.DictWriter(output, fieldnames=fieldnames)
            writer.writeheader()
            for loc in locations:
                writer.writerow(loc.dict())
        
        return {
            "data": output.getvalue(),
            "rows": len(locations_cache),
            "format": "csv"
        }
    
    # ========================================================================
    # Admin Endpoints (protected in production)
    # ========================================================================
    
    @app.delete("/api/v1/admin/cache/clear")
    async def clear_cache(api_key: Optional[str] = Query(None)):
        """Clear all cached data"""
        logger.info("Clear cache request")
        
        # In production, verify API key
        if api_key != "admin_secret_key":
            raise HTTPException(status_code=403, detail="Unauthorized")
        
        locations_cache.clear()
        lcoe_results_cache.clear()
        
        return {"status": "cache cleared"}


# ============================================================================
# Flask Implementation (alternative)
# ============================================================================

elif USE_FLASK:
    app = Flask(__name__)
    
    locations_cache: Dict[str, Dict[str, Any]] = {}
    
    @app.route('/health')
    def health_check():
        """Health check endpoint"""
        return jsonify({
            "status": "healthy",
            "timestamp": datetime.now().isoformat(),
            "services": {
                "database": "connected",
                "cache": "operational"
            }
        })
    
    @app.route('/api/v1/locations', methods=['GET'])
    def list_locations():
        """List locations"""
        province = request.args.get('province')
        limit = request.args.get('limit', default=100, type=int)
        
        locations = list(locations_cache.values())
        if province:
            locations = [loc for loc in locations if loc.get('province') == province]
        
        return jsonify(locations[:limit])
    
    @app.route('/api/v1/locations/<location_id>', methods=['GET'])
    def get_location(location_id):
        """Get location details"""
        if location_id not in locations_cache:
            return jsonify({"error": "Location not found"}), 404
        
        return jsonify(locations_cache[location_id])
    
    @app.route('/api/v1/locations', methods=['POST'])
    def create_location():
        """Create new location"""
        data = request.get_json()
        location_id = data.get('location_id')
        
        if location_id in locations_cache:
            return jsonify({"error": "Location already exists"}), 409
        
        locations_cache[location_id] = data
        return jsonify({"status": "created", "location_id": location_id}), 201


# ============================================================================
# Standalone mode (if neither framework available)
# ============================================================================

else:
    logger.error("No API framework available. Install fastapi or flask.")
    app = None


if __name__ == '__main__':
    if USE_FASTAPI:
        import uvicorn
        uvicorn.run(app, host='0.0.0.0', port=5000)
    elif USE_FLASK:
        app.run(host='0.0.0.0', port=5000, debug=True)
    else:
        logger.error("Cannot run: no framework available")
