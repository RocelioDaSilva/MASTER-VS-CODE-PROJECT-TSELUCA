#!/usr/bin/env bash
# Shared PostgreSQL environment defaults for GEESP DB scripts.

load_db_env_defaults() {
  : "${PGHOST:=localhost}"
  : "${PGPORT:=5432}"
  : "${PGUSER:=postgres}"
  : "${PGPASSWORD:=}"
  : "${PGDATABASE:=geesp}"
  : "${RETENTION_DAYS:=7}"

  export PGPASSWORD
}
