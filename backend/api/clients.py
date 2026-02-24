"""
Apex AI Marketing - Clients API

CRUD operations for agency clients, including engine engagement
and deliverable retrieval, plus infrastructure audit triggering.
"""

import uuid
from datetime import datetime
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field, EmailStr
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Client, EngineEngagement, Deliverable, Task
from api.auth import get_current_user, UserInfo

router = APIRouter(prefix="/api/clients", tags=["Clients"])


# ── Pydantic Schemas ─────────────────────────────────────────────────

class ClientCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    language: str = "en"
    brand_voice_doc: Optional[str] = None
    status: str = "lead"
    monthly_value: Optional[Decimal] = None
    notes: Optional[str] = None
    market: Optional[str] = None

    model_config = {"from_attributes": True}


class ClientUpdate(BaseModel):
    name: Optional[str] = None
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    language: Optional[str] = None
    brand_voice_doc: Optional[str] = None
    status: Optional[str] = None
    active_engines: Optional[list] = None
    monthly_value: Optional[Decimal] = None
    notes: Optional[str] = None
    onboarding_completed: Optional[bool] = None
    market: Optional[str] = None

    model_config = {"from_attributes": True}


class ClientResponse(BaseModel):
    id: uuid.UUID
    name: str
    company: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    whatsapp: Optional[str] = None
    telegram: Optional[str] = None
    industry: Optional[str] = None
    website: Optional[str] = None
    language: str
    brand_voice_doc: Optional[str] = None
    status: str
    active_engines: Optional[list] = None
    monthly_value: Optional[Decimal] = None
    notes: Optional[str] = None
    onboarding_completed: bool
    market: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ClientDetailResponse(ClientResponse):
    engine_engagements: List[dict] = []
    deliverables_count: int = 0


