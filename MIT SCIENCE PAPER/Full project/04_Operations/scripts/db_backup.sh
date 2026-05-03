#!/usr/bin/env bash
# Simple PG backup script: creates timestamped dumps and prunes old backups
# Requires: pg_dump

set -euo pipefail
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
BACKUP_DIR="$ROOT_DIR/backups"
mkdir -p "$BACKUP_DIR"

: "${PGHOST:=localhost}"
: "${PGPORT:=5432}"
: "${PGUSER:=postgres}"
: "${PGPASSWORD:=}"
: "${PGDATABASE:=geesp}"
: "${RETENTION_DAYS:=7}"

export PGPASSWORD

TS=$(date +"%F_%H%M%S")
OUT_FILE="$BACKUP_DIR/${PGDATABASE}_backup_${TS}.dump"

echo "Creating backup: $OUT_FILE"
pg_dump -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -Fc -d "$PGDATABASE" -f "$OUT_FILE"

# Prune old backups
find "$BACKUP_DIR" -type f -mtime +$RETENTION_DAYS -name "${PGDATABASE}_backup_*.dump" -print -delete || true

echo "Backup complete. Current backups in $BACKUP_DIR"