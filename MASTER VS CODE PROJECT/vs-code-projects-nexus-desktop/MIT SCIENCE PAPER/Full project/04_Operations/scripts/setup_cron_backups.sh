#!/usr/bin/env bash
# Cron Scheduling Setup Helper for GEESP-Angola Database Backups
# Install automated backup jobs safely with retention policies
#
# Usage:
#   bash scripts/setup_cron_backups.sh --daily
#   bash scripts/setup_cron_backups.sh --daily --weekly
#   bash scripts/setup_cron_backups.sh --remove    # Uninstall all backup crons

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
BACKUP_SCRIPT="$SCRIPT_DIR/db_backup.sh"
CRON_LOG="/var/log/geesp_backups.log"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

log_info() {
    echo -e "${GREEN}✓${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}⚠${NC} $1"
}

log_error() {
    echo -e "${RED}✗${NC} $1" >&2
}

# Validate backup script exists
if [ ! -x "$BACKUP_SCRIPT" ]; then
    log_error "Backup script not found or not executable: $BACKUP_SCRIPT"
    exit 1
fi

log_info "Setting up automated database backups"
log_info "Backup script: $BACKUP_SCRIPT"
log_info "Log file: $CRON_LOG"

# Create log file with appropriate permissions
if ! touch "$CRON_LOG" 2>/dev/null; then
    log_warn "Cannot write to $CRON_LOG, using current directory"
    CRON_LOG="./geesp_backups.log"
fi

chmod 666 "$CRON_LOG" 2>/dev/null || true

# Function to install cron job
install_cron() {
    local schedule=$1
    local description=$2
    local cron_entry="$schedule $BACKUP_SCRIPT >> $CRON_LOG 2>&1"
    
    # Get current crontab (if exists)
    local current_crontab
    if current_crontab=$(crontab -l 2>/dev/null); then
        # Check if job already exists
        if echo "$current_crontab" | grep -F "$BACKUP_SCRIPT" > /dev/null; then
            log_warn "Backup job already scheduled: $description"
            return 1
        fi
        # Append new job
        echo "$current_crontab" | { cat; echo "$cron_entry"; } | crontab -
    else
        # Create new crontab
        echo "$cron_entry" | crontab -
    fi
    
    log_info "Installed cron: $description"
    log_info "  Schedule: $schedule"
    return 0
}

# Function to remove all backup cron jobs
remove_crons() {
    local current_crontab
    if current_crontab=$(crontab -l 2>/dev/null); then
        if echo "$current_crontab" | grep -F "$BACKUP_SCRIPT" > /dev/null; then
            # Remove all lines containing our backup script
            echo "$current_crontab" | grep -v "$BACKUP_SCRIPT" | crontab - || true
            log_info "Removed all GEESP backup cron jobs"
        else
            log_warn "No GEESP backup cron jobs found"
        fi
    else
        log_warn "No crontab exists"
    fi
}

# Main logic
case "${1:-daily}" in
    daily)
        # Daily backup at 1:00 AM
        install_cron "0 1 * * *" "Daily backup (01:00)"
        ;;
    both)
        # Daily backup at 1:00 AM
        install_cron "0 1 * * *" "Daily backup (01:00)"
        # Weekly full backup at 3:00 AM on Sunday
        install_cron "0 3 * * 0" "Weekly full backup (Sunday 03:00)"
        ;;
    weekly)
        # Weekly backup at 3:00 AM on Sunday
        install_cron "0 3 * * 0" "Weekly full backup (Sunday 03:00)"
        ;;
    remove)
        remove_crons
        ;;
    *)
        log_error "Unknown option: $1"
        echo "Usage: $0 [daily|weekly|both|remove]"
        exit 1
        ;;
esac

# Display installed cron jobs
echo ""
log_info "Current cron jobs:"
crontab -l 2>/dev/null | grep -E "(^[0-9]|$BACKUP_SCRIPT)" | sed 's/^/  /' || log_warn "No cron jobs found"

echo ""
log_info "Backup logs will be written to: $CRON_LOG"
log_info "To monitor backups: tail -f $CRON_LOG"
echo ""
