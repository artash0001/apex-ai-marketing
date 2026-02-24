#!/usr/bin/env bash
# =============================================================================
# Apex AI Marketing - Database Backup Script
# =============================================================================
# Creates a timestamped PostgreSQL backup from the Docker container.
# Keeps the last 30 backups automatically.
#
# Usage:
#   chmod +x scripts/backup.sh
#   ./scripts/backup.sh
#
# Cron setup (daily at 2:00 AM):
#   crontab -e
#   0 2 * * * /home/user/apex-ai-marketing/scripts/backup.sh >> /var/log/apex-backup.log 2>&1
# =============================================================================

set -euo pipefail

# ── Configuration ────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
BACKUP_DIR="${PROJECT_ROOT}/backups"
MAX_BACKUPS=30
CONTAINER_NAME="apex-db"
TIMESTAMP="$(date +%Y%m%d_%H%M%S)"
BACKUP_FILE="apex_ai_marketing_${TIMESTAMP}.sql.gz"

# Load environment variables
if [ -f "${PROJECT_ROOT}/.env" ]; then
    set -a
    source "${PROJECT_ROOT}/.env"
    set +a
fi

DB_USER="${POSTGRES_USER:-apex}"
DB_NAME="${POSTGRES_DB:-apex_ai_marketing}"

# ── Colors ───────────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

info()    { echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"; }
success() { echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"; }
error()   { echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $*"; exit 1; }

# ── Pre-flight checks ───────────────────────────────────────────────────
info "Starting database backup..."

# Ensure backup directory exists
mkdir -p "${BACKUP_DIR}"

# Check if the database container is running
if ! docker ps --format '{{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    error "Database container '${CONTAINER_NAME}' is not running"
fi

# ── Create backup ────────────────────────────────────────────────────────
info "Dumping database '${DB_NAME}' from container '${CONTAINER_NAME}'..."

docker exec "${CONTAINER_NAME}" \
    pg_dump \
        -U "${DB_USER}" \
        -d "${DB_NAME}" \
        --format=plain \
        --no-owner \
        --no-privileges \
        --clean \
        --if-exists \
    | gzip > "${BACKUP_DIR}/${BACKUP_FILE}"

# Verify the backup file was created and is not empty
if [ ! -s "${BACKUP_DIR}/${BACKUP_FILE}" ]; then
    rm -f "${BACKUP_DIR}/${BACKUP_FILE}"
    error "Backup file is empty or was not created"
fi

BACKUP_SIZE=$(du -h "${BACKUP_DIR}/${BACKUP_FILE}" | cut -f1)
success "Backup created: ${BACKUP_FILE} (${BACKUP_SIZE})"

# ── Rotate old backups ──────────────────────────────────────────────────
# Keep only the most recent MAX_BACKUPS files
BACKUP_COUNT=$(find "${BACKUP_DIR}" -name "apex_ai_marketing_*.sql.gz" -type f | wc -l)

if [ "${BACKUP_COUNT}" -gt "${MAX_BACKUPS}" ]; then
    REMOVE_COUNT=$((BACKUP_COUNT - MAX_BACKUPS))
    info "Rotating backups: removing ${REMOVE_COUNT} old backup(s) (keeping ${MAX_BACKUPS})..."

    find "${BACKUP_DIR}" -name "apex_ai_marketing_*.sql.gz" -type f \
        | sort \
        | head -n "${REMOVE_COUNT}" \
        | xargs rm -f

    success "Old backups removed"
fi

# ── Summary ──────────────────────────────────────────────────────────────
CURRENT_COUNT=$(find "${BACKUP_DIR}" -name "apex_ai_marketing_*.sql.gz" -type f | wc -l)
TOTAL_SIZE=$(du -sh "${BACKUP_DIR}" | cut -f1)

echo ""
success "Backup complete!"
info "  File:     ${BACKUP_DIR}/${BACKUP_FILE}"
info "  Size:     ${BACKUP_SIZE}"
info "  Backups:  ${CURRENT_COUNT}/${MAX_BACKUPS}"
info "  Total:    ${TOTAL_SIZE}"
echo ""

# ── Optional: Restore instructions ──────────────────────────────────────
# To restore a backup:
#   gunzip -c backups/apex_ai_marketing_YYYYMMDD_HHMMSS.sql.gz | \
#     docker exec -i apex-db psql -U apex -d apex_ai_marketing
