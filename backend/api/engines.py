"""
Apex AI Marketing - Engine Configuration API

Engine type definitions, pricing, and deliverable template management.
Provides the configuration layer that powers the engine engagement system.
"""

import uuid
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Task
from api.auth import get_current_user, UserInfo

router = APIRouter(prefix="/api/engine-config", tags=["Engine Configuration"])


# ── Static Engine Type Definitions ───────────────────────────────────
# These define the available engine types, their descriptions, and pricing.

ENGINE_TYPES = {
    "seo": {
        "name": "SEO Engine",
        "description": (
            "Search engine optimization infrastructure: technical SEO audits, "
            "keyword strategy, on-page optimization, link building, and "
            "local SEO for multi-market presence."
        ),
        "deliverables": [
            "technical_audit",
            "keyword_research",
            "on_page_optimization",
            "link_building_plan",
            "local_seo_setup",
            "monthly_report",
        ],
        "pricing": {
            "starter": 2500,
            "growth": 5000,
            "scale": 10000,
            "currency": "USD",
        },
    },
    "content": {
        "name": "Content Engine",
        "description": (
            "AI-powered content production: blog posts, landing pages, "
            "case studies, whitepapers, email sequences, and social media "
            "content in multiple languages."
        ),
        "deliverables": [
            "blog_post",
            "landing_page",
            "case_study",
            "whitepaper",
            "email_sequence",
            "social_media_pack",
            "video_script",
        ],
        "pricing": {
            "starter": 2000,
            "growth": 4000,
            "scale": 8000,
            "currency": "USD",
        },
    },
    "ads": {
        "name": "Paid Ads Engine",
        "description": (
            "Performance marketing: Google Ads, Meta Ads, LinkedIn Ads, "
            "TikTok Ads setup, optimization, and creative production."
        ),
        "deliverables": [
            "campaign_setup",
            "ad_creative",
            "landing_page",
            "audience_research",
            "monthly_optimization",
            "performance_report",
        ],
        "pricing": {
            "starter": 2000,
            "growth": 4500,
            "scale": 9000,
            "currency": "USD",
            "note": "Plus ad spend (managed separately)",
        },
    },
    "social": {
        "name": "Social Media Engine",
        "description": (
            "Social media management: content calendar, post creation, "
            "community management, influencer outreach, and analytics."
        ),
        "deliverables": [
            "content_calendar",
            "social_posts",
            "story_templates",
            "reel_scripts",
            "community_management",
            "monthly_analytics",
        ],
        "pricing": {
            "starter": 1500,
            "growth": 3500,
            "scale": 7000,
            "currency": "USD",
        },
    },
    "email": {
        "name": "Email Marketing Engine",
        "description": (
            "Email automation: welcome sequences, nurture flows, "
            "newsletters, re-engagement campaigns, and deliverability optimization."
        ),
        "deliverables": [
            "welcome_sequence",
            "nurture_flow",
            "newsletter_template",
            "re_engagement_campaign",
            "deliverability_audit",
            "monthly_report",
        ],
        "pricing": {
            "starter": 1500,
            "growth": 3000,
            "scale": 6000,
            "currency": "USD",
        },
    },
    "web": {
        "name": "Web Development Engine",
        "description": (
            "Website infrastructure: design, development, optimization, "
            "CRO (conversion rate optimization), and ongoing maintenance."
        ),
        "deliverables": [
            "website_audit",
            "wireframes",
            "design_mockups",
            "development",
            "cro_optimization",
            "maintenance",
        ],
        "pricing": {
            "starter": 3000,
            "growth": 7500,
            "scale": 15000,
            "currency": "USD",
            "note": "One-time setup + monthly maintenance",
        },
    },
    "analytics": {
        "name": "Analytics Engine",
        "description": (
            "Data infrastructure: GA4 setup, tag management, dashboards, "
            "attribution modeling, and custom reporting."
        ),
        "deliverables": [
            "analytics_audit",
            "ga4_setup",
            "tag_management",
            "custom_dashboard",
            "attribution_model",
            "monthly_insights",
        ],
        "pricing": {
            "starter": 2000,
            "growth": 4000,
            "scale": 8000,
            "currency": "USD",
        },
    },
    "branding": {
        "name": "Branding Engine",
        "description": (
            "Brand infrastructure: brand strategy, visual identity, "
            "messaging framework, brand guidelines, and brand voice documentation."
        ),
        "deliverables": [
            "brand_audit",
            "brand_strategy",
            "visual_identity",
            "messaging_framework",
            "brand_guidelines",
            "brand_voice_doc",
        ],
        "pricing": {
            "starter": 3000,
            "growth": 6000,
            "scale": 12000,
            "currency": "USD",
            "note": "One-time project pricing",
        },
    },
}


# ── Pydantic Schemas ─────────────────────────────────────────────────

class EngineTypeResponse(BaseModel):
    key: str
    name: str
    description: str
    deliverables: List[str]
    pricing: dict


