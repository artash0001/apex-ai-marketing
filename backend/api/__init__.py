"""
Apex AI Marketing - API Package

All FastAPI routers are defined here and can be included in the main app.
"""

from api.auth import router as auth_router
from api.clients import router as clients_router
from api.projects import router as projects_router
from api.content import router as content_router
from api.leads import router as leads_router
from api.reports import router as reports_router
from api.outreach import router as outreach_router
from api.experiments import router as experiments_router
from api.engines import router as engines_router
from api.webhooks import router as webhooks_router

all_routers = [
    auth_router,
    clients_router,
    projects_router,
    content_router,
    leads_router,
    reports_router,
    outreach_router,
    experiments_router,
    engines_router,
    webhooks_router,
]

__all__ = [
    "auth_router",
    "clients_router",
    "projects_router",
    "content_router",
    "leads_router",
    "reports_router",
    "outreach_router",
    "experiments_router",
    "engines_router",
    "webhooks_router",
    "all_routers",
]
