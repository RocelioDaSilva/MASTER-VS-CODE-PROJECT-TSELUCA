#!/bin/bash
# Production Database Initialization and Backup Script
# Purpose: Manage PostgreSQL database for GEESP-Angola production
# Usage: ./db_init_backup.sh [init|backup|restore|verify]

set -e

# Configuration
DB_NAME="${DB_NAME:-geesp_angola_prod}"
DB_USER="${DB_USER:-geesp_admin}"
DB_HOST="${DB_HOST:-localhost}"
DB_PORT="${DB_PORT:-5432}"
BACKUP_DIR="${BACKUP_DIR:-./backups}"
BACKUP_RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-30}"
SCHEMA_FILE="./scripts/db_schema.sql"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Initialize production database
init_database() {
    log_info "Initializing production database..."
    
    # Check if database exists
    if psql -h "$DB_HOST" -U "$DB_USER" -tc "SELECT 1 FROM pg_database WHERE datname = '$DB_NAME'" | grep -q 1; then
        log_warn "Database '$DB_NAME' already exists"
        return 0
    fi
    
    # Create database
    log_info "Creating database: $DB_NAME"
    createdb -h "$DB_HOST" -U "$DB_USER" "$DB_NAME"
    
    # Enable PostGIS extension
    log_info "Enabling PostGIS extension..."
    psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS postgis;"
    psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "CREATE EXTENSION IF NOT EXISTS postgis_topology;"
    
    # Load schema
    if [ -f "$SCHEMA_FILE" ]; then
        log_info "Loading schema from $SCHEMA_FILE..."
        psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f "$SCHEMA_FILE"
    else
        log_warn "Schema file not found: $SCHEMA_FILE"
    fi
    
    # Create indexes
    log_info "Creating indexes..."
    psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" <<EOF
    -- Spatial indexes
    CREATE INDEX IF NOT EXISTS idx_communities_geom ON communities USING GIST(geom);
    CREATE INDEX IF NOT EXISTS idx_solar_data_raster ON solar_data USING GIST(rast::geometry);
    
    -- Temporal indexes
    CREATE INDEX IF NOT EXISTS idx_measurements_date ON measurements(measurement_date DESC);
    
    -- Lookup indexes
    CREATE INDEX IF NOT EXISTS idx_communities_code ON communities(community_code);
    CREATE INDEX IF NOT EXISTS idx_projects_name ON projects(project_name);
    
    -- Composite indexes
    CREATE INDEX IF NOT EXISTS idx_measurements_location_date ON measurements(community_id, measurement_date);
    
    -- VACUUM and ANALYZE
    VACUUM FULL ANALYZE;
EOF
    
    log_info "Database initialization complete"
}

# Create database backup
backup_database() {
    log_info "Starting database backup..."
    
    # Create backup directory
    mkdir -p "$BACKUP_DIR"
    
    # Generate backup filename
    BACKUP_FILE="$BACKUP_DIR/geesp_${DB_NAME}_$(date +%Y%m%d_%H%M%S).sql.gz"
    
    log_info "Backing up to: $BACKUP_FILE"
    
    # Create backup
    pg_dump -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" | gzip > "$BACKUP_FILE"
    
    # Verify backup
    if [ -f "$BACKUP_FILE" ]; then
        SIZE=$(du -h "$BACKUP_FILE" | cut -f1)
        log_info "Backup successful (size: $SIZE)"
    else
        log_error "Backup failed"
        exit 1
    fi
    
    # Upload to S3 (if configured)
    if command -v aws &> /dev/null; then
        log_info "Uploading backup to S3..."
        aws s3 cp "$BACKUP_FILE" "s3://geesp-backups/$(basename $BACKUP_FILE)"
        log_info "S3 upload complete"
    fi
    
    # Cleanup old backups
    cleanup_old_backups
}

