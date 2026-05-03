"""
FastAPI REST API endpoints for GEESP-Angola.

This module provides the main REST API with 8 endpoints for:
- Scenario management (CRUD)
- Analysis execution
- Results retrieval
- Health checks

Endpoints:
    - POST /scenarios - Create scenario
    - GET /scenarios - List all scenarios
    - GET /scenarios/{id} - Get scenario
    - PUT /scenarios/{id} - Update scenario
    - DELETE /scenarios/{id} - Delete scenario
    - POST /analyze - Run analysis (LCOE/MCDA)
    - GET /results/{id} - Get results
    - GET /maps/{id} - Get maps
    - GET /health - Health check
"""

import os
import sys
import time
import uuid
import hmac
import hashlib
import secrets
import base64
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Any, Dict, List, Optional

_START_TIME = time.monotonic()

from fastapi import Depends, FastAPI, Header, HTTPException, Path as PathParam, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from slowapi import Limiter
    from slowapi.errors import RateLimitExceeded
    from slowapi.util import get_remote_address
except ImportError:
    Limiter = None
    RateLimitExceeded = None

    def get_remote_address(request: Request) -> str:
        return "0.0.0.0"

# Setup project paths for imports
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))

try:
    from utils.logging import setup_logging
except ImportError:
    setup_logging = None

from .models import (
    AnalysisRequest,
    AnalysisResponse,
    DirectAnalysisRequest,
    DirectAnalysisResponse,
    SuitabilityResultItem,
    HealthResponse,
    LoginRequest,
    RegisterRequest,
    AuthTokenResponse,
    UserResponse,
    ScenarioCreate,
    ScenarioResponse,
    ScenarioUpdate,
)

# Import analysis engines
try:
    from scripts.mcda_analysis import AHPWeighter, MCDAnalyzer
    from scripts.lcoe_calculator import LCOECalculator, SolarParameters
    _HAS_ANALYSIS = True
except ImportError:
    _HAS_ANALYSIS = False

# Import database session and ORM models
try:
    from database.session import get_db, init_db, SessionLocal
    from database.models import (
        Scenario as DBScenario,
        AnalysisResult as DBAnalysisResult,
        Map as DBMap,
        User as DBUser,
    )
    from sqlalchemy.orm import Session
    _HAS_DB = True
except ImportError:
    _HAS_DB = False
    Session = None  # type annotation fallback

# Setup logging
logger = setup_logging(__name__) if setup_logging else None

