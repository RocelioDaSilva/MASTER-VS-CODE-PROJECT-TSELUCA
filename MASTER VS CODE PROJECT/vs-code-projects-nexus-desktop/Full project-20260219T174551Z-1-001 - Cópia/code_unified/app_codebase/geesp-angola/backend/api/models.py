"""
Pydantic models for API request/response validation.

Classes:
    - Auth models: LoginRequest, RegisterRequest, AuthTokenResponse, UserResponse
    - ScenarioCreate: Create scenario request model
    - ScenarioUpdate: Update scenario request model
    - ScenarioResponse: Scenario response model
    - AnalysisRequest: Analysis request model
    - AnalysisResponse: Analysis response model
    - HealthResponse: Health check response model
"""

from datetime import datetime
from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field, field_validator
import re


# ============================================================================
# AUTH MODELS
# ============================================================================


class LoginRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=1, description="Password")


class RegisterRequest(BaseModel):
    email: str = Field(..., description="User email")
    password: str = Field(..., min_length=8, description="Password (min 8 chars)")
    name: str = Field(..., min_length=1, description="Display name")

    @field_validator("email")
    @classmethod
    def validate_email(cls, v: str) -> str:
        if not re.match(r"^[^@\s]+@[^@\s]+\.[^@\s]+$", v):
            raise ValueError("Invalid email format")
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def validate_password(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError("Password must be at least 8 characters")
        return v


class AuthTokenResponse(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
    user: Dict[str, Any]


class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str


# ============================================================================
# SCENARIO MODELS
# ============================================================================


class ScenarioCreate(BaseModel):
    """Request model for creating a new scenario."""
    
    name: str = Field(..., description="Scenario name")
    description: Optional[str] = Field(None, description="Scenario description")
    location: Optional[Dict[str, float]] = Field(
        None, description="Location coordinates (latitude, longitude)"
    )
    config: Optional[Dict[str, Any]] = Field(
        None, description="Scenario configuration"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Angola North 2024",
                "description": "Solar site selection for northern Angola",
                "location": {"latitude": -11.5, "longitude": 27.5},
                "config": {"mcda_iterations": 100}
            }
        }


class ScenarioUpdate(BaseModel):
    """Request model for updating a scenario."""
    
    name: Optional[str] = None
    description: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    config: Optional[Dict[str, Any]] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "name": "Angola North 2024 - Updated",
                "config": {"mcda_iterations": 200}
            }
        }


class ScenarioResponse(BaseModel):
    """Response model for scenario."""
    
    id: str = Field(..., description="Scenario ID")
    name: str = Field(..., description="Scenario name")
    description: Optional[str] = None
    location: Optional[Dict[str, float]] = None
    status: str = Field(default="active", description="Scenario status")
    created_at: datetime = Field(..., description="Creation timestamp")
    updated_at: Optional[datetime] = None
    config: Optional[Dict[str, Any]] = None
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "scenario-123",
                "name": "Angola North 2024",
                "description": "Solar site selection",
                "status": "active",
                "created_at": "2024-03-08T10:30:00Z",
                "location": {"latitude": -11.5, "longitude": 27.5}
            }
        }


class AnalysisRequest(BaseModel):
    """Request model for running analysis."""
    
    scenario_id: str = Field(..., description="Scenario ID")
    analysis_type: str = Field(..., description="Type: 'mcda', 'lcoe', 'validation'")
    parameters: Dict[str, Any] = Field(
        default_factory=dict, description="Analysis parameters"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "scenario_id": "scenario-123",
                "analysis_type": "mcda",
                "parameters": {"weights": {"irradiance": 0.4, "distance": 0.3}}
            }
        }


