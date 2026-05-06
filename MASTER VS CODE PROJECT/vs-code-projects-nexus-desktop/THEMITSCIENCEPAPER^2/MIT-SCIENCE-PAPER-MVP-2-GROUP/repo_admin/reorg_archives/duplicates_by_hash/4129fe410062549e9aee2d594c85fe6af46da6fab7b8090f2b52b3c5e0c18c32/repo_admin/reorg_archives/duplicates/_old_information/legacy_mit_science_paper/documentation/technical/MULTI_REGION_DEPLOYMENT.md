# Multi-Region Deployment Guide for GEESP-Angola
# This file shows how to adapt docker-compose.yml for different regions and environments

## Overview

The GEESP-Angola application can be deployed across multiple regions (Angola regional offices, headquarters, disaster recovery sites). Each region may have:
- Different database instances (regional PostGIS for local data)
- Separate Streamlit dashboard instances
- Regional data processing pipelines

## File Structure for Multi-Region Deployment

```
deployment/
├── docker-compose.yml              # Base configuration (shared services)
├── docker-compose.prod.yml         # Production overrides
├── regions/
│   ├── luanda-hq/
│   │   ├── .env                    # Regional environment variables
│   │   ├── docker-compose.override.yml
│   │   └── config/
│   ├── huambo-regional/
│   │   ├── .env
│   │   ├── docker-compose.override.yml
│   │   └── config/
│   └── benguela-field-station/
│       ├── .env
│       ├── docker-compose.override.yml
│       └── config/
└── scripts/
    ├── deploy_region.sh
    └── sync_databases.sh
```

## Docker Compose Override Pattern

### Base Config: `docker-compose.yml`

The base file defines common services (app, PostGIS, Redis). Each region overrides with:

```yaml
# docker-compose.yml (base)
version: '3.8'

services:
  geesp-app:
    image: geesp-app:latest
    ports:
      - "${STREAMLIT_PORT:-8501}:8501"
    environment:
      DATABASE_URL: "postgresql://${DB_USER}:${DB_PASSWORD}@postgres:5432/${DB_NAME}"
      REDIS_URL: "redis://redis:6379/0"
      REGION: "${REGION:-default}"
    depends_on:
      - postgres
      - redis
    volumes:
      - ./data:/app/data

  postgres:
    image: postgis/postgis:latest
    environment:
      POSTGRES_PASSWORD: ${DB_PASSWORD}
      POSTGRES_USER: ${DB_USER}
      POSTGRES_DB: ${DB_NAME}
    ports:
      - "${DB_PORT:-5432}:5432"
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/db_schema.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    image: redis:7-alpine
    ports:
      - "${REDIS_PORT:-6379}:6379"
    volumes:
      - redis_data:/data

volumes:
  postgres_data:
  redis_data:
```

### Regional Override: `regions/luanda-hq/docker-compose.override.yml`

```yaml
version: '3.8'

services:
  geesp-app:
    # Use region-specific image tag
    image: geesp-app:luanda-hq-latest
    
    # Luanda HQ has more replicas
    deploy:
      replicas: 3
    
    # Map external port for HQ access
    ports:
      - "8501:8501"
      - "8502:8501"  # Replica 2
      - "8503:8501"  # Replica 3
    
    # Add region-specific config
    volumes:
      - ./config/luanda_config.yaml:/app/config/region.yaml
      - /mnt/shared_data:/app/shared_data  # NFS mount for shared analysis
    
  postgres:
    # HQ has more resources (explicit CPU/memory limits)
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 4G
        reservations:
          cpus: '1'
          memory: 2G
    
    # Persist backups locally
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./backups:/var/lib/postgresql/backups
      - ./scripts/db_schema.sql:/docker-entrypoint-initdb.d/init.sql

  redis:
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 1G
    # Sentinel for high availability
    environment:
      - REDIS_SENTINEL_ENABLED=true
```

### Regional Override: `regions/huambo-regional/docker-compose.override.yml`

```yaml
version: '3.8'

services:
  geesp-app:
    image: geesp-app:huambo-regional-latest
    
    # Single instance in regional office
    deploy:
      replicas: 1
    
    ports:
      - "8501:8501"
    
    # Region-specific config and smaller data volumes
    volumes:
      - ./config/huambo_config.yaml:/app/config/region.yaml
      - /data/regional_surveys:/app/data/local_surveys
  
  postgres:
    # Regional database (smaller than HQ)
    deploy:
      resources:
        limits:
          cpus: '1'
          memory: 2G
        reservations:
          cpus: '0.5'
          memory: 1G
    
    volumes:
      - postgres_data:/var/lib/postgresql/data
      - ./scripts/db_schema.sql:/docker-entrypoint-initdb.d/init.sql
```

### Regional Override: `regions/benguela-field-station/docker-compose.override.yml`

