FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gdal-bin \
    libgdal-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements-app.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements-app.txt

# Copy application code
COPY . .

# Create data directory
RUN mkdir -p data/processed logs

# Expose Streamlit port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit app
CMD ["streamlit", "run", "geesp_unified_app.py", "--server.port=8501", "--server.address=0.0.0.0"]