# Create FastAPI application
app = FastAPI(
    title="GEESP-Angola API",
    description="Geospatial Energy for Equity & Solar Planning - REST API",
    version="2.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

# Add CORS middleware
allowed_origins = os.getenv(
    "GEESP_ALLOWED_ORIGINS",
    "http://localhost:3000,http://localhost:5173,http://localhost:8501",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=[origin.strip() for origin in allowed_origins.split(",") if origin.strip()],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization", "Accept"],
)

if Limiter is not None:
    limiter = Limiter(key_func=get_remote_address)
    app.state.limiter = limiter
else:
    _env = os.getenv("GEESP_ENVIRONMENT", "development").lower()
    if _env == "production":
        raise RuntimeError(
            "slowapi is required in production for rate limiting. "
            "Install it with: pip install slowapi"
        )

    class _NoopLimiter:
        def limit(self, _value: str):
            def _decorator(func):
                return func
            return _decorator

    limiter = _NoopLimiter()
    if logger:
        logger.warning("slowapi not installed; rate limiting is disabled (dev only)")


async def _rate_limit_exceeded_handler(request: Request, exc: Exception) -> JSONResponse:
    """Return consistent response body for rate-limit violations."""
    return JSONResponse(
        status_code=status.HTTP_429_TOO_MANY_REQUESTS,
        content={
            "error": "Rate limit exceeded",
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


if RateLimitExceeded is not None:
    app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)


# ============================================================================
# Security Helpers
# ============================================================================


async def verify_api_key(
    x_api_key: Optional[str] = Header(default=None, alias="X-API-Key"),
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
) -> str:
    """Verify API key from headers. In development, allow when key is unset."""
    valid_key = os.getenv("GEESP_API_KEY", "").strip()
    if not valid_key:
        return "dev"

    provided_key = (x_api_key or "").strip()
    if not provided_key and authorization:
        auth_value = authorization.strip()
        if auth_value.lower().startswith("bearer "):
            provided_key = auth_value[7:].strip()
        else:
            provided_key = auth_value

    if not provided_key or not hmac.compare_digest(provided_key, valid_key):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing API key",
        )

    return provided_key

# ---------------------------------------------------------------------------
# Database initialisation (fallback to in-memory dicts when DB unavailable)
# ---------------------------------------------------------------------------

if _HAS_DB:
    try:
        init_db()
        if logger:
            logger.info("Database initialised (SQLAlchemy)")
    except Exception as _db_err:
        if logger:
            logger.warning(f"Database init failed, falling back to in-memory: {_db_err}")
        _HAS_DB = False

# In-memory fallback (used when SQLAlchemy is unavailable)
if not _HAS_DB:
    _MEM_SCENARIOS: Dict[str, Dict[str, Any]] = {}
    _MEM_ANALYSES: Dict[str, Dict[str, Any]] = {}
    _MEM_RESULTS: Dict[str, Dict[str, Any]] = {}
    if logger:
        logger.warning("Running with in-memory storage (data will not persist)")


# ============================================================================
# Database helper: optional DB dependency
# ============================================================================

def _get_optional_db():
    """Yield a DB session if available, else None."""
    if _HAS_DB:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()
    else:
        yield None


# ============================================================================
# Auth Helpers
# ============================================================================

_JWT_SECRET = os.getenv("GEESP_JWT_SECRET", secrets.token_hex(32))
_JWT_EXPIRY_HOURS = 24
_JWT_REFRESH_EXPIRY_DAYS = 7


def _hash_password(password: str) -> str:
    """Hash a password using PBKDF2-HMAC-SHA256 with a random salt."""
    salt = secrets.token_hex(16)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return f"{salt}${h.hex()}"


def _verify_password(password: str, stored_hash: str) -> bool:
    """Verify a password against a stored hash."""
    if "$" not in stored_hash:
        return False
    salt, hash_hex = stored_hash.split("$", 1)
    h = hashlib.pbkdf2_hmac("sha256", password.encode(), salt.encode(), 100_000)
    return hmac.compare_digest(h.hex(), hash_hex)


def _create_jwt(payload: dict, expiry_hours: float = _JWT_EXPIRY_HOURS) -> str:
    """Create a simple JWT (HS256) without external dependencies."""
    header = {"alg": "HS256", "typ": "JWT"}
    payload = {**payload, "exp": int((datetime.now(timezone.utc) + timedelta(hours=expiry_hours)).timestamp())}
    segments = []
    for part in [header, payload]:
        encoded = base64.urlsafe_b64encode(json.dumps(part, separators=(",", ":")).encode()).rstrip(b"=")
        segments.append(encoded)
    signing_input = b".".join(segments)
    sig = hmac.new(_JWT_SECRET.encode(), signing_input, hashlib.sha256).digest()
    segments.append(base64.urlsafe_b64encode(sig).rstrip(b"="))
    return b".".join(segments).decode()


def _decode_jwt(token: str) -> Optional[dict]:
    """Decode and verify a JWT. Returns payload or None if invalid."""
    try:
        parts = token.split(".")
        if len(parts) != 3:
            return None
        # Verify signature
        signing_input = f"{parts[0]}.{parts[1]}".encode()
        sig = hmac.new(_JWT_SECRET.encode(), signing_input, hashlib.sha256).digest()
        expected_sig = base64.urlsafe_b64encode(sig).rstrip(b"=").decode()
        if not hmac.compare_digest(parts[2], expected_sig):
            return None
        # Decode payload
        padded = parts[1] + "=" * (4 - len(parts[1]) % 4)
        payload = json.loads(base64.urlsafe_b64decode(padded))
        # Check expiry
        if payload.get("exp", 0) < datetime.now(timezone.utc).timestamp():
            return None
        return payload
    except Exception:
        return None


# ============================================================================
# Auth Endpoints
# ============================================================================


@app.post("/api/auth/register", tags=["Auth"], summary="Register a new user")
async def auth_register(
    request: Request,
    body: RegisterRequest,
    db: Optional[Session] = Depends(_get_optional_db),
):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    existing = db.query(DBUser).filter(DBUser.email == body.email.lower().strip()).first()
    if existing:
        raise HTTPException(status_code=409, detail="Email already registered")

    user_id = f"user-{uuid.uuid4().hex[:8]}"
    now = datetime.now(timezone.utc)
    user = DBUser(
        id=user_id,
        email=body.email.lower().strip(),
        name=body.name.strip(),
        password_hash=_hash_password(body.password),
        role="user",
        is_active=True,
        created_at=now,
    )
    db.add(user)
    db.commit()
    db.refresh(user)

    user_data = user.to_dict()
    access_token = _create_jwt({"sub": user.id, "email": user.email, "role": user.role})
    refresh_token = _create_jwt({"sub": user.id, "type": "refresh"}, expiry_hours=_JWT_REFRESH_EXPIRY_DAYS * 24)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "user": user_data,
    }


