#!/usr/bin/env bash
# Restore a pg_dump custom-format file into the target database (will DROP existing db)
# Usage: scripts/db_restore.sh /path/to/backup.dump

set -euo pipefail
if [ "$#" -lt 1 ]; then
  echo "Usage: $0 /path/to/backup.dump" >&2
  exit 1
fi

DUMP_FILE="$1"
ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
source "$SCRIPT_DIR/db_env_loader.sh"
load_db_env_defaults

if [ ! -f "$DUMP_FILE" ]; then
  echo "Dump file not found: $DUMP_FILE" >&2
  exit 2
fi

echo "Dropping and recreating database $PGDATABASE"
psql -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -c "DROP DATABASE IF EXISTS $PGDATABASE; CREATE DATABASE $PGDATABASE;"

echo "Restoring $DUMP_FILE into $PGDATABASE"
pg_restore -h "$PGHOST" -p "$PGPORT" -U "$PGUSER" -d "$PGDATABASE" --no-owner "$DUMP_FILE"

echo "Restore complete."