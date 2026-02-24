"""
Apex AI Marketing - Leads API

Lead management with outreach tracking, batch operations,
and pipeline advancement.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_, case
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Lead
from api.auth import get_current_user, UserInfo

router = APIRouter(prefix="/api/leads", tags=["Leads"])


# ── Outreach sequence definitions ────────────────────────────────────
OUTREACH_STEPS = [
    "new",
    "researched",
    "message_drafted",
    "sent",
    "follow_up_1",
    "follow_up_2",
    "follow_up_3",
    "replied",
    "meeting_booked",
    "qualified",
    "not_interested",
]


# ── Pydantic Schemas ─────────────────────────────────────────────────

class LeadCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    linkedin_url: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    market: Optional[str] = Field(None, description="dubai, uk, global, russian_dubai")
    language: str = "en"
    channel: Optional[str] = Field(None, description="linkedin, email, whatsapp, instagram, cold_call")
    source: Optional[str] = None
    outreach_status: str = "new"
    sequence_step: int = 0
    pain_points: Optional[str] = None
    observation: Optional[str] = None
    icp_score: Optional[int] = Field(None, ge=0, le=100, description="Ideal Customer Profile score 0-100")
    notes: Optional[str] = None
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class LeadUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    linkedin_url: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    market: Optional[str] = None
    language: Optional[str] = None
    channel: Optional[str] = None
    source: Optional[str] = None
    outreach_status: Optional[str] = None
    sequence_step: Optional[int] = None
    pain_points: Optional[str] = None
    observation: Optional[str] = None
    icp_score: Optional[int] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class LeadResponse(BaseModel):
    id: uuid.UUID
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    linkedin_url: Optional[str] = None
    website: Optional[str] = None
    industry: Optional[str] = None
    market: Optional[str] = None
    language: str
    channel: Optional[str] = None
    source: Optional[str] = None
    outreach_status: str
    sequence_step: int
    pain_points: Optional[str] = None
    observation: Optional[str] = None
    icp_score: Optional[int] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None
    outreach_history: Optional[list] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class LeadListResponse(BaseModel):
    items: List[LeadResponse]
    total: int
    page: int
    per_page: int
    pages: int


class LeadBatchCreate(BaseModel):
    leads: List[LeadCreate] = Field(..., min_length=1, max_length=500)


class OutreachStats(BaseModel):
    total_leads: int
    by_status: dict
    by_market: dict
    by_channel: dict
    conversion_rate: float


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/stats", response_model=OutreachStats)
async def get_lead_stats(
    market: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get outreach statistics: counts by status, market, and channel."""
    base_filters = []
    if market:
        base_filters.append(Lead.market == market)
    if language:
        base_filters.append(Lead.language == language)

    # Total leads
    total_query = select(func.count(Lead.id))
    if base_filters:
        total_query = total_query.where(and_(*base_filters))
    total_result = await db.execute(total_query)
    total_leads = total_result.scalar() or 0

    # Counts by status
    status_query = (
        select(Lead.outreach_status, func.count(Lead.id))
        .group_by(Lead.outreach_status)
    )
    if base_filters:
        status_query = status_query.where(and_(*base_filters))
    status_result = await db.execute(status_query)
    by_status = {row[0]: row[1] for row in status_result.all()}

    # Counts by market
    market_query = (
        select(Lead.market, func.count(Lead.id))
        .group_by(Lead.market)
    )
    if base_filters:
        market_query = market_query.where(and_(*base_filters))
    market_result = await db.execute(market_query)
    by_market = {(row[0] or "unknown"): row[1] for row in market_result.all()}

    # Counts by channel
    channel_query = (
        select(Lead.channel, func.count(Lead.id))
        .group_by(Lead.channel)
    )
    if base_filters:
        channel_query = channel_query.where(and_(*base_filters))
    channel_result = await db.execute(channel_query)
    by_channel = {(row[0] or "unknown"): row[1] for row in channel_result.all()}

    # Conversion rate: leads that reached 'meeting_booked' or 'qualified'
    converted_statuses = ["meeting_booked", "qualified"]
    converted_query = select(func.count(Lead.id)).where(
        Lead.outreach_status.in_(converted_statuses)
    )
    if base_filters:
        converted_query = converted_query.where(and_(*base_filters))
    converted_result = await db.execute(converted_query)
    converted = converted_result.scalar() or 0
    conversion_rate = round((converted / total_leads * 100) if total_leads > 0 else 0, 2)

    return OutreachStats(
        total_leads=total_leads,
        by_status=by_status,
        by_market=by_market,
        by_channel=by_channel,
        conversion_rate=conversion_rate,
    )


