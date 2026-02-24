"""
Apex AI Marketing - Outreach API

Campaign management, outreach templates, sequence tracking,
and AI-powered batch generation for multi-channel outreach.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import Lead, Task, AIUsage
from api.auth import get_current_user, UserInfo
from config import get_settings

settings = get_settings()

router = APIRouter(prefix="/api/outreach", tags=["Outreach"])


# ── Pydantic Schemas ─────────────────────────────────────────────────

class CampaignCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    market: str = Field(..., description="dubai, uk, global, russian_dubai")
    language: str = "en"
    channel: str = Field(..., description="linkedin, email, whatsapp, instagram, cold_call")
    icp_criteria: Optional[dict] = Field(
        None,
        description="Ideal Customer Profile criteria for targeting",
    )
    template_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    status: str = "draft"
    scheduled_at: Optional[datetime] = None
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class CampaignResponse(BaseModel):
    id: uuid.UUID
    name: str
    market: str
    language: str
    channel: str
    icp_criteria: Optional[dict] = None
    template_id: Optional[uuid.UUID] = None
    description: Optional[str] = None
    status: str
    scheduled_at: Optional[datetime] = None
    sent_count: int = 0
    reply_count: int = 0
    metadata: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class TemplateCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    channel: str = Field(..., description="linkedin, email, whatsapp, instagram")
    language: str = "en"
    subject: Optional[str] = None
    body: str = Field(..., min_length=1)
    sequence_step: int = Field(0, ge=0, description="Which step in the outreach sequence this template is for")
    variables: Optional[List[str]] = Field(
        None,
        description="Template variables e.g. ['name', 'company', 'pain_point']",
    )
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class TemplateResponse(BaseModel):
    id: uuid.UUID
    name: str
    channel: str
    language: str
    subject: Optional[str] = None
    body: str
    sequence_step: int
    variables: Optional[List[str]] = None
    metadata: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class SequenceStatus(BaseModel):
    lead_id: uuid.UUID
    lead_name: str
    company: Optional[str] = None
    outreach_status: str
    sequence_step: int
    channel: Optional[str] = None
    last_activity: Optional[datetime] = None


class BatchGenerateRequest(BaseModel):
    market: str = Field(..., description="Target market for batch")
    language: str = "en"
    channel: str = Field(..., description="Outreach channel")
    count: int = Field(10, ge=1, le=100, description="Number of messages to generate")
    template_id: Optional[uuid.UUID] = None
    agent: str = Field(
        "outreach_specialist",
        description="AI agent to use for generation",
    )
    tone: Optional[str] = None
    custom_instructions: Optional[str] = None


# ── In-memory campaign/template storage ──────────────────────────────
# NOTE: In production, these would be database models. For now we store
# them as Task records with specific task_types to leverage the existing
# data model. A dedicated Campaign and Template table is recommended
# for a production deployment.


# ── Endpoints: Campaigns ─────────────────────────────────────────────

@router.get("/campaigns", response_model=List[CampaignResponse])
async def list_campaigns(
    status: Optional[str] = Query(None, description="Filter by campaign status"),
    market: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """List outreach campaigns.

    Campaigns are stored as Task records with task_type='outreach_campaign'.
    """
    query = select(Task).where(Task.task_type == "outreach_campaign")

    if status:
        query = query.where(Task.status == status)

    query = query.order_by(Task.created_at.desc())
    offset = (page - 1) * per_page
    query = query.offset(offset).limit(per_page)

    result = await db.execute(query)
    tasks = result.scalars().all()

    campaigns = []
    for t in tasks:
        meta = t.metadata or {}
        campaigns.append(
            CampaignResponse(
                id=t.id,
                name=t.title,
                market=meta.get("market", ""),
                language=meta.get("language", "en"),
                channel=meta.get("channel", ""),
                icp_criteria=meta.get("icp_criteria"),
                template_id=meta.get("template_id"),
                description=t.description,
                status=t.status,
                scheduled_at=meta.get("scheduled_at"),
                sent_count=meta.get("sent_count", 0),
                reply_count=meta.get("reply_count", 0),
                metadata=meta,
                created_at=t.created_at,
                updated_at=t.updated_at or t.created_at,
            )
        )

    return campaigns


@router.post("/campaigns", response_model=CampaignResponse, status_code=status.HTTP_201_CREATED)
async def create_campaign(
    payload: CampaignCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create a new outreach campaign.

    Stores as a Task record with task_type='outreach_campaign'.
    """
    campaign_id = uuid.uuid4()
    meta = {
        "market": payload.market,
        "language": payload.language,
        "channel": payload.channel,
        "icp_criteria": payload.icp_criteria,
        "template_id": str(payload.template_id) if payload.template_id else None,
        "scheduled_at": payload.scheduled_at.isoformat() if payload.scheduled_at else None,
        "sent_count": 0,
        "reply_count": 0,
    }
    if payload.metadata:
        meta.update(payload.metadata)

    task = Task(
        id=campaign_id,
        title=payload.name,
        description=payload.description,
        task_type="outreach_campaign",
        assigned_agent="outreach_specialist",
        status=payload.status,
        metadata=meta,
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)

    return CampaignResponse(
        id=task.id,
        name=task.title,
        market=payload.market,
        language=payload.language,
        channel=payload.channel,
        icp_criteria=payload.icp_criteria,
        template_id=payload.template_id,
        description=task.description,
        status=task.status,
        scheduled_at=payload.scheduled_at,
        sent_count=0,
        reply_count=0,
        metadata=meta,
        created_at=task.created_at,
        updated_at=task.updated_at or task.created_at,
    )


