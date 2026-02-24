"""
Apex AI Marketing - Deliverables (Content) API

Full lifecycle management for deliverables: creation, AI generation,
quality gate review, approval, and rejection workflows.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Deliverable, EngineEngagement, Client, AIUsage, Task
from api.auth import get_current_user, UserInfo
from config import get_settings

settings = get_settings()

router = APIRouter(prefix="/api/deliverables", tags=["Deliverables"])


# ── Pydantic Schemas ─────────────────────────────────────────────────

class DeliverableCreate(BaseModel):
    client_id: uuid.UUID
    engine_engagement_id: Optional[uuid.UUID] = None
    title: str = Field(..., min_length=1, max_length=500)
    type: str = Field(
        ...,
        description="blog, landing_page, email, social_post, ad_copy, report, audit, video_script, etc.",
    )
    content: Optional[str] = None
    status: str = "draft"
    notes: Optional[str] = None
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class DeliverableUpdate(BaseModel):
    title: Optional[str] = None
    type: Optional[str] = None
    content: Optional[str] = None
    status: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class DeliverableResponse(BaseModel):
    id: uuid.UUID
    client_id: uuid.UUID
    engine_engagement_id: Optional[uuid.UUID] = None
    title: str
    type: str
    content: Optional[str] = None
    status: str
    notes: Optional[str] = None
    metadata: Optional[dict] = None
    reviewed_at: Optional[datetime] = None
    reviewed_by: Optional[str] = None
    feedback: Optional[str] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class DeliverableListResponse(BaseModel):
    items: List[DeliverableResponse]
    total: int
    page: int
    per_page: int
    pages: int


class ReviewRequest(BaseModel):
    notes: Optional[str] = None


class RejectRequest(BaseModel):
    feedback: str = Field(..., min_length=1, description="Rejection feedback / revision instructions")


class GenerateContentRequest(BaseModel):
    client_id: uuid.UUID
    engine_engagement_id: Optional[uuid.UUID] = None
    agent: str = Field(
        ...,
        description="AI agent to use: content_writer, seo_specialist, copywriter, email_marketer",
    )
    type: str = Field(
        ...,
        description="Content type: blog, landing_page, email, social_post, ad_copy, etc.",
    )
    title: Optional[str] = None
    context: Optional[str] = Field(
        None,
        description="Additional context, keywords, or brief for the AI agent",
    )
    language: str = "en"
    tone: Optional[str] = None
    target_audience: Optional[str] = None
    word_count: Optional[int] = None


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/", response_model=DeliverableListResponse)
async def list_deliverables(
    status: Optional[str] = Query(None, description="Filter by status (draft, in_review, approved, rejected, published)"),
    type: Optional[str] = Query(None, description="Filter by deliverable type"),
    client_id: Optional[uuid.UUID] = Query(None, description="Filter by client"),
    engine_engagement_id: Optional[uuid.UUID] = Query(None, description="Filter by engine engagement"),
    search: Optional[str] = Query(None, description="Search by title"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """List deliverables with optional filters and pagination."""
    query = select(Deliverable)
    count_query = select(func.count(Deliverable.id))

    filters = []
    if status:
        filters.append(Deliverable.status == status)
    if type:
        filters.append(Deliverable.type == type)
    if client_id:
        filters.append(Deliverable.client_id == client_id)
    if engine_engagement_id:
        filters.append(Deliverable.engine_engagement_id == engine_engagement_id)
    if search:
        filters.append(Deliverable.title.ilike(f"%{search}%"))

    if filters:
        combined = and_(*filters)
        query = query.where(combined)
        count_query = count_query.where(combined)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    pages = max(1, (total + per_page - 1) // per_page)
    offset = (page - 1) * per_page

    query = query.order_by(Deliverable.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    deliverables = result.scalars().all()

    return DeliverableListResponse(
        items=[DeliverableResponse.model_validate(d) for d in deliverables],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get("/{id}", response_model=DeliverableResponse)
async def get_deliverable(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get deliverable details."""
    result = await db.execute(select(Deliverable).where(Deliverable.id == id))
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")
    return DeliverableResponse.model_validate(deliverable)