class AnalysisResponse(BaseModel):
    """Response model for analysis results."""
    
    id: str = Field(..., description="Analysis ID")
    scenario_id: str = Field(..., description="Parent scenario ID")
    analysis_type: str = Field(..., description="Type of analysis")
    status: str = Field(default="completed", description="Analysis status")
    results: Dict[str, Any] = Field(..., description="Analysis results")
    created_at: datetime = Field(..., description="Creation timestamp")
    processing_time_ms: Optional[float] = Field(
        None, description="Processing time in milliseconds"
    )
    
    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": "analysis-456",
                "scenario_id": "scenario-123",
                "analysis_type": "mcda",
                "status": "completed",
                "results": {"best_sites": ["site1", "site2"], "total_score": 85.5},
                "created_at": "2024-03-08T10:35:00Z",
                "processing_time_ms": 1250.5
            }
        }


class HealthResponse(BaseModel):
    """Response model for health check endpoint."""
    
    status: str = Field(default="healthy", description="Service status")
    version: str = Field(..., description="API version")
    timestamp: datetime = Field(..., description="Current timestamp")
    uptime_seconds: Optional[float] = Field(None, description="Uptime in seconds")
    
    class Config:
        json_schema_extra = {
            "example": {
                "status": "healthy",
                "version": "2.0",
                "timestamp": "2024-03-08T10:40:00Z",
                "uptime_seconds": 3600.0
            }
        }


class ErrorResponse(BaseModel):
    """Response model for error responses."""
    
    error: str = Field(..., description="Error message")
    detail: Optional[str] = Field(None, description="Detailed error information")
    code: Optional[str] = Field(None, description="Error code")
    timestamp: datetime = Field(..., description="Error timestamp")
    
    class Config:
        json_schema_extra = {
            "example": {
                "error": "NotFound",
                "detail": "Scenario with ID 'abc123' not found",
                "code": "SCENARIO_NOT_FOUND",
                "timestamp": "2024-03-08T10:40:00Z"
            }
        }


# ============================================================================
# Frontend-compatible direct analysis models
# ============================================================================


class CommunityInput(BaseModel):
    """A geographic community for MCDA + LCOE analysis."""
    id: str
    name: str
    province: str
    lat: float
    lng: float
    ghi: float = Field(..., description="Global Horizontal Irradiance (kWh/m2/day)")
    soilType: str = ""
    slope: float = 0.0
    distToGrid: float = Field(0.0, description="Distance to nearest grid (km)")
    population: int = 0


class MCDAWeightsInput(BaseModel):
    """MCDA weights (should sum to ~1.0)."""
    climate: float = Field(0.35, ge=0, le=1)
    soil: float = Field(0.15, ge=0, le=1)
    terrain: float = Field(0.25, ge=0, le=1)
    infrastructure: float = Field(0.25, ge=0, le=1)


class SolarParamsInput(BaseModel):
    """Solar PV system parameters for LCOE calculation."""
    wattage: float = Field(400, gt=0)
    efficiency: float = Field(0.21, gt=0, le=1)
    lifetime: int = Field(25, gt=0, le=50)
    omCost: float = Field(500, ge=0, description="Annual O&M cost ($)")
    capitalCost: float = Field(25000, gt=0, description="Initial investment ($)")


class DirectAnalysisRequest(BaseModel):
    """Request model for the frontend-facing /api/analyze endpoint."""
    communities: List[CommunityInput]
    weights: MCDAWeightsInput
    params: SolarParamsInput

    class Config:
        json_schema_extra = {
            "example": {
                "communities": [{"id": "c1", "name": "Luanda Solar Hub", "province": "Luanda",
                                 "lat": -8.838, "lng": 13.234, "ghi": 5.6, "soilType": "Sandy",
                                 "slope": 2.1, "distToGrid": 1.5, "population": 25000}],
                "weights": {"climate": 0.35, "soil": 0.15, "terrain": 0.25, "infrastructure": 0.25},
                "params": {"wattage": 400, "efficiency": 0.21, "lifetime": 25, "omCost": 500, "capitalCost": 25000},
            }
        }


class SuitabilityResultItem(BaseModel):
    """Single community suitability score."""
    communityId: str
    score: float = Field(..., ge=0, le=100)
    aptitude: str
    lcoe: float


class DirectAnalysisResponse(BaseModel):
    """Response for the frontend-facing /api/analyze endpoint."""
    results: List[SuitabilityResultItem]
