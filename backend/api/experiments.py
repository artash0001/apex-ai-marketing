"""
Apex AI Marketing - Experiments API

Track marketing experiments (A/B tests, channel tests, creative tests)
with hypothesis, results, and learnings for continuous optimization.
"""

import uuid
from datetime import datetime
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from fastapi.responses import StreamingResponse
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_
from sqlalchemy.ext.asyncio import AsyncSession

import csv
import io

from database import get_db
from models import Experiment, Client, EngineEngagement
from api.auth import get_current_user, UserInfo

router = APIRouter(prefix="/api/experiments", tags=["Experiments"])


# ── Pydantic Schemas ─────────────────────────────────────────────────

class ExperimentCreate(BaseModel):
    client_id: Optional[uuid.UUID] = None
    engine_engagement_id: Optional[uuid.UUID] = None
    name: str = Field(..., min_length=1, max_length=500)
    hypothesis: str = Field(..., min_length=1)
    description: Optional[str] = None
    experiment_type: str = Field(
        ...,
        description="ab_test, channel_test, creative_test, copy_test, audience_test, pricing_test",
    )
    status: str = "planned"
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metrics: Optional[dict] = Field(
        None,
        description="Key metrics to track for this experiment",
    )
    variant_a: Optional[dict] = None
    variant_b: Optional[dict] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class ExperimentUpdate(BaseModel):
    name: Optional[str] = None
    hypothesis: Optional[str] = None
    description: Optional[str] = None
    experiment_type: Optional[str] = None
    status: Optional[str] = None
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metrics: Optional[dict] = None
    variant_a: Optional[dict] = None
    variant_b: Optional[dict] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None

    model_config = {"from_attributes": True}


class ExperimentResponse(BaseModel):
    id: uuid.UUID
    client_id: Optional[uuid.UUID] = None
    engine_engagement_id: Optional[uuid.UUID] = None
    name: str
    hypothesis: str
    description: Optional[str] = None
    experiment_type: str
    status: str
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None
    metrics: Optional[dict] = None
    variant_a: Optional[dict] = None
    variant_b: Optional[dict] = None
    results: Optional[dict] = None
    winner: Optional[str] = None
    learnings: Optional[str] = None
    notes: Optional[str] = None
    metadata: Optional[dict] = None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class ExperimentListResponse(BaseModel):
    items: List[ExperimentResponse]
    total: int
    page: int
    per_page: int
    pages: int