@router.post("/", response_model=DeliverableResponse, status_code=status.HTTP_201_CREATED)
async def create_deliverable(
    payload: DeliverableCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create a deliverable manually."""
    # Verify client exists
    client_result = await db.execute(
        select(Client).where(Client.id == payload.client_id)
    )
    if not client_result.scalar_one_or_none():
        raise HTTPException(status_code=404, detail="Client not found")

    # Verify engine engagement if provided
    if payload.engine_engagement_id:
        eng_result = await db.execute(
            select(EngineEngagement).where(
                EngineEngagement.id == payload.engine_engagement_id
            )
        )
        if not eng_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Engine engagement not found")

    deliverable = Deliverable(
        id=uuid.uuid4(),
        **payload.model_dump(),
    )
    db.add(deliverable)
    await db.flush()
    await db.refresh(deliverable)
    return DeliverableResponse.model_validate(deliverable)


@router.put("/{id}", response_model=DeliverableResponse)
async def update_deliverable(
    id: uuid.UUID,
    payload: DeliverableUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Update a deliverable (content, status, metadata)."""
    result = await db.execute(select(Deliverable).where(Deliverable.id == id))
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(deliverable, field, value)
    deliverable.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(deliverable)
    return DeliverableResponse.model_validate(deliverable)


@router.post("/{id}/review", response_model=DeliverableResponse)
async def submit_for_review(
    id: uuid.UUID,
    payload: ReviewRequest = ReviewRequest(),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Submit a deliverable for quality gate review.

    Transitions status from 'draft' to 'in_review'.
    """
    result = await db.execute(select(Deliverable).where(Deliverable.id == id))
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    if deliverable.status not in ("draft", "rejected"):
        raise HTTPException(
            status_code=400,
            detail=f"Cannot submit for review: deliverable is currently '{deliverable.status}'",
        )

    deliverable.status = "in_review"
    deliverable.reviewed_at = None
    deliverable.reviewed_by = None
    deliverable.feedback = None
    if payload.notes:
        deliverable.notes = payload.notes
    deliverable.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(deliverable)
    return DeliverableResponse.model_validate(deliverable)


@router.post("/{id}/approve", response_model=DeliverableResponse)
async def approve_deliverable(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Approve a deliverable that is in review.

    Transitions status from 'in_review' to 'approved'.
    """
    result = await db.execute(select(Deliverable).where(Deliverable.id == id))
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    if deliverable.status != "in_review":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot approve: deliverable is currently '{deliverable.status}', must be 'in_review'",
        )

    deliverable.status = "approved"
    deliverable.reviewed_at = datetime.utcnow()
    deliverable.reviewed_by = current_user.username
    deliverable.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(deliverable)
    return DeliverableResponse.model_validate(deliverable)


@router.post("/{id}/reject", response_model=DeliverableResponse)
async def reject_deliverable(
    id: uuid.UUID,
    payload: RejectRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Reject a deliverable with feedback for revision.

    Transitions status from 'in_review' to 'rejected'.
    """
    result = await db.execute(select(Deliverable).where(Deliverable.id == id))
    deliverable = result.scalar_one_or_none()
    if not deliverable:
        raise HTTPException(status_code=404, detail="Deliverable not found")

    if deliverable.status != "in_review":
        raise HTTPException(
            status_code=400,
            detail=f"Cannot reject: deliverable is currently '{deliverable.status}', must be 'in_review'",
        )

    deliverable.status = "rejected"
    deliverable.feedback = payload.feedback
    deliverable.reviewed_at = datetime.utcnow()
    deliverable.reviewed_by = current_user.username
    deliverable.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(deliverable)
    return DeliverableResponse.model_validate(deliverable)


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate_content(
    payload: GenerateContentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Generate content using an AI agent.

    Creates a deliverable with AI-generated content and logs AI usage.
    The actual AI generation would be handled by the agent system;
    this endpoint creates the task and placeholder deliverable.
    """
    # Verify client exists
    client_result = await db.execute(
        select(Client).where(Client.id == payload.client_id)
    )
    client = client_result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Verify engine engagement if provided
    if payload.engine_engagement_id:
        eng_result = await db.execute(
            select(EngineEngagement).where(
                EngineEngagement.id == payload.engine_engagement_id
            )
        )
        if not eng_result.scalar_one_or_none():
            raise HTTPException(status_code=404, detail="Engine engagement not found")

    # Determine title
    title = payload.title or f"AI Generated {payload.type.replace('_', ' ').title()}"

    # Create deliverable placeholder (status: generating)
    deliverable = Deliverable(
        id=uuid.uuid4(),
        client_id=payload.client_id,
        engine_engagement_id=payload.engine_engagement_id,
        title=title,
        type=payload.type,
        content=None,  # Will be populated by AI agent
        status="generating",
        notes=f"Agent: {payload.agent} | Language: {payload.language}",
        metadata={
            "agent": payload.agent,
            "context": payload.context,
            "language": payload.language,
            "tone": payload.tone,
            "target_audience": payload.target_audience,
            "word_count": payload.word_count,
        },
    )
    db.add(deliverable)

    # Create task for the AI agent
    task = Task(
        id=uuid.uuid4(),
        client_id=payload.client_id,
        title=f"Generate {payload.type}: {title}",
        description=(
            f"Use {payload.agent} agent to generate {payload.type} content. "
            f"Context: {payload.context or 'No additional context'}. "
            f"Language: {payload.language}. "
            f"Tone: {payload.tone or 'Default'}. "
            f"Target audience: {payload.target_audience or 'General'}. "
            f"Word count: {payload.word_count or 'Standard'}."
        ),
        task_type="content_generation",
        assigned_agent=payload.agent,
        status="pending",
        metadata={"deliverable_id": str(deliverable.id)},
    )
    db.add(task)

    # Log AI usage (initial request)
    ai_usage = AIUsage(
        agent_name=payload.agent,
        client_id=payload.client_id,
        action=f"generate_{payload.type}",
        model=settings.DEFAULT_MODEL,
        input_tokens=0,
        output_tokens=0,
        cost=0.0,
        metadata={
            "deliverable_id": str(deliverable.id),
            "task_id": str(task.id),
            "status": "queued",
        },
    )
    db.add(ai_usage)

    await db.flush()
    await db.refresh(deliverable)

    return {
        "deliverable_id": str(deliverable.id),
        "task_id": str(task.id),
        "status": "generating",
        "agent": payload.agent,
        "type": payload.type,
        "title": title,
        "message": f"Content generation queued. Agent '{payload.agent}' will process this task.",
    }
