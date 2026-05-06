FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies needed for geospatial packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gdal-bin libgdal-dev \
    libpq-dev \
    git \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables
ENV LANG C.UTF-8 \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PIP_NO_CACHE_DIR=1

# Copy requirement file and install Python deps
COPY requirements-unified.txt .
RUN pip install --upgrade pip setuptools wheel && \
    pip install -r requirements-unified.txt

# Copy project files
COPY . /app

# Create non-root user for security
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app
USER appuser

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Run Streamlit app
ENTRYPOINT ["streamlit", "run"]
CMD ["geesp-unified-app.py"]