class ClientListResponse(BaseModel):
    items: List[ClientResponse]
    total: int
    page: int
    per_page: int
    pages: int


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/", response_model=ClientListResponse)
async def list_clients(
    status: Optional[str] = Query(None, description="Filter by status"),
    market: Optional[str] = Query(None, description="Filter by market"),
    language: Optional[str] = Query(None, description="Filter by language"),
    search: Optional[str] = Query(None, description="Search by name, company, or email"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """List all clients with optional filters and pagination."""
    query = select(Client)
    count_query = select(func.count(Client.id))

    # Apply filters
    filters = []
    if status:
        filters.append(Client.status == status)
    if market:
        filters.append(Client.market == market)
    if language:
        filters.append(Client.language == language)
    if search:
        search_filter = f"%{search}%"
        filters.append(
            (Client.name.ilike(search_filter))
            | (Client.company.ilike(search_filter))
            | (Client.email.ilike(search_filter))
        )

    if filters:
        combined = and_(*filters)
        query = query.where(combined)
        count_query = count_query.where(combined)

    # Get total count
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Pagination
    pages = max(1, (total + per_page - 1) // per_page)
    offset = (page - 1) * per_page
    query = query.order_by(Client.created_at.desc()).offset(offset).limit(per_page)

    result = await db.execute(query)
    clients = result.scalars().all()

    return ClientListResponse(
        items=[ClientResponse.model_validate(c) for c in clients],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get("/{id}", response_model=ClientDetailResponse)
async def get_client(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get client details with engine engagements and deliverables count."""
    result = await db.execute(select(Client).where(Client.id == id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get engine engagements
    eng_result = await db.execute(
        select(EngineEngagement).where(EngineEngagement.client_id == id)
    )
    engagements = eng_result.scalars().all()
    engagement_dicts = [
        {
            "id": str(e.id),
            "engine_name": e.engine_name,
            "status": e.status,
            "created_at": e.created_at.isoformat() if e.created_at else None,
        }
        for e in engagements
    ]

    # Get deliverables count
    del_count_result = await db.execute(
        select(func.count(Deliverable.id)).where(Deliverable.client_id == id)
    )
    deliverables_count = del_count_result.scalar() or 0

    response = ClientDetailResponse.model_validate(client)
    response.engine_engagements = engagement_dicts
    response.deliverables_count = deliverables_count
    return response


@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
async def create_client(
    payload: ClientCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create a new client from form submission or manual entry."""
    client = Client(
        id=uuid.uuid4(),
        **payload.model_dump(),
    )
    db.add(client)
    await db.flush()
    await db.refresh(client)
    return ClientResponse.model_validate(client)


@router.put("/{id}", response_model=ClientResponse)
async def update_client(
    id: uuid.UUID,
    payload: ClientUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Update an existing client."""
    result = await db.execute(select(Client).where(Client.id == id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(client, field, value)
    client.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(client)
    return ClientResponse.model_validate(client)


@router.delete("/{id}", status_code=status.HTTP_200_OK)
async def delete_client(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Soft delete a client by setting status to 'churned'."""
    result = await db.execute(select(Client).where(Client.id == id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    client.status = "churned"
    client.updated_at = datetime.utcnow()
    await db.flush()
    return {"detail": "Client marked as churned", "id": str(id)}


@router.post("/{id}/trigger-audit")
async def trigger_audit(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Trigger an infrastructure audit for the client.

    Creates a task for the Infrastructure Auditor agent and updates
    the client status to 'audit_requested'.
    """
    result = await db.execute(select(Client).where(Client.id == id))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Update client status
    client.status = "audit_requested"
    client.updated_at = datetime.utcnow()

    # Create a task for the Infrastructure Auditor agent
    task = Task(
        id=uuid.uuid4(),
        client_id=id,
        title=f"Infrastructure Audit: {client.name}",
        description=(
            f"Perform a full AI infrastructure audit for {client.name} "
            f"({client.company or 'N/A'}). "
            f"Website: {client.website or 'N/A'}. "
            f"Industry: {client.industry or 'N/A'}. "
            f"Market: {client.market or 'N/A'}."
        ),
        task_type="infrastructure_audit",
        assigned_agent="infrastructure_auditor",
        status="pending",
    )
    db.add(task)
    await db.flush()

    return {
        "detail": "Infrastructure audit triggered",
        "client_id": str(id),
        "task_id": str(task.id),
    }


@router.get("/{id}/deliverables")
async def get_client_deliverables(
    id: uuid.UUID,
    status: Optional[str] = Query(None, description="Filter by deliverable status"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get all deliverables for a specific client."""
    # Verify client exists
    client_result = await db.execute(select(Client).where(Client.id == id))
    if not client_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Client not found")

    query = select(Deliverable).where(Deliverable.client_id == id)
    count_query = select(func.count(Deliverable.id)).where(Deliverable.client_id == id)

    if status:
        query = query.where(Deliverable.status == status)
        count_query = count_query.where(Deliverable.status == status)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    pages = max(1, (total + per_page - 1) // per_page)
    offset = (page - 1) * per_page

    query = query.order_by(Deliverable.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    deliverables = result.scalars().all()

    return {
        "items": [
            {
                "id": str(d.id),
                "title": d.title,
                "type": d.type,
                "status": d.status,
                "engine_engagement_id": str(d.engine_engagement_id) if d.engine_engagement_id else None,
                "created_at": d.created_at.isoformat() if d.created_at else None,
                "updated_at": d.updated_at.isoformat() if d.updated_at else None,
            }
            for d in deliverables
        ],
        "total": total,
        "page": page,
        "per_page": per_page,
        "pages": pages,
    }


@router.get("/{id}/engines")
async def get_client_engines(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get all engine engagements for a specific client."""
    # Verify client exists
    client_result = await db.execute(select(Client).where(Client.id == id))
    if not client_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Client not found")

    result = await db.execute(
        select(EngineEngagement)
        .where(EngineEngagement.client_id == id)
        .order_by(EngineEngagement.created_at.desc())
    )
    engagements = result.scalars().all()

    return {
        "client_id": str(id),
        "engines": [
            {
                "id": str(e.id),
                "engine_name": e.engine_name,
                "status": e.status,
                "scope": e.scope,
                "monthly_value": float(e.monthly_value) if e.monthly_value else None,
                "created_at": e.created_at.isoformat() if e.created_at else None,
                "updated_at": e.updated_at.isoformat() if e.updated_at else None,
            }
            for e in engagements
        ],
    }