class CompleteExperimentRequest(BaseModel):
    results: dict = Field(..., description="Experiment results data")
    winner: Optional[str] = Field(
        None,
        description="Winner: 'variant_a', 'variant_b', 'inconclusive', or 'neither'",
    )
    learnings: str = Field(..., min_length=1, description="Key learnings from the experiment")
    end_date: Optional[datetime] = None


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/", response_model=ExperimentListResponse)
async def list_experiments(
    client_id: Optional[uuid.UUID] = Query(None, description="Filter by client"),
    engine_engagement_id: Optional[uuid.UUID] = Query(None, description="Filter by engine engagement"),
    status: Optional[str] = Query(None, description="Filter by status (planned, running, completed, cancelled)"),
    experiment_type: Optional[str] = Query(None, description="Filter by experiment type"),
    search: Optional[str] = Query(None, description="Search by name or hypothesis"),
    page: int = Query(1, ge=1),
    per_page: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """List experiments with optional filters and pagination."""
    query = select(Experiment)
    count_query = select(func.count(Experiment.id))

    filters = []
    if client_id:
        filters.append(Experiment.client_id == client_id)
    if engine_engagement_id:
        filters.append(Experiment.engine_engagement_id == engine_engagement_id)
    if status:
        filters.append(Experiment.status == status)
    if experiment_type:
        filters.append(Experiment.experiment_type == experiment_type)
    if search:
        search_filter = f"%{search}%"
        filters.append(
            (Experiment.name.ilike(search_filter))
            | (Experiment.hypothesis.ilike(search_filter))
        )

    if filters:
        combined = and_(*filters)
        query = query.where(combined)
        count_query = count_query.where(combined)

    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0
    pages = max(1, (total + per_page - 1) // per_page)
    offset = (page - 1) * per_page

    query = query.order_by(Experiment.created_at.desc()).offset(offset).limit(per_page)
    result = await db.execute(query)
    experiments = result.scalars().all()

    return ExperimentListResponse(
        items=[ExperimentResponse.model_validate(e) for e in experiments],
        total=total,
        page=page,
        per_page=per_page,
        pages=pages,
    )


@router.get("/{id}", response_model=ExperimentResponse)
async def get_experiment(
    id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get experiment details."""
    result = await db.execute(select(Experiment).where(Experiment.id == id))
    experiment = result.scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")
    return ExperimentResponse.model_validate(experiment)


@router.post("/", response_model=ExperimentResponse, status_code=status.HTTP_201_CREATED)
async def create_experiment(
    payload: ExperimentCreate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Create a new experiment."""
    # Verify client if provided
    if payload.client_id:
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

    experiment = Experiment(
        id=uuid.uuid4(),
        **payload.model_dump(),
    )
    db.add(experiment)
    await db.flush()
    await db.refresh(experiment)
    return ExperimentResponse.model_validate(experiment)


@router.put("/{id}", response_model=ExperimentResponse)
async def update_experiment(
    id: uuid.UUID,
    payload: ExperimentUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Update an experiment."""
    result = await db.execute(select(Experiment).where(Experiment.id == id))
    experiment = result.scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    update_data = payload.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(experiment, field, value)
    experiment.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(experiment)
    return ExperimentResponse.model_validate(experiment)


@router.post("/{id}/complete", response_model=ExperimentResponse)
async def complete_experiment(
    id: uuid.UUID,
    payload: CompleteExperimentRequest,
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Mark an experiment as completed with results and learnings.

    Transitions status to 'completed' and records results, winner, and learnings.
    """
    result = await db.execute(select(Experiment).where(Experiment.id == id))
    experiment = result.scalar_one_or_none()
    if not experiment:
        raise HTTPException(status_code=404, detail="Experiment not found")

    if experiment.status == "completed":
        raise HTTPException(
            status_code=400,
            detail="Experiment is already completed",
        )
    if experiment.status == "cancelled":
        raise HTTPException(
            status_code=400,
            detail="Cannot complete a cancelled experiment",
        )

    experiment.status = "completed"
    experiment.results = payload.results
    experiment.winner = payload.winner
    experiment.learnings = payload.learnings
    experiment.end_date = payload.end_date or datetime.utcnow()
    experiment.updated_at = datetime.utcnow()

    await db.flush()
    await db.refresh(experiment)
    return ExperimentResponse.model_validate(experiment)


@router.get("/export/{client_id}")
async def export_experiments(
    client_id: uuid.UUID,
    format: str = Query("csv", description="Export format: csv or json"),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Export experiment log for a client.

    Returns all experiments for the client as CSV or JSON.
    """
    # Verify client
    client_result = await db.execute(
        select(Client).where(Client.id == client_id)
    )
    client = client_result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Get all experiments
    exp_result = await db.execute(
        select(Experiment)
        .where(Experiment.client_id == client_id)
        .order_by(Experiment.created_at.desc())
    )
    experiments = exp_result.scalars().all()

    if format == "csv":
        output = io.StringIO()
        writer = csv.writer(output)
        writer.writerow([
            "ID",
            "Name",
            "Hypothesis",
            "Type",
            "Status",
            "Winner",
            "Learnings",
            "Start Date",
            "End Date",
            "Created At",
        ])
        for e in experiments:
            writer.writerow([
                str(e.id),
                e.name,
                e.hypothesis,
                e.experiment_type,
                e.status,
                e.winner or "",
                e.learnings or "",
                e.start_date.isoformat() if e.start_date else "",
                e.end_date.isoformat() if e.end_date else "",
                e.created_at.isoformat() if e.created_at else "",
            ])

        output.seek(0)
        filename = f"experiments_{client.name.replace(' ', '_')}_{datetime.utcnow().strftime('%Y%m%d')}.csv"
        return StreamingResponse(
            iter([output.getvalue()]),
            media_type="text/csv",
            headers={"Content-Disposition": f"attachment; filename={filename}"},
        )

    # JSON format
    return {
        "client_id": str(client_id),
        "client_name": client.name,
        "exported_at": datetime.utcnow().isoformat(),
        "total_experiments": len(experiments),
        "experiments": [
            {
                "id": str(e.id),
                "name": e.name,
                "hypothesis": e.hypothesis,
                "experiment_type": e.experiment_type,
                "status": e.status,
                "results": e.results,
                "winner": e.winner,
                "learnings": e.learnings,
                "start_date": e.start_date.isoformat() if e.start_date else None,
                "end_date": e.end_date.isoformat() if e.end_date else None,
                "created_at": e.created_at.isoformat() if e.created_at else None,
            }
            for e in experiments
        ],
    }
