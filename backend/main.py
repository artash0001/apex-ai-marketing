"""
Apex AI Marketing - FastAPI Application Entry Point

Main application setup: middleware, routers, startup events, health checks.
"""

import logging
from contextlib import asynccontextmanager
from datetime import datetime, timezone

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from pathlib import Path

from config import get_settings
from database import init_db

settings = get_settings()

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)-7s | %(name)s | %(message)s",
)
logger = logging.getLogger(__name__)


# ── Lifespan: startup / shutdown ──────────────────────────────────────

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Run initialization on startup and cleanup on shutdown."""
    logger.info("Starting %s backend ...", settings.BRAND_NAME)
    await init_db()
    logger.info("Database tables created / verified.")
    yield
    logger.info("Shutting down %s backend.", settings.BRAND_NAME)


# ── Create FastAPI app ────────────────────────────────────────────────

app = FastAPI(
    title=f"{settings.BRAND_NAME} API",
    version="2.0.0",
    description="AI Growth Infrastructure Agency - Backend API",
    lifespan=lifespan,
)

# ── CORS middleware ───────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Tighten in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Mount static files ────────────────────────────────────────────────
static_dir = Path(__file__).resolve().parent / settings.STATIC_DIR
static_dir.mkdir(parents=True, exist_ok=True)
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# ── Include API routers ───────────────────────────────────────────────
from api import all_routers  # noqa: E402

for _router in all_routers:
    app.include_router(_router)


# ── Health check ──────────────────────────────────────────────────────

@app.get("/health", tags=["System"])
async def health_check():
    """Health-check endpoint for uptime monitoring."""
    return {
        "status": "healthy",
        "service": settings.BRAND_NAME,
        "version": "2.0.0",
        "timestamp": datetime.now(timezone.utc).isoformat(),
    }


@app.get("/", tags=["System"])
async def root():
    """Root endpoint - basic service info."""
    return {
        "service": f"{settings.BRAND_NAME} API",
        "version": "2.0.0",
        "docs": "/docs",
        "health": "/health",
    }


# ── Run with uvicorn (development) ───────────────────────────────────
if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
    )
