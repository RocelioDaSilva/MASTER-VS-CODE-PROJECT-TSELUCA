# Database Backup & Restore (PostgreSQL + PostGIS)

This document explains how to initialize, backup and restore the production database.

Prerequisites:
- PostgreSQL 14+ with `psql`, `pg_dump`, `pg_restore` available on PATH
- User with privileges to create databases: typically `postgres`

Setup:
1. Copy `scripts/pg_env_example.sh` to `.env` and set values, or export the vars in your shell.

Initialize database and schema:
```bash
source scripts/pg_env_example.sh
bash scripts/db_init.sh
```

Create a backup (manual):
```bash
source scripts/pg_env_example.sh
bash scripts/db_backup.sh
```

Restore from a backup:
```bash
source scripts/pg_env_example.sh
bash scripts/db_restore.sh backups/geesp_backup_2026-02-10_120000.dump
```

Automating backups:
- Add a cron job on the DB server to run `db_backup.sh` daily. Example crontab entry (run as user with DB access):
```cron
0 2 * * * /bin/bash /path/to/repo/scripts/db_backup.sh >> /var/log/geesp/db_backup.log 2>&1
```

Retention & monitoring:
- `db_backup.sh` prunes backups older than `$RETENTION_DAYS` (default 7).
- Monitor `/var/log/geesp/db_backup.log` and alert on failures.

Security:
- Do not commit `PGPASSWORD` to source control.
- Prefer storing secrets in environment managers or Kubernetes secrets.

Notes:
- `db_init.sh` will create the database if it does not exist and run `scripts/db_schema.sql`.
- The schema file is intentionally minimal and idempotent. Adapt to production needs.
