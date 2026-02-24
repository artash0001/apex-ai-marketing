"""
Apex AI Marketing - Engine Engagements API (Projects)

Manage engine engagements (the core service delivery units),
including pipeline views and deliverable attachment.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import Dict, List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import EngineEngagement, Deliverable, Client
from api.auth import get_current_user, UserInfo

router = APIRouter(prefix="/api/engines", tags=["Engine Engagements"])


# ── Pydantic Schemas ─────────────────────────────────────────────────

class EngineEngagementCreate(BaseModel):
    client_id: uuid.UUID
    engine_name: str = Field(
        ...,
        description="Engine type: seo, content, ads, social, email, web, analytics, branding",
    )
    status: str = "scoping"
    scope: Optional[dict] = None
    monthly_value: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class EngineEngagementUpdate(BaseModel):
    engine_name: Optional[str] = None
    status: Optional[str] = None
    scope: Optional[dict] = None
    monthly_value: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    notes: Optional[str] = None

    model_config = {"from_attributes": True}


class EngineEngagementResponse(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    engine_name: str
    status: str
    scope: Optional[dict] = None
    monthly_value: Optional[Decimal] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    notes: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class EngineEngagementDetailResponse(EngineEngagementResponse):
    client_name: Optional[str] = None
    deliverables: List[dict] = []


class DeliverableAdd(BaseModel):
    title: str = Field(..., min_length=1)
    type: str = Field(..., description="blog, landing_page, email, social_post, ad_copy, report, audit, etc.")
    content: Optional[str] = None
    status: str = "draft"
    notes: Optional[str] = None


class PipelineResponse(BaseModel):
    engine_name: str
    statuses: Dict[str, List[dict]]


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/pipeline", response_model=List[PipelineResponse])
async def get_pipeline(
    engine_name: Optional[str] = Query(None, description="Filter by engine type"),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get kanban pipeline data grouped by status for each engine type.

    Returns engagements organized by engine type and status for
    kanban board visualization.
    """
    query = select(EngineEngagement)
    if engine_name:
        query = query.where(EngineEngagement.engine_name == engine_name)
    query = query.order_by(EngineEngagement.engine_name, EngineEngagement.created_at.desc())

    result = await db.execute(query)
    engagements = result.scalars().all()

    # Group by engine_name, then by status
    pipeline: Dict[str, Dict[str, list]] = {}
    for e in engagements:
        if e.engine_name not in pipeline:
            pipeline[e.engine_name] = {}
        if e.status not in pipeline[e.engine_name]:
            pipeline[e.engine_name][e.status] = []
        pipeline[e.engine_name][e.status].append(
            {
                "id": str(e.id),
                "client_id": str(e.client_id),
                "status": e.status,
                "monthly_value": float(e.monthly_value) if e.monthly_value else None,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
        )

    return [
        PipelineResponse(engine_name=name, statuses=statuses)
        for name, statuses in pipeline.items()
    ]


@router.get("/", response_model=List[EngineEngagementResponse])
async def list_engine_engagements(
    status: Optional[str] = Query(None, description="Filter by status"),
    engine_name: Optional[str] = Query(None, description="Filter by engine type"),
    client_id: Optional[uuid.UUID] = Query(None, description="Filter by client"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """List all engine engagements with optional filters."""
    query = select(EngineEngagement)
    filters = []

    if status:
        filters.append(EngineEngagement.status == status)
    if engine_name:
        filters.append(EngineEngagement.engine_name == engine_name)
    if client_id:
        filters.append(EngineEngagement.client_id == client_id)

    if filters:
        query = query.where(and_(*filters))

    offset = (page - 1) * per_page
    query = query.order_by(EngineEngagement.created_at.desc()).offset(offset).limit(per_page)

    result = await db.execute(query)
    engagements = result.scalars().all()

    return [EngineEngagementResponse.model_validate(e) for e in engagements]


@router.get("/{id}", response_model=EngineEngagementDetailResponse)
async def get_engine_engagement(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get engine engagement details with deliverables."""
    result = await db.execute(
        select(EngineEngagement).where(EngineEngagement.id == id)
    )
    engagement = result.scalar_one_or_none()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engine engagement not found")

    # Get client name
    client_result = await db.execute(
        select(Client.name).where(Client.id == engagement.client_id)
    )
    client_name = client_result.scalar_one_or_none()

    # Get deliverables
    del_result = await db.execute(
        select(Deliverable)
        .where(Deliverable.engine_engagement_id == id)
        .order_by(Deliverable.created_at.desc())
    )
    deliverables = del_result.scalars().all()
    deliverable_dicts = [
        {
            "id": str(d.id),
            "title": d.title,
            "type": d.type,
            "status": d.status,
            "created_at": d.created_at.isoformat() if d.created_at else None,
        }
        for d in deliverables
    ]

    response = EngineEngagementDetailResponse.model_validate(engagement)
    response.client_name = client_name
    response.deliverables = deliverable_dicts
    return response


@router.post("/", response_model=EngineEngagementResponse, status_code=status.HTTP_201_CREATED)
async def create_engine_engagement(
    payload: EngineEngagementCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create a new engine engagement."""
    # Verify client exists
    client_result = await db.execute(
        select(Client).where(Client.id == payload.client_id)
    )
    if not client_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Client not found")

    engagement = EngineEngagement(
        id=uuid.uuid4(),
        **payload.model_dump(),
    )
    db.add(engagement)
    await db.flush()
    await db.refresh(engagement)
    return EngineEngagementResponse.model_validate(engagement)


@router.put("/{id}", response_model=EngineEngagementResponse)
async def update_engine_engagement(
    id: uuid.UUID,
    payload: EngineEngagementUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Update an engine engagement (status, scope, deliverables, etc.)."""
    result = await db.execute(
        select(EngineEngagement).where(EngineEngagement.id == id)
    )
    engagement = result.scalar_one_or_none()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engine engagement not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(engagement, field, value)
    engagement.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(engagement)
    return EngineEngagementResponse.model_validate(engagement)


@router.post("/{id}/deliverables", status_code=status.HTTP_201_CREATED)
async def add_deliverable_to_engagement(
    id: uuid.UUID,
    payload: DeliverableAdd,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Add a deliverable to an engine engagement."""
    # Verify engagement exists
    eng_result = await db.execute(
        select(EngineEngagement).where(EngineEngagement.id == id)
    )
    engagement = eng_result.scalar_one_or_none()
    if not engagement:
        raise HTTPException(status_code=404, detail="Engine engagement not found")

    deliverable = Deliverable(
        id=uuid.uuid4(),
        client_id=engagement.client_id,
        engine_engagement_id=id,
        title=payload.title,
        type=payload.type,
        content=payload.content,
        status=payload.status,
        notes=payload.notes,
    )
    db.add(deliverable)
    await db.flush()
    await db.refresh(deliverable)

    return {
        "id": str(deliverable.id),
        "title": deliverable.title,
        "type": deliverable.type,
        "status": deliverable.status,
        "engine_engagement_id": str(id),
        "client_id": str(engagement.client_id),
        "created_at": deliverable.created_at.isoformat() if deliverable.created_at else None,
    }