```yaml
version: '3.8'

services:
  geesp-app:
    image: geesp-app:benguela-latest
    
    # Minimal footprint for field station
    deploy:
      replicas: 1
      resources:
        limits:
          cpus: '0.5'
          memory: 1G
    
    ports:
      - "8501:8501"
    
    # Offline-first: sync with central DB periodically
    environment:
      SYNC_MODE: "periodic"
      SYNC_INTERVAL: "3600"  # 1 hour
    
    # Limited local storage
    volumes:
      - ./config/benguela_config.yaml:/app/config/region.yaml
      - /data/field_surveys:/app/data/surveys

  postgres:
    # Minimal resources (field station may have limited power)
    deploy:
      resources:
        limits:
          cpus: '0.25'
          memory: 512M
    
    volumes:
      - postgres_data:/var/lib/postgresql/data
```

## Regional .env Files

### `regions/luanda-hq/.env`

```env
# Luanda Headquarters
REGION=luanda-hq
STREAMLIT_PORT=8501
DB_USER=geesp_hq
DB_PASSWORD=secure_hq_password_here
DB_NAME=geesp_hq_production
DB_PORT=5432
REDIS_PORT=6379

# Replication settings
ENABLE_REPLICATION=true
REPLICA_UPSTREAM=luanda-hq.geesp.internal
BACKUP_RETENTION_DAYS=90

# Performance
WORKERS=4
WORKER_TIMEOUT=120
```

### `regions/huambo-regional/.env`

```env
# Huambo Regional Office
REGION=huambo
STREAMLIT_PORT=8501
DB_USER=geesp_huambo
DB_PASSWORD=secure_huambo_password
DB_NAME=geesp_huambo_regional
DB_PORT=5432
REDIS_PORT=6379

# Sync with HQ every 4 hours
SYNC_WITH_HQ=true
SYNC_INTERVAL=14400
HQ_DATABASE_URL=postgresql://sync_user:sync_pass@hq.geesp.internal:5432/geesp_hq_production

# Performance
WORKERS=2
WORKER_TIMEOUT=90
```

### `regions/benguela-field-station/.env`

```env
# Benguela Field Station
REGION=benguela
STREAMLIT_PORT=8501
DB_USER=geesp_field
DB_PASSWORD=simple_field_password
DB_NAME=geesp_field_local
DB_PORT=5432

# Offline mode (no HQ sync while offline)
OFFLINE_MODE=true
OFFLINE_SYNC_ON_RECONNECT=true

# Minimal resources
WORKERS=1
WORKER_TIMEOUT=60
```

## Deployment Scripts

### `scripts/deploy_region.sh`

```bash
#!/bin/bash
# Deploy GEESP-Angola to a specific region
# Usage: ./deploy_region.sh <region_name> [environment]

REGION=${1:-luanda-hq}
ENV=${2:-prod}
COMPOSE_FILE="docker-compose.yml"
OVERRIDE_FILE="regions/$REGION/docker-compose.override.yml"

if [ ! -f "$OVERRIDE_FILE" ]; then
    echo "Error: Region '$REGION' not found"
    exit 1
fi

echo "Deploying GEESP-Angola to region: $REGION"

# Load regional environment variables
set -a
source "regions/$REGION/.env"
set +a

# Deploy with base + regional override
docker-compose \
    -f "$COMPOSE_FILE" \
    -f "$OVERRIDE_FILE" \
    -p "geesp_$REGION" \
    up -d --build

echo "Region '$REGION' deployment complete"
docker-compose -p "geesp_$REGION" ps
```

### `scripts/sync_databases.sh`

```bash
#!/bin/bash
# Sync regional databases with HQ

HQ_REGION="luanda-hq"
REGIONS=("huambo" "benguela")

for region in "${REGIONS[@]}"; do
    echo "Syncing $region with HQ..."
    
    # Dump regional DB
    docker-compose -p "geesp_$region" exec -T postgres \
        pg_dump -U geesp_$region -h localhost geesp_${region}_* \
        > "/tmp/$region.sql"
    
    # Send to HQ
    psql -h hq.geesp.internal -U sync_user -d geesp_hq_production \
        < "/tmp/$region.sql"
    
    # Clean up
    rm "/tmp/$region.sql"
done

echo "Database sync complete"
```

## Deployment Commands

```bash
# Deploy to Luanda HQ
./scripts/deploy_region.sh luanda-hq prod

# Deploy to Huambo regional
./scripts/deploy_region.sh huambo regional

# Deploy to Benguela field station
./scripts/deploy_region.sh benguela-field-station dev

# Sync all regional databases with HQ
./scripts/sync_databases.sh

# View logs for a region
docker-compose -p geesp_luanda-hq logs -f geesp-app

# Scale app in a region
docker-compose -p geesp_huambo up -d --scale geesp-app=3
```

## High Availability & Disaster Recovery

For critical deployments:
- **Replication:** Set `ENABLE_REPLICATION=true` for database replication between regions
- **Backup:** Daily backups with 90-day retention to object storage (S3, Azure Blob, etc.)
- **Failover:** Use DNS failover or Kubernetes for automatic failover between regions
