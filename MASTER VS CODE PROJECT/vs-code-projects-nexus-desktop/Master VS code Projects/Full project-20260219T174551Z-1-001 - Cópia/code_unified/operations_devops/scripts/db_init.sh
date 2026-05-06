#!/usr/bin/env bash
# Initialize PostgreSQL database with PostGIS and project schema
# Uses environment variables: PGHOST, PGPORT, PGUSER, PGPASSWORD, PGDATABASE

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SCHEMA_FILE="$ROOT_DIR/scripts/db_schema.sql"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/db_env_loader.sh"
load_db_env_defaults

echo "Initializing database '$PGDATABASE' on $PGHOST:$PGPORT as $PGUSER"

# Create database if not exists
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -tc "SELECT 1 FROM pg_database WHERE datname = '$PGDATABASE'" | grep -q 1 || psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -c "CREATE DATABASE $PGDATABASE"

# Run schema SQL
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" -f "$SCHEMA_FILE"

echo "Database initialization complete. Run 'psql -d $PGDATABASE' to inspect."