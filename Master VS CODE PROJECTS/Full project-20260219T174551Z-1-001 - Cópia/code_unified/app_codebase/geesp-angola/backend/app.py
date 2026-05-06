"""
GEESP-Angola Application Factory.

This module creates and configures the Flask/FastAPI application instances
for different environments (development, staging, production).

Usage:
    from backend.app import create_app
    app = create_app("production")
"""

import sys
from pathlib import Path
from typing import Optional

# Setup project paths
_root = Path(__file__).resolve().parent
_scripts = _root / "scripts"

# Clear any existing paths
if str(_root) in sys.path:
    sys.path.remove(str(_root))
if str(_scripts) in sys.path:
    sys.path.remove(str(_scripts))

# Insert in correct order (scripts FIRST, then root)
sys.path.insert(0, str(_scripts))
sys.path.insert(0, str(_root))

# Clean up module cache
if "utils" in sys.modules and not hasattr(sys.modules["utils"], "error_handlers"):
    del sys.modules["utils"]

from utils.logging import setup_logging

logger = setup_logging(__name__)


def create_app(environment: str = "development"):
    """
    Application factory for GEESP-Angola.
    
    Creates and configures the FastAPI application for the specified environment.
    
    Args:
        environment: Environment name (development, staging, production)
        
    Returns:
        FastAPI: Configured FastAPI application instance
        
    Raises:
        ValueError: If environment is not supported
    """
    if environment not in ["development", "staging", "production", "testing"]:
        raise ValueError(
            f"Invalid environment: {environment}. "
            "Must be one of: development, staging, production, testing"
        )
    
    logger.info(f"Creating application for environment: {environment}")
    
    # Import API
    from api.api import app
    
    # Load environment-specific configuration
    try:
        from core.config import ConfigManager
        config = ConfigManager.get_instance()
        config.set("environment", environment)
        logger.info(f"Configuration loaded for {environment}")
    except Exception as e:
        logger.warning(f"Could not load configuration: {e}")
    
    # Add environment-specific middleware and configuration
    if environment == "development":
        logger.info("Development environment - enabling debug mode")
        app.debug = True
    
    elif environment == "staging":
        logger.info("Staging environment - production-like setup")
        app.debug = False
    
    elif environment == "production":
        logger.info("Production environment - optimized configuration")
        app.debug = False
    
    elif environment == "testing":
        logger.info("Testing environment - enabled for unit tests")
        app.debug = True
    
    logger.info(f"Application successfully created with {environment} configuration")
    
    return app


if __name__ == "__main__":
    import uvicorn
    
    # Get environment from command line or default to development
    import sys
    
    env = sys.argv[1] if len(sys.argv) > 1 else "development"
    app = create_app(env)
    
    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
        log_level="info",
        reload=(env == "development"),
    )