class EngineTemplateCreate(BaseModel):
    engine_name: str = Field(..., description="Engine type key: seo, content, ads, etc.")
    deliverable_type: str = Field(..., description="Type of deliverable this template is for")
    name: str = Field(..., min_length=1, max_length=255)
    description: Optional[str] = None
    template_content: str = Field(..., min_length=1, description="Template content/structure")
    language: str = "en"
    variables: Optional[List[str]] = Field(
        None,
        description="Template variables e.g. ['client_name', 'industry', 'keyword']",
    )
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class EngineTemplateResponse(BaseModel):
    id: uuid.UUID
    engine_name: str
    deliverable_type: str
    name: str
    description: Optional[str] = None
    template_content: str
    language: str
    variables: Optional[List[str]] = None
    metadata: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/types", response_model=List[EngineTypeResponse])
async def list_engine_types(
    current_user: UserInfo = Depends(get_current_user),
):
    """List all engine types with descriptions and pricing.

    Returns the full catalog of available marketing engines
    with their deliverable types and pricing tiers.
    """
    return [
        EngineTypeResponse(
            key=key,
            name=config["name"],
            description=config["description"],
            deliverables=config["deliverables"],
            pricing=config["pricing"],
        )
        for key, config in ENGINE_TYPES.items()
    ]


@router.get("/templates", response_model=List[EngineTemplateResponse])
async def list_engine_templates(
    engine_name: Optional[str] = Query(None, description="Filter by engine type"),
    deliverable_type: Optional[str] = Query(None, description="Filter by deliverable type"),
    language: Optional[str] = Query(None, description="Filter by language"),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get engine deliverable templates.

    Templates are stored as Task records with task_type='engine_template'.
    """
    query = select(Task).where(Task.task_type == "engine_template")
    query = query.order_by(Task.created_at.desc())

    result = await db.execute(query)
    tasks = result.scalars().all()

    templates = []
    for t in tasks:
        meta = t.metadata or {}
        t_engine = meta.get("engine_name", "")
        t_del_type = meta.get("deliverable_type", "")
        t_language = meta.get("language", "en")

        # Apply filters
        if engine_name and t_engine != engine_name:
            continue
        if deliverable_type and t_del_type != deliverable_type:
            continue
        if language and t_language != language:
            continue

        templates.append(
            EngineTemplateResponse(
                id=t.id,
                engine_name=t_engine,
                deliverable_type=t_del_type,
                name=t.title,
                description=t.description,
                template_content=meta.get("template_content", ""),
                language=t_language,
                variables=meta.get("variables"),
                metadata=meta,
                created_at=t.created_at,
                updated_at=t.updated_at or t.created_at,
            )
        )

    return templates


@router.post("/templates", response_model=EngineTemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_or_update_engine_template(
    payload: EngineTemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create or update an engine deliverable template.

    If a template for the same engine_name + deliverable_type + language
    already exists, it will be updated. Otherwise, a new one is created.
    """
    # Validate engine name
    if payload.engine_name not in ENGINE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid engine name '{payload.engine_name}'. "
                   f"Valid engines: {', '.join(ENGINE_TYPES.keys())}",
        )

    # Validate deliverable type
    valid_deliverables = ENGINE_TYPES[payload.engine_name]["deliverables"]
    if payload.deliverable_type not in valid_deliverables:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid deliverable type '{payload.deliverable_type}' for engine "
                   f"'{payload.engine_name}'. Valid types: {', '.join(valid_deliverables)}",
        )

    # Check for existing template
    existing_result = await db.execute(
        select(Task).where(
            and_(
                Task.task_type == "engine_template",
                Task.metadata["engine_name"].astext == payload.engine_name,
                Task.metadata["deliverable_type"].astext == payload.deliverable_type,
                Task.metadata["language"].astext == payload.language,
            )
        )
    )
    existing = existing_result.scalar_one_or_none()

    meta = {
        "engine_name": payload.engine_name,
        "deliverable_type": payload.deliverable_type,
        "template_content": payload.template_content,
        "language": payload.language,
        "variables": payload.variables,
    }
    if payload.metadata:
        meta.update(payload.metadata)

    if existing:
        # Update existing template
        existing.title = payload.name
        existing.description = payload.description
        existing.metadata = meta
        existing.updated_at = datetime.utcnow()
        await db.flush()
        await db.refresh(existing)
        task = existing
    else:
        # Create new template
        task = Task(
            id=uuid.uuid4(),
            title=payload.name,
            description=payload.description,
            task_type="engine_template",
            assigned_agent="system",
            status="active",
            metadata=meta,
        )
        db.add(task)
        await db.flush()
        await db.refresh(task)

    return EngineTemplateResponse(
        id=task.id,
        engine_name=payload.engine_name,
        deliverable_type=payload.deliverable_type,
        name=task.title,
        description=task.description,
        template_content=payload.template_content,
        language=payload.language,
        variables=payload.variables,
        metadata=meta,
        created_at=task.created_at,
        updated_at=task.updated_at or task.created_at,
    )