@router.get("/", response_model=LeadListResponse)
async def list_leads(
    outreach_status: Optional[str] = Query(None, description="Filter by outreach status"),
    market: Optional[str] = Query(None, description="Filter by market"),
    language: Optional[str] = Query(None, description="Filter by language"),
    channel: Optional[str] = Query(None, description="Filter by channel"),
    source: Optional[str] = Query(None, description="Filter by source"),
    search: Optional[str] = Query(None, description="Search by name, company, or email"),
    min_icp_score: Optional[int] = Query(None, ge=0, le=100),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """List leads with optional filters and pagination."""
    query = select(Lead)
    count_query = select(func.count(Lead.id))

    filters = []
    if outreach_status:
        filters.append(Lead.outreach_status == outreach_status)
    if market:
        filters.append(Lead.market == market)
    if language:
        filters.append(Lead.language == language)
    if channel:
        filters.append(Lead.channel == channel)
    if source:
        filters.append(Lead.source == source)
    if min_icp_score is not None:
        filters.append(Lead.icp_score >= min_icp_score)
    if search:
        search_filter = f"%{search}%"
        filters.append(
            (Lead.name.ilike(search_filter))
            | (Lead.company.ilike(search_filter))
            | (Lead.email.ilike(search_filter))
        )

    if filters:
        combined = and_(*filters)
        query = query.where(combined)
        count_query = count_query.where(combined)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    pages = max(1, (total + per_page - 1) // per_page)
    offset = (page - 1) * per_page

    query = query.order_by(Lead.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    leads = result.scalars().all()

    return LeadListResponse(
        items=[LeadResponse.model_validate(l) for l in leads],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get("/{id}", response_model=LeadResponse)
async def get_lead(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get lead details with outreach history."""
    result = await db.execute(select(Lead).where(Lead.id == id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")
    return LeadResponse.model_validate(lead)


@router.post("/", response_model=LeadResponse, status_code=status.HTTP_201_CREATED)
async def create_lead(
    payload: LeadCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create a new lead."""
    lead = Lead(
        id=uuid.uuid4(),
        **payload.model_dump(),
    )
    db.add(lead)
    await db.flush()
    await db.refresh(lead)
    return LeadResponse.model_validate(lead)


@router.put("/{id}", response_model=LeadResponse)
async def update_lead(
    id: uuid.UUID,
    payload: LeadUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Update a lead."""
    result = await db.execute(select(Lead).where(Lead.id == id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(lead, field, value)
    lead.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(lead)
    return LeadResponse.model_validate(lead)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_lead(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Delete a lead permanently."""
    result = await db.execute(select(Lead).where(Lead.id == id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    await db.delete(lead)
    await db.flush()
    return {"detail": "Lead deleted", "id": str(id)}


@router.post("/batch", status_code=status.HTTP_201_CREATED)
async def create_leads_batch(
    payload: LeadBatchCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create multiple leads in a single batch operation."""
    created_ids = []
    errors = []

    for idx, lead_data in enumerate(payload.leads):
        try:
            lead = Lead(
                id=uuid.uuid4(),
                **lead_data.model_dump(),
            )
            db.add(lead)
            created_ids.append(str(lead.id))
        except Exception as e:
            errors.append({"index": idx, "error": str(e)})

    await db.flush()

    return {
        "created": len(created_ids),
        "errors": len(errors),
        "created_ids": created_ids,
        "error_details": errors if errors else None,
    }


@router.post("/{id}/advance", response_model=LeadResponse)
async def advance_lead(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Advance a lead to the next outreach step in the sequence.

    Sequence: new -> researched -> message_drafted -> sent ->
    follow_up_1 -> follow_up_2 -> follow_up_3 -> replied ->
    meeting_booked -> qualified
    """
    result = await db.execute(select(Lead).where(Lead.id == id))
    lead = result.scalar_one_or_none()
    if not lead:
        raise HTTPException(status_code=404, detail="Lead not found")

    current_status = lead.outreach_status
    if current_status == "not_interested":
        raise HTTPException(
            status_code=400,
            detail="Cannot advance: lead is marked as not interested",
        )
    if current_status == "qualified":
        raise HTTPException(
            status_code=400,
            detail="Cannot advance: lead is already qualified (end of sequence)",
        )

    # Find next step
    try:
        current_index = OUTREACH_STEPS.index(current_status)
    except ValueError:
        current_index = -1

    next_index = current_index + 1
    # Skip 'not_interested' in advancement
    if next_index < len(OUTREACH_STEPS) and OUTREACH_STEPS[next_index] == "not_interested":
        next_index += 1

    if next_index >= len(OUTREACH_STEPS):
        raise HTTPException(
            status_code=400,
            detail="Lead is already at the final outreach step",
        )

    new_status = OUTREACH_STEPS[next_index]
    lead.outreach_status = new_status
    lead.sequence_step = next_index

    # Update outreach history
    history_entry = {
        "from": current_status,
        "to": new_status,
        "timestamp": datetime.utcnow().isoformat(),
        "advanced_by": current_user.username,
    }
    if lead.outreach_history is None:
        lead.outreach_history = []
    lead.outreach_history = lead.outreach_history + [history_entry]

    lead.updated_at = datetime.utcnow()
    await db.flush()
    await db.refresh(lead)
    return LeadResponse.model_validate(lead)
