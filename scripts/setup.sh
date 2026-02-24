#!/usr/bin/env bash
# =============================================================================
# Apex AI Marketing - Setup Script
# =============================================================================
# Complete setup for the Docker-based deployment.
#
# Usage:
#   chmod +x scripts/setup.sh
#   ./scripts/setup.sh
#
# What it does:
#   1. Checks that Docker and Docker Compose are installed
#   2. Creates .env from .env.example if it doesn't exist
#   3. Builds all Docker images
#   4. Starts all services
#   5. Waits for the database to be ready
#   6. Runs database table creation (via the FastAPI startup event)
#   7. Prints service status and URLs
# =============================================================================

set -euo pipefail

# ── Colors for output ────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# ── Helper functions ─────────────────────────────────────────────────────
info()    { echo -e "${BLUE}[INFO]${NC} $*"; }
success() { echo -e "${GREEN}[OK]${NC} $*"; }
warn()    { echo -e "${YELLOW}[WARN]${NC} $*"; }
error()   { echo -e "${RED}[ERROR]${NC} $*"; exit 1; }

# ── Navigate to project root ────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
cd "${PROJECT_ROOT}"

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Apex AI Marketing - Setup${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""

# ── Step 1: Check prerequisites ─────────────────────────────────────────
info "Checking prerequisites..."

if ! command -v docker &> /dev/null; then
    error "Docker is not installed. Install it from https://docs.docker.com/engine/install/"
fi
success "Docker found: $(docker --version)"

# Check for docker compose (v2 plugin) or docker-compose (v1 standalone)
if docker compose version &> /dev/null; then
    COMPOSE_CMD="docker compose"
    success "Docker Compose found: $(docker compose version --short)"
elif command -v docker-compose &> /dev/null; then
    COMPOSE_CMD="docker-compose"
    success "Docker Compose found: $(docker-compose --version)"
else
    error "Docker Compose is not installed. Install it from https://docs.docker.com/compose/install/"
fi

# Check if Docker daemon is running
if ! docker info &> /dev/null 2>&1; then
    error "Docker daemon is not running. Start it with: sudo systemctl start docker"
fi
success "Docker daemon is running"

echo ""

# ── Step 2: Environment file ────────────────────────────────────────────
info "Checking environment configuration..."

if [ ! -f .env ]; then
    if [ -f .env.example ]; then
        cp .env.example .env
        warn ".env file created from .env.example"
        echo ""
        echo -e "${YELLOW}  IMPORTANT: Edit .env with your actual values before continuing!${NC}"
        echo -e "${YELLOW}  At minimum, set these variables:${NC}"
        echo -e "${YELLOW}    - POSTGRES_PASSWORD (and match in DATABASE_URL)${NC}"
        echo -e "${YELLOW}    - JWT_SECRET (generate with: python3 -c \"import secrets; print(secrets.token_hex(32))\")${NC}"
        echo -e "${YELLOW}    - ANTHROPIC_API_KEY${NC}"
        echo -e "${YELLOW}    - TELEGRAM_BOT_TOKEN & TELEGRAM_CHAT_ID${NC}"
        echo -e "${YELLOW}    - ADMIN_PASSWORD${NC}"
        echo ""
        read -rp "Press Enter after editing .env, or Ctrl+C to abort... "
    else
        error ".env.example not found. Cannot create .env file."
    fi
else
    success ".env file already exists"
fi

# Quick validation: check that placeholder values have been changed
if grep -q "your-secure-password" .env 2>/dev/null; then
    warn "Detected placeholder passwords in .env - make sure to change them before going to production!"
fi

echo ""

# ── Step 3: Create required directories ──────────────────────────────────
info "Creating required directories..."

mkdir -p backups
success "Backup directory ready"

echo ""

# ── Step 4: Build Docker images ──────────────────────────────────────────
info "Building Docker images (this may take a few minutes on first run)..."

${COMPOSE_CMD} build --parallel 2>&1 | tail -20

success "All Docker images built successfully"
echo ""

# ── Step 5: Start services ───────────────────────────────────────────────
info "Starting all services..."

${COMPOSE_CMD} up -d

success "All services started"
echo ""

# ── Step 6: Wait for database readiness ──────────────────────────────────
info "Waiting for PostgreSQL to be ready..."

MAX_RETRIES=30
RETRY_COUNT=0

while [ ${RETRY_COUNT} -lt ${MAX_RETRIES} ]; do
    if ${COMPOSE_CMD} exec -T db pg_isready -U "${POSTGRES_USER:-apex}" -d "${POSTGRES_DB:-apex_ai_marketing}" &> /dev/null; then
        success "PostgreSQL is ready"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ ${RETRY_COUNT} -eq ${MAX_RETRIES} ]; then
        error "PostgreSQL failed to become ready after ${MAX_RETRIES} attempts"
    fi
    echo -n "."
    sleep 2
