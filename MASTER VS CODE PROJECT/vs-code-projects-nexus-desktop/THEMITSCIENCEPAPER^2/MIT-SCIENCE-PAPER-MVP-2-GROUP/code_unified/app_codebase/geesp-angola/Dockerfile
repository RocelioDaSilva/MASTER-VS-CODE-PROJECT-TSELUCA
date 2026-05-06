# ============================================================================
# GEESP-Angola Multi-Stage Dockerfile
# Optimized for production with minimal footprint and security best practices
# Build: docker build -t geesp-angola:latest .
# Run: docker run -p 8501:8501 geesp-angola:latest
# ============================================================================

# ============================================================================
# STAGE 1: Builder - Compile dependencies
# ============================================================================
FROM python:3.11-slim as builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin libgdal-dev \
    libpq-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements*.txt ./

# Build wheels in isolated location
RUN mkdir /build/wheels && \
    pip install --upgrade pip setuptools wheel && \
    pip wheel --no-cache-dir --no-deps --wheel-dir /build/wheels -r requirements-app.txt

# ============================================================================
# STAGE 2: Runtime - Minimal production image
# ============================================================================
FROM python:3.11-slim

LABEL maintainer="GEESP Team <rocelio@isptec.ao>"
LABEL description="GEESP-Angola: Geospatial Energy for Equity & Solar Planning"
LABEL version="1.0.0"

# Set working directory
WORKDIR /app

# Set environment variables for Python
ENV LANG=C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1 \
    STREAMLIT_SERVER_HEADLESS=true \
    STREAMLIT_SERVER_ADDRESS=0.0.0.0 \
    STREAMLIT_SERVER_PORT=8501

# Install runtime dependencies only (much smaller layer)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gdal-bin libgdal26 libpq5 git curl \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder stage
COPY --from=builder /build/wheels /wheels

# Install wheels (fast, no compilation)
RUN pip install --upgrade pip setuptools wheel && \
    pip install --no-index --no-deps --find-links /wheels /wheels/* && \
    rm -rf /wheels

# Create non-root user for security (principle of least privilege)
RUN useradd -m -u 1000 -s /bin/bash appuser && \
    mkdir -p /app /data /logs && \
    chown -R appuser:appuser /app /data /logs

# Switch to non-root user
USER appuser

# Copy application code (after creating user to preserve permissions)
COPY --chown=appuser:appuser . /app

# Create necessary directories
RUN mkdir -p /app/data/processed /app/logs /app/cache

# Expose port
EXPOSE 8501

# Health check - verify app is running
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Security: Run as non-root user, read-only root filesystem where possible
SECURITY_OPTS: no-new-privileges:true

# Default command
ENTRYPOINT ["streamlit", "run"]
CMD ["geesp_unified_app.py", "--server.port=8501", "--server.address=0.0.0.0"]