@app.post("/api/auth/login", tags=["Auth"], summary="Login")
async def auth_login(
    request: Request,
    body: LoginRequest,
    db: Optional[Session] = Depends(_get_optional_db),
):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    user = db.query(DBUser).filter(DBUser.email == body.email.lower().strip()).first()
    if not user or not _verify_password(body.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    if not user.is_active:
        raise HTTPException(status_code=403, detail="Account disabled")

    user.last_login = datetime.now(timezone.utc)
    db.commit()

    user_data = user.to_dict()
    access_token = _create_jwt({"sub": user.id, "email": user.email, "role": user.role})
    refresh_token = _create_jwt({"sub": user.id, "type": "refresh"}, expiry_hours=_JWT_REFRESH_EXPIRY_DAYS * 24)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "user": user_data,
    }


@app.post("/api/auth/refresh", tags=["Auth"], summary="Refresh access token")
async def auth_refresh(
    request: Request,
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
    db: Optional[Session] = Depends(_get_optional_db),
):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()

    payload = _decode_jwt(token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid refresh token")

    user = db.query(DBUser).filter(DBUser.id == payload["sub"]).first()
    if not user or not user.is_active:
        raise HTTPException(status_code=401, detail="User not found or disabled")

    access_token = _create_jwt({"sub": user.id, "email": user.email, "role": user.role})
    refresh_token = _create_jwt({"sub": user.id, "type": "refresh"}, expiry_hours=_JWT_REFRESH_EXPIRY_DAYS * 24)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "Bearer",
        "user": user.to_dict(),
    }


@app.post("/api/auth/logout", tags=["Auth"], summary="Logout")
async def auth_logout(request: Request):
    # JWT is stateless; client clears tokens. Server-side we just return success.
    return {"message": "Logged out successfully"}


@app.get("/api/auth/profile", tags=["Auth"], summary="Get current user profile")
async def auth_profile(
    request: Request,
    authorization: Optional[str] = Header(default=None, alias="Authorization"),
    db: Optional[Session] = Depends(_get_optional_db),
):
    if db is None:
        raise HTTPException(status_code=503, detail="Database unavailable")

    token = ""
    if authorization and authorization.lower().startswith("bearer "):
        token = authorization[7:].strip()

    payload = _decode_jwt(token)
    if not payload or payload.get("type") == "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = db.query(DBUser).filter(DBUser.id == payload["sub"]).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user.to_dict()


# ============================================================================
# Scenario Management Endpoints
# ============================================================================