# Restore database from backup
restore_database() {
    BACKUP_FILE="$1"
    
    if [ -z "$BACKUP_FILE" ]; then
        log_error "Usage: $0 restore <backup_file>"
        exit 1
    fi
    
    if [ ! -f "$BACKUP_FILE" ]; then
        log_error "Backup file not found: $BACKUP_FILE"
        exit 1
    fi
    
    log_warn "WARNING: This will drop existing database '$DB_NAME'"
    read -p "Continue? (yes/no): " RESPONSE
    
    if [ "$RESPONSE" != "yes" ]; then
        log_info "Restore cancelled"
        return 0
    fi
    
    log_info "Dropping existing database..."
    dropdb -h "$DB_HOST" -U "$DB_USER" "$DB_NAME" || true
    
    log_info "Creating new database..."
    createdb -h "$DB_HOST" -U "$DB_USER" "$DB_NAME"
    
    log_info "Restoring from backup..."
    
    # Detect if file is gzipped
    if [[ "$BACKUP_FILE" == *.gz ]]; then
        gunzip -c "$BACKUP_FILE" | psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME"
    else
        psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -f "$BACKUP_FILE"
    fi
    
    log_info "Restore complete"
}

# Cleanup old backups
cleanup_old_backups() {
    log_info "Cleaning up backups older than $BACKUP_RETENTION_DAYS days..."
    
    find "$BACKUP_DIR" -name "geesp_*.sql.gz" -mtime +$BACKUP_RETENTION_DAYS -delete
    
    # Count remaining backups
    COUNT=$(find "$BACKUP_DIR" -name "geesp_*.sql.gz" | wc -l)
    log_info "Retained $COUNT recent backups"
}

# Verify database integrity
verify_database() {
    log_info "Verifying database integrity..."
    
    # Check database connection
    if ! psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT 1" &>/dev/null; then
        log_error "Cannot connect to database"
        exit 1
    fi
    log_info "✓ Database connection OK"
    
    # Check tables exist
    TABLE_COUNT=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tc "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public'")
    log_info "✓ Tables found: $TABLE_COUNT"
    
    # Check indexes
    INDEX_COUNT=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tc "SELECT COUNT(*) FROM pg_indexes WHERE schemaname='public'")
    log_info "✓ Indexes found: $INDEX_COUNT"
    
    # Check data
    COMMUNITY_COUNT=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tc "SELECT COUNT(*) FROM communities" 2>/dev/null || echo "0")
    log_info "✓ Communities: $COMMUNITY_COUNT"
    
    # Check PostGIS
    if psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c "SELECT postgis_version()" &>/dev/null; then
        POSTGIS_VERSION=$(psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -tc "SELECT postgis_version()")
        log_info "✓ PostGIS: $POSTGIS_VERSION"
    fi
    
    log_info "Database verification complete"
}

# Automated daily backup (for cron)
daily_backup() {
    log_info "Running daily backup..."
    backup_database
    
    # Log event
    echo "$(date): Daily backup completed" >> "${BACKUP_DIR}/backup.log"
}

# Show help
show_help() {
    cat <<EOF
GEESP-Angola Database Management Script

Usage: $0 [COMMAND] [OPTIONS]

Commands:
  init                Initialize production database with schema
  backup              Create backup of current database
  restore <file>      Restore from backup file
  verify              Verify database integrity
  daily-backup        Run automated daily backup (for cron)
  help                Show this help message

Environment Variables:
  DB_NAME             Database name (default: geesp_angola_prod)
  DB_USER             Database user (default: geesp_admin)
  DB_HOST             Database host (default: localhost)
  DB_PORT             Database port (default: 5432)
  BACKUP_DIR          Backup directory (default: ./backups)
  BACKUP_RETENTION_DAYS  Retention days (default: 30)

Examples:
  # Initialize production database
  $0 init
  
  # Create backup
  $0 backup
  
  # Restore from backup
  $0 restore ./backups/geesp_geesp_angola_prod_20260301_120000.sql.gz
  
  # Setup daily backup in crontab
  0 2 * * * /path/to/$0 daily-backup

EOF
}

# Main script
case "${1:-help}" in
    init)
        init_database
        ;;
    backup)
        backup_database
        ;;
    restore)
        restore_database "$2"
        ;;
    verify)
        verify_database
        ;;
    daily-backup)
        daily_backup
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        log_error "Unknown command: $1"
        show_help
        exit 1
        ;;
esac

log_info "Done"
