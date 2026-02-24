# =============================================================================
# Apex AI Marketing - Backend Dockerfile
# =============================================================================
# Multi-stage build for the FastAPI + Celery backend.
# Build context is the project root (not backend/) so that the backend package
# can be properly structured.
#
# Build:  docker build -f backend/Dockerfile -t apex-backend .
# Run:    docker run -p 8000:8000 --env-file .env apex-backend
# =============================================================================

# ── Stage 1: Build dependencies ─────────────────────────────────────────
FROM python:3.11-slim AS builder

# System dependencies required for building Python packages
# Includes WeasyPrint build deps for PDF export support
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    libpq-dev \
    libffi-dev \
    libcairo2-dev \
    libpango1.0-dev \
    libgdk-pixbuf2.0-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

# Copy and install Python dependencies first (layer caching)
COPY backend/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ── Stage 2: Production image ───────────────────────────────────────────
FROM python:3.11-slim

# Runtime system dependencies
# Includes WeasyPrint runtime libs for PDF generation
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi8 \
    fonts-dejavu-core \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user for security
RUN groupadd -r apex && useradd -r -g apex -d /app -s /sbin/nologin apex

WORKDIR /app

# Copy installed Python packages from builder
COPY --from=builder /install /usr/local

# Copy backend source code
COPY backend/ /app/backend/

# Set working directory to backend so bare imports work
WORKDIR /app/backend

# Create deliverables directory
RUN mkdir -p /app/deliverables && chown -R apex:apex /app

# Switch to non-root user
USER apex

# Expose the API port
EXPOSE 8000

# Default command: run the FastAPI application via uvicorn
# Working dir is /app/backend so "main:app" resolves to backend/main.py
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "2"]