@app.post(
    "/scenarios",
    response_model=ScenarioResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["Scenarios"],
    summary="Create a new scenario",
    description="Create a new solar energy planning scenario",
)
@limiter.limit("10/minute")
async def create_scenario(
    request: Request,
    scenario_data: ScenarioCreate,
    _: str = Depends(verify_api_key),
    db: Optional[Session] = Depends(_get_optional_db),
) -> ScenarioResponse:
    """Create a new scenario."""
    try:
        scenario_id = f"scenario-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        
        if db is not None:
            row = DBScenario(
                id=scenario_id,
                name=scenario_data.name,
                description=scenario_data.description,
                location=scenario_data.location,
                status="active",
                config=scenario_data.config or {},
                created_at=now,
                updated_at=now,
            )
            db.add(row)
            db.commit()
            db.refresh(row)
            resp = ScenarioResponse(
                id=row.id, name=row.name, description=row.description,
                location=row.location, status=row.status,
                created_at=row.created_at, updated_at=row.updated_at,
                config=row.config,
            )
        else:
            scenario = {
                "id": scenario_id, "name": scenario_data.name,
                "description": scenario_data.description,
                "location": scenario_data.location, "status": "active",
                "created_at": now, "updated_at": now,
                "config": scenario_data.config or {},
            }
            _MEM_SCENARIOS[scenario_id] = scenario
            resp = ScenarioResponse(**scenario)
        
        if logger:
            logger.info(f"Created scenario: {scenario_id}")
        return resp
    except Exception as e:
        if logger:
            logger.error(f"Error creating scenario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process request"
        )


@app.get(
    "/scenarios",
    response_model=List[ScenarioResponse],
    tags=["Scenarios"],
    summary="List all scenarios",
    description="Retrieve all existing scenarios with optional pagination",
)
@limiter.limit("30/minute")
async def list_scenarios(
    request: Request,
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=200),
    _: str = Depends(verify_api_key),
    db: Optional[Session] = Depends(_get_optional_db),
) -> List[ScenarioResponse]:
    """List all scenarios with pagination."""
    if db is not None:
        rows = db.query(DBScenario).offset(skip).limit(limit).all()
        return [
            ScenarioResponse(
                id=r.id, name=r.name, description=r.description,
                location=r.location, status=r.status,
                created_at=r.created_at, updated_at=r.updated_at,
                config=r.config,
            )
            for r in rows
        ]
    scenarios = list(_MEM_SCENARIOS.values())
    return [ScenarioResponse(**s) for s in scenarios[skip : skip + limit]]