done

echo ""

# ── Step 7: Wait for backend readiness ───────────────────────────────────
info "Waiting for backend API to be ready..."

RETRY_COUNT=0
while [ ${RETRY_COUNT} -lt ${MAX_RETRIES} ]; do
    if curl -sf http://localhost:8100/health &> /dev/null; then
        success "Backend API is healthy"
        break
    fi
    RETRY_COUNT=$((RETRY_COUNT + 1))
    if [ ${RETRY_COUNT} -eq ${MAX_RETRIES} ]; then
        warn "Backend health check timed out - check logs with: ${COMPOSE_CMD} logs backend"
    fi
    echo -n "."
    sleep 2
done

echo ""

# ── Step 8: Initialize database tables ───────────────────────────────────
info "Initializing database tables..."

# The FastAPI app creates tables on startup via Base.metadata.create_all
# But we can also trigger it explicitly via a quick Python command
${COMPOSE_CMD} exec -T backend python -c "
from backend.database import Base, engine
from backend import models
import asyncio

async def init():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print('Database tables created successfully')

asyncio.run(init())
" 2>/dev/null && success "Database tables initialized" || warn "Table initialization via exec failed (tables may already exist from app startup)"

echo ""

# ── Step 9: Print status ────────────────────────────────────────────────
info "Checking service status..."
echo ""

${COMPOSE_CMD} ps

echo ""
echo -e "${CYAN}========================================${NC}"
echo -e "${CYAN}  Setup Complete!${NC}"
echo -e "${CYAN}========================================${NC}"
echo ""
echo -e "${GREEN}Services are running at:${NC}"
echo -e "  Backend API:    http://localhost:8100"
echo -e "  API Docs:       http://localhost:8100/docs"
echo -e "  Health Check:   http://localhost:8100/health"
echo -e "  Admin Panel:    http://localhost:8101"
echo -e "  Frontend:       http://localhost:8102"
echo -e "  PostgreSQL:     localhost:5433"
echo -e "  Redis:          localhost:6380"
echo ""
echo -e "${GREEN}With Caddy configured, access via:${NC}"
echo -e "  Frontend:       https://apexaimarketing.pro"
echo -e "  Admin Panel:    https://apexaimarketing.pro/admin/"
echo -e "  API:            https://apexaimarketing.pro/api/"
echo -e "  Health:         https://apexaimarketing.pro/health"
echo ""
echo -e "${BLUE}Useful commands:${NC}"
echo -e "  View logs:      ${COMPOSE_CMD} logs -f"
echo -e "  View service:   ${COMPOSE_CMD} logs -f backend"
echo -e "  Stop all:       ${COMPOSE_CMD} down"
echo -e "  Restart:        ${COMPOSE_CMD} restart"
echo -e "  Rebuild:        ${COMPOSE_CMD} up -d --build"
echo -e "  DB backup:      ./scripts/backup.sh"
echo ""