@router.post("/campaigns/{id}/send")
async def send_campaign(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Trigger sending for a campaign.

    Finds matching leads based on campaign criteria and queues
    outreach messages for each.
    """
    result = await db.execute(
        select(Task).where(
            and_(Task.id == id, Task.task_type == "outreach_campaign")
        )
    )
    campaign_task = result.scalar_one_or_none()
    if not campaign_task:
        raise HTTPException(status_code=404, detail="Campaign not found")

    if campaign_task.status == "sending":
        raise HTTPException(status_code=400, detail="Campaign is already being sent")
    if campaign_task.status == "completed":
        raise HTTPException(status_code=400, detail="Campaign has already been sent")

    meta = campaign_task.metadata or {}
    market = meta.get("market")
    channel = meta.get("channel")
    language = meta.get("language", "en")

    # Find matching leads
    lead_query = select(Lead).where(
        Lead.outreach_status.in_(["new", "researched", "message_drafted"])
    )
    if market:
        lead_query = lead_query.where(Lead.market == market)
    if channel:
        lead_query = lead_query.where(Lead.channel == channel)
    if language:
        lead_query = lead_query.where(Lead.language == language)

    lead_result = await db.execute(lead_query)
    matching_leads = lead_result.scalars().all()

    # Update campaign status
    campaign_task.status = "sending"
    meta["sent_count"] = len(matching_leads)
    meta["send_triggered_at"] = datetime.utcnow().isoformat()
    meta["send_triggered_by"] = current_user.username
    campaign_task.metadata = meta

    # Create individual send tasks for each lead
    send_tasks = []
    for lead in matching_leads:
        send_task = Task(
            id=uuid.uuid4(),
            title=f"Send outreach: {lead.name}",
            description=f"Send {channel} outreach to {lead.name} ({lead.company or 'N/A'})",
            task_type="outreach_send",
            assigned_agent="outreach_specialist",
            status="pending",
            metadata={
                "campaign_id": str(id),
                "lead_id": str(lead.id),
                "channel": channel,
                "market": market,
            },
        )
        db.add(send_task)
        send_tasks.append(str(send_task.id))

    await db.flush()

    return {
        "campaign_id": str(id),
        "status": "sending",
        "matching_leads": len(matching_leads),
        "send_tasks_created": len(send_tasks),
        "message": f"Campaign queued for sending to {len(matching_leads)} leads",
    }


# ── Endpoints: Templates ────────────────────────────────────────────

@router.get("/templates", response_model=List[TemplateResponse])
async def list_templates(
    channel: Optional[str] = Query(None),
    language: Optional[str] = Query(None),
    sequence_step: Optional[int] = Query(None, ge=0),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """List outreach templates.

    Templates are stored as Task records with task_type='outreach_template'.
    """
    query = select(Task).where(Task.task_type == "outreach_template")
    query = query.order_by(Task.created_at.desc())

    result = await db.execute(query)
    tasks = result.scalars().all()

    templates = []
    for t in tasks:
        meta = t.metadata or {}
        t_channel = meta.get("channel", "")
        t_language = meta.get("language", "en")
        t_step = meta.get("sequence_step", 0)

        # Apply filters in Python (since metadata is JSONB)
        if channel and t_channel != channel:
            continue
        if language and t_language != language:
            continue
        if sequence_step is not None and t_step != sequence_step:
            continue

        templates.append(
            TemplateResponse(
                id=t.id,
                name=t.title,
                channel=t_channel,
                language=t_language,
                subject=meta.get("subject"),
                body=t.description or "",
                sequence_step=t_step,
                variables=meta.get("variables"),
                metadata=meta,
                created_at=t.created_at,
                updated_at=t.updated_at or t.created_at,
            )
        )

    return templates


@router.post("/templates", response_model=TemplateResponse, status_code=status.HTTP_201_CREATED)
async def create_template(
    payload: TemplateCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create an outreach template."""
    template_id = uuid.uuid4()
    meta = {
        "channel": payload.channel,
        "language": payload.language,
        "subject": payload.subject,
        "sequence_step": payload.sequence_step,
        "variables": payload.variables,
    }
    if payload.metadata:
        meta.update(payload.metadata)

    task = Task(
        id=template_id,
        title=payload.name,
        description=payload.body,
        task_type="outreach_template",
        assigned_agent="outreach_specialist",
        status="active",
        metadata=meta,
    )
    db.add(task)
    await db.flush()
    await db.refresh(task)

    return TemplateResponse(
        id=task.id,
        name=task.title,
        channel=payload.channel,
        language=payload.language,
        subject=payload.subject,
        body=payload.body,
        sequence_step=payload.sequence_step,
        variables=payload.variables,
        metadata=meta,
        created_at=task.created_at,
        updated_at=task.updated_at or task.created_at,
    )


# ── Endpoints: Sequences ────────────────────────────────────────────

@router.get("/sequences", response_model=List[SequenceStatus])
async def get_sequences(
    market: Optional[str] = Query(None),
    channel: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    per_page: int = Query(50, ge=1, le=200),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get sequence status for all active leads.

    Returns leads that are currently in an outreach sequence
    (not 'new' and not terminal statuses).
    """
    active_statuses = [
        "researched",
        "message_drafted",
        "sent",
        "follow_up_1",
        "follow_up_2",
        "follow_up_3",
    ]

    query = select(Lead).where(Lead.outreach_status.in_(active_statuses))

    if market:
        query = query.where(Lead.market == market)
    if channel:
        query = query.where(Lead.channel == channel)

    offset = (page - 1) * per_page
    query = query.order_by(Lead.updated_at.desc()).offset(offset).limit(per_page)

    result = await db.execute(query)
    leads = result.scalars().all()

    return [
        SequenceStatus(
            lead_id=l.id,
            lead_name=l.name,
            company=l.company,
            outreach_status=l.outreach_status,
            sequence_step=l.sequence_step,
            channel=l.channel,
            last_activity=l.updated_at,
        )
        for l in leads
    ]


# ── Endpoints: AI Batch Generation ──────────────────────────────────

@router.post("/generate-batch", status_code=status.HTTP_201_CREATED)
async def generate_outreach_batch(
    payload: BatchGenerateRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Generate a new outreach batch using AI.

    Creates tasks for the AI agent to generate personalized
    outreach messages for leads matching the criteria.
    """
    # Find leads matching the criteria that need messages
    lead_query = select(Lead).where(
        and_(
            Lead.market == payload.market,
            Lead.language == payload.language,
            Lead.outreach_status.in_(["new", "researched"]),
        )
    )
    if payload.channel:
        lead_query = lead_query.where(Lead.channel == payload.channel)

    lead_query = lead_query.limit(payload.count)
    lead_result = await db.execute(lead_query)
    leads = lead_result.scalars().all()

    if not leads:
        raise HTTPException(
            status_code=404,
            detail="No matching leads found for the given criteria",
        )

    # Create a batch task
    batch_id = uuid.uuid4()
    batch_task = Task(
        id=batch_id,
        title=f"Outreach Batch: {payload.market}/{payload.channel} ({len(leads)} leads)",
        description=(
            f"Generate {payload.channel} outreach messages for {len(leads)} leads "
            f"in {payload.market} market. Language: {payload.language}. "
            f"Custom instructions: {payload.custom_instructions or 'None'}"
        ),
        task_type="outreach_batch",
        assigned_agent=payload.agent,
        status="pending",
        metadata={
            "market": payload.market,
            "language": payload.language,
            "channel": payload.channel,
            "lead_count": len(leads),
            "lead_ids": [str(l.id) for l in leads],
            "template_id": str(payload.template_id) if payload.template_id else None,
            "tone": payload.tone,
            "custom_instructions": payload.custom_instructions,
        },
    )
    db.add(batch_task)

    # Log AI usage
    ai_usage = AIUsage(
        agent_name=payload.agent,
        action="generate_outreach_batch",
        model=settings.DEFAULT_MODEL,
        input_tokens=0,
        output_tokens=0,
        cost=0.0,
        metadata={
            "batch_task_id": str(batch_id),
            "lead_count": len(leads),
            "status": "queued",
        },
    )
    db.add(ai_usage)

    await db.flush()

    return {
        "batch_id": str(batch_id),
        "status": "pending",
        "agent": payload.agent,
        "matching_leads": len(leads),
        "market": payload.market,
        "channel": payload.channel,
        "language": payload.language,
        "message": (
            f"Batch generation queued for {len(leads)} leads. "
            f"Agent '{payload.agent}' will generate personalized messages."
        ),
    }