@app.get(
    "/scenarios/{scenario_id}",
    response_model=ScenarioResponse,
    tags=["Scenarios"],
    summary="Get scenario details",
    description="Retrieve details of a specific scenario",
)
@limiter.limit("30/minute")
async def get_scenario(
    request: Request,
    scenario_id: str = PathParam(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$"),
    _: str = Depends(verify_api_key),
    db: Optional[Session] = Depends(_get_optional_db),
) -> ScenarioResponse:
    """Get scenario by ID."""
    if db is not None:
        row = db.query(DBScenario).filter(DBScenario.id == scenario_id).first()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Scenario {scenario_id} not found")
        return ScenarioResponse(
            id=row.id, name=row.name, description=row.description,
            location=row.location, status=row.status,
            created_at=row.created_at, updated_at=row.updated_at, config=row.config,
        )
    if scenario_id not in _MEM_SCENARIOS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Scenario {scenario_id} not found")
    return ScenarioResponse(**_MEM_SCENARIOS[scenario_id])


@app.put(
    "/scenarios/{scenario_id}",
    response_model=ScenarioResponse,
    tags=["Scenarios"],
    summary="Update scenario",
    description="Update an existing scenario",
)
@limiter.limit("10/minute")
async def update_scenario(
    request: Request,
    scenario_id: str = PathParam(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$"),
    scenario_data: ScenarioUpdate = ..., 
    _: str = Depends(verify_api_key),
    db: Optional[Session] = Depends(_get_optional_db),
) -> ScenarioResponse:
    """Update scenario."""
    now = datetime.now(timezone.utc)
    
    if db is not None:
        row = db.query(DBScenario).filter(DBScenario.id == scenario_id).first()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Scenario {scenario_id} not found")
        try:
            if scenario_data.name is not None:
                row.name = scenario_data.name
            if scenario_data.description is not None:
                row.description = scenario_data.description
            if scenario_data.location is not None:
                row.location = scenario_data.location
            if scenario_data.config is not None:
                existing = row.config or {}
                existing.update(scenario_data.config)
                row.config = existing
            row.updated_at = now
            db.commit()
            db.refresh(row)
            if logger:
                logger.info(f"Updated scenario: {scenario_id}")
            return ScenarioResponse(
                id=row.id, name=row.name, description=row.description,
                location=row.location, status=row.status,
                created_at=row.created_at, updated_at=row.updated_at, config=row.config,
            )
        except Exception as e:
            db.rollback()
            if logger:
                logger.error(f"Error updating scenario: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process request")
    
    # In-memory fallback
    if scenario_id not in _MEM_SCENARIOS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Scenario {scenario_id} not found")
    try:
        scenario = _MEM_SCENARIOS[scenario_id]
        if scenario_data.name is not None:
            scenario["name"] = scenario_data.name
        if scenario_data.description is not None:
            scenario["description"] = scenario_data.description
        if scenario_data.location is not None:
            scenario["location"] = scenario_data.location
        if scenario_data.config is not None:
            scenario["config"].update(scenario_data.config)
        scenario["updated_at"] = now
        if logger:
            logger.info(f"Updated scenario: {scenario_id}")
        return ScenarioResponse(**scenario)
    except Exception as e:
        if logger:
            logger.error(f"Error updating scenario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process request"
        )


@app.delete(
    "/scenarios/{scenario_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["Scenarios"],
    summary="Delete scenario",
    description="Delete a scenario",
)
@limiter.limit("10/minute")
async def delete_scenario(
    request: Request,
    scenario_id: str = PathParam(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$"),
    _: str = Depends(verify_api_key),
    db: Optional[Session] = Depends(_get_optional_db),
) -> None:
    """Delete scenario."""
    if db is not None:
        row = db.query(DBScenario).filter(DBScenario.id == scenario_id).first()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Scenario {scenario_id} not found")
        try:
            db.delete(row)
            db.commit()
            if logger:
                logger.info(f"Deleted scenario: {scenario_id}")
            return
        except Exception as e:
            db.rollback()
            if logger:
                logger.error(f"Error deleting scenario: {e}")
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Failed to process request")
    
    # In-memory fallback
    if scenario_id not in _MEM_SCENARIOS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Scenario {scenario_id} not found")
    try:
        del _MEM_SCENARIOS[scenario_id]
        if logger:
            logger.info(f"Deleted scenario: {scenario_id}")
    except Exception as e:
        if logger:
            logger.error(f"Error deleting scenario: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process request"
        )


# ============================================================================
# Analysis Endpoints
# ============================================================================


@app.post(
    "/analyze",
    response_model=AnalysisResponse,
    status_code=status.HTTP_202_ACCEPTED,
    tags=["Analysis"],
    summary="Run analysis",
    description="Execute analysis on a scenario",
)
@limiter.limit("10/minute")
async def run_analysis(
    request: Request,
    analysis_request: AnalysisRequest,
    _: str = Depends(verify_api_key),
    db: Optional[Session] = Depends(_get_optional_db),
) -> AnalysisResponse:
    """Run analysis on scenario."""
    # Validate scenario exists
    scenario_exists = False
    scenario_name = "Angola"
    if db is not None:
        row = db.query(DBScenario).filter(DBScenario.id == analysis_request.scenario_id).first()
        if row:
            scenario_exists = True
            scenario_name = row.name or "Angola"
    else:
        if analysis_request.scenario_id in _MEM_SCENARIOS:
            scenario_exists = True
            scenario_name = _MEM_SCENARIOS[analysis_request.scenario_id].get("name", "Angola")
    
    if not scenario_exists:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Scenario {analysis_request.scenario_id} not found"
        )
    
    try:
        analysis_id = f"analysis-{uuid.uuid4().hex[:8]}"
        now = datetime.now(timezone.utc)
        start = time.monotonic()
        
        params = analysis_request.parameters or {}
        analysis_type = analysis_request.analysis_type
        
        results: Dict[str, Any] = {}

        if analysis_type == "lcoe" and _HAS_ANALYSIS:
            calculator = LCOECalculator(
                location=params.get("location", scenario_name)
            )
            capacity = params.get("capacity_mw", 1.0)
            irradiance = params.get("annual_irradiance", 2000.0)
            discount = params.get("discount_rate", 8)
            lifetime = params.get("lifetime", 25)

            comparison = calculator.compare_technologies(
                capacity_mw=capacity,
                annual_irradiance=irradiance,
                discount_rate=discount,
                lifetime=lifetime,
            )
            best = comparison.sort_values("lcoe_usd_per_kwh").iloc[0] if not comparison.empty else {}
            results = {
                "analysis_type": "lcoe",
                "scenario_id": analysis_request.scenario_id,
                "technologies": comparison.to_dict(orient="records") if not comparison.empty else [],
                "best_technology": best.to_dict() if hasattr(best, "to_dict") else {},
                "parameters_used": {
                    "capacity_mw": capacity,
                    "annual_irradiance": irradiance,
                    "discount_rate": discount,
                    "lifetime": lifetime,
                },
            }
        elif analysis_type == "mcda" and _HAS_ANALYSIS:
            weights = params.get("weights", {
                "Irradiação Solar": 25,
                "Densidade Populacional": 20,
                "Acesso (Distância Rede)": 20,
                "Infraestrutura": 10,
                "Uso do Solo": 15,
                "Luminosidade Noturna": 10,
            })
            total_w = sum(weights.values()) or 1
            normalized_weights = {k: v / total_w for k, v in weights.items()}
            results = {
                "analysis_type": "mcda",
                "scenario_id": analysis_request.scenario_id,
                "weights_normalized": normalized_weights,
                "status": "completed",
                "note": "Full raster overlay requires dashboard (Streamlit) or GeoTIFF upload",
                "parameters_used": params,
            }
        else:
            results = {
                "analysis_type": analysis_type,
                "scenario_id": analysis_request.scenario_id,
                "status": "completed",
                "parameters_used": params,
            }

        elapsed_ms = (time.monotonic() - start) * 1000
        
        analysis = {
            "id": analysis_id,
            "scenario_id": analysis_request.scenario_id,
            "analysis_type": analysis_type,
            "status": "completed",
            "results": results,
            "created_at": now,
            "processing_time_ms": round(elapsed_ms, 2),
        }
        
        # Persist to database or in-memory
        if db is not None:
            db_result = DBAnalysisResult(
                id=analysis_id,
                scenario_id=analysis_request.scenario_id,
                analysis_type=analysis_type,
                status="completed",
                results=results,
                processing_time_ms=round(elapsed_ms, 2),
                created_at=now,
            )
            db.add(db_result)
            db.commit()
        else:
            _MEM_ANALYSES[analysis_id] = analysis
            _MEM_RESULTS[analysis_id] = results
        
        if logger:
            logger.info(f"Completed {analysis_type} analysis: {analysis_id} ({elapsed_ms:.0f}ms)")
        
        return AnalysisResponse(**analysis)
    except Exception as e:
        if logger:
            logger.error(f"Error running analysis: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to process request"
        )


# ============================================================================
# Frontend-compatible direct analysis endpoint
# ============================================================================


@app.post(
    "/api/analyze",
    response_model=DirectAnalysisResponse,
    tags=["Analysis"],
    summary="Run direct MCDA + LCOE analysis (frontend)",
    description=(
        "Accepts communities, MCDA weights and solar parameters directly "
        "and returns per-community suitability scores + LCOE."
    ),
)
@limiter.limit("10/minute")
async def run_direct_analysis(
    request: Request,
    body: DirectAnalysisRequest,
) -> DirectAnalysisResponse:
    """
    Frontend-facing analysis: compute a weighted suitability score and
    simplified LCOE for each community without requiring a stored scenario.
    """
    import math

    w = body.weights
    p = body.params
    items: list = []

    for c in body.communities:
        # --- MCDA suitability score (0-100) ---
        # Normalize individual criteria to 0-1 range with domain-appropriate scales.
        climate_score = min(c.ghi / 7.0, 1.0)                        # GHI up to 7 kWh/m2/day
        soil_score = 0.8 if c.soilType.lower() in ("sandy", "loam", "clay") else 0.5
        terrain_score = max(1.0 - c.slope / 30.0, 0.0)               # flat = best
        infra_score = max(1.0 - c.distToGrid / 100.0, 0.0)           # closer = better

        raw = (
            w.climate * climate_score
            + w.soil * soil_score
            + w.terrain * terrain_score
            + w.infrastructure * infra_score
        )
        weight_sum = w.climate + w.soil + w.terrain + w.infrastructure
        score = round((raw / weight_sum) * 100, 2) if weight_sum > 0 else 0.0

        # --- Simplified LCOE ($/kWh) ---
        annual_generation_kwh = (
            c.ghi * 365 * (p.wattage / 1000) * p.efficiency
        )
        if annual_generation_kwh > 0 and p.lifetime > 0:
            total_cost = p.capitalCost + p.omCost * p.lifetime
            lcoe = round(total_cost / (annual_generation_kwh * p.lifetime), 4)
        else:
            lcoe = 0.0

        # --- Aptitude label ---
        if score >= 80:
            aptitude = "Excellent"
        elif score >= 60:
            aptitude = "Good"
        elif score >= 40:
            aptitude = "Moderate"
        elif score >= 20:
            aptitude = "Poor"
        else:
            aptitude = "Unsuitable"

        items.append(SuitabilityResultItem(
            communityId=c.id, score=score, aptitude=aptitude, lcoe=lcoe,
        ))

    if logger:
        logger.info(f"Direct analysis completed for {len(items)} communities")

    return DirectAnalysisResponse(results=items)


@app.get(
    "/results/{analysis_id}",
    response_model=Dict[str, Any],
    tags=["Results"],
    summary="Get analysis results",
    description="Retrieve results of a completed analysis",
)
@limiter.limit("30/minute")
async def get_results(
    request: Request,
    analysis_id: str = PathParam(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$"),
    _: str = Depends(verify_api_key),
    db: Optional[Session] = Depends(_get_optional_db),
) -> Dict[str, Any]:
    """Get analysis results."""
    if db is not None:
        row = db.query(DBAnalysisResult).filter(DBAnalysisResult.id == analysis_id).first()
        if not row:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis {analysis_id} not found")
        return row.results or {}
    if analysis_id not in _MEM_RESULTS:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis {analysis_id} not found")
    return _MEM_RESULTS[analysis_id]


@app.get(
    "/maps/{analysis_id}",
    response_model=Dict[str, Any],
    tags=["Maps"],
    summary="Get maps",
    description="Retrieve generated maps for an analysis",
)
@limiter.limit("30/minute")
async def get_maps(
    request: Request,
    analysis_id: str = PathParam(..., min_length=1, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$"),
    _: str = Depends(verify_api_key),
    db: Optional[Session] = Depends(_get_optional_db),
) -> Dict[str, Any]:
    """Get generated maps."""
    found = False
    if db is not None:
        row = db.query(DBAnalysisResult).filter(DBAnalysisResult.id == analysis_id).first()
        found = row is not None
    else:
        found = analysis_id in _MEM_ANALYSES
    
    if not found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Analysis {analysis_id} not found")
    return {"map_url": f"/maps/{analysis_id}.html", "analysis_id": analysis_id}


# ============================================================================
# Health Check Endpoint
# ============================================================================


@app.get(
    "/health",
    response_model=HealthResponse,
    tags=["Health"],
    summary="Health check",
    description="Check API service health",
)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.
    
    Returns:
        HealthResponse: Service health status
    """
    return HealthResponse(
        status="healthy",
        version="2.0",
        timestamp=datetime.now(timezone.utc),
        uptime_seconds=round(time.monotonic() - _START_TIME, 2),
    )


# ============================================================================
# Root Endpoint
# ============================================================================


@app.get("/", tags=["Root"], summary="API Information")
async def root() -> Dict[str, str]:
    """
    Root endpoint with API information.
    
    Returns:
        Dict: API information
    """
    return {
        "name": "GEESP-Angola API",
        "version": "2.0",
        "docs": "/docs",
        "redoc": "/redoc",
        "status": "running"
    }


# ============================================================================
# Error Handlers
# ============================================================================


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions."""
    if exc.status_code >= 500 and logger:
        logger.error(f"Internal API error: {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "Failed to process request" if exc.status_code >= 500 else exc.detail,
            "timestamp": datetime.now(timezone.utc).isoformat(),
        },
    )


if __name__ == "__main__":
    import uvicorn
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=True,
    )
