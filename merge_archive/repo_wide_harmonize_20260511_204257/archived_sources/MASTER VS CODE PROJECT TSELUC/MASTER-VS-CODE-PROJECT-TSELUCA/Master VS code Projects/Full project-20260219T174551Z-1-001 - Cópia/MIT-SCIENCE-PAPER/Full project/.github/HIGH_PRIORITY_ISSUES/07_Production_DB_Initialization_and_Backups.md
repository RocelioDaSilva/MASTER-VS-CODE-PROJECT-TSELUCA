Title: Production database initialization & backups

Owner: DB Admin

Description:
Initialize production PostGIS database and configure automated backups using `scripts/db_init.sh` and `scripts/db_backup.sh`.

Acceptance criteria:
- Production DB created with `scripts/db_schema.sql`
- Automated daily backups enabled and monitored
- Backup retention confirmed (default 7 days)

Labels: infra, high-priority
