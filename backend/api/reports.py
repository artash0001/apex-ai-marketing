"""
Apex AI Marketing - Reports API

Dashboard metrics, client report generation, AI cost tracking,
and revenue analytics.
"""

import uuid
from datetime import datetime, date, timedelta
from decimal import Decimal
from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pydantic import BaseModel, Field
from sqlalchemy import select, func, and_, extract, cast, Date
from sqlalchemy.ext.asyncio import AsyncSession

from database import get_db
from models import (
    Client,
    EngineEngagement,
    Deliverable,
    Lead,
    AIUsage,
    Invoice,
    Task,
)
from api.auth import get_current_user, UserInfo
from config import get_settings

settings = get_settings()

router = APIRouter(prefix="/api/reports", tags=["Reports"])


# ── Pydantic Schemas ─────────────────────────────────────────────────

class DashboardMetrics(BaseModel):
    active_clients: int
    total_clients: int
    mrr: float
    pipeline_counts: dict
    ai_costs_this_month: float
    ai_costs_total: float
    outreach_stats: dict
    deliverables_stats: dict
    recent_activity: List[dict]


class ReportGenerateRequest(BaseModel):
    report_type: str = Field("weekly", description="weekly or monthly")
    start_date: Optional[date] = None
    end_date: Optional[date] = None
    include_deliverables: bool = True
    include_experiments: bool = True
    include_ai_usage: bool = True


class AICostBreakdown(BaseModel):
    total_cost: float
    by_agent: dict
    by_client: dict
    by_date: List[dict]
    total_input_tokens: int
    total_output_tokens: int


class RevenueData(BaseModel):
    current_mrr: float
    mrr_trend: List[dict]
    by_engine_type: dict
    total_clients_by_status: dict
    average_client_value: float


# ── Endpoints ────────────────────────────────────────────────────────

@router.get("/dashboard", response_model=DashboardMetrics)
async def get_dashboard(
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get admin dashboard metrics.

    Returns a comprehensive snapshot of the business including:
    active clients, MRR, pipeline counts, AI costs, and outreach stats.
    """
    now = datetime.utcnow()
    first_of_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # ── Active clients ────────────────────────────────────────────
    active_result = await db.execute(
        select(func.count(Client.id)).where(Client.status == "active")
    )
    active_clients = active_result.scalar() or 0

    total_result = await db.execute(select(func.count(Client.id)))
    total_clients = total_result.scalar() or 0

    # ── MRR (Monthly Recurring Revenue) ───────────────────────────
    mrr_result = await db.execute(
        select(func.coalesce(func.sum(Client.monthly_value), 0)).where(
            Client.status == "active"
        )
    )
    mrr = float(mrr_result.scalar() or 0)

    # ── Pipeline counts (engine engagements by status) ────────────
    pipeline_result = await db.execute(
        select(EngineEngagement.status, func.count(EngineEngagement.id)).group_by(
            EngineEngagement.status
        )
    )
    pipeline_counts = {row[0]: row[1] for row in pipeline_result.all()}

    # ── AI costs ──────────────────────────────────────────────────
    ai_cost_month_result = await db.execute(
        select(func.coalesce(func.sum(AIUsage.cost), 0)).where(
            AIUsage.created_at >= first_of_month
        )
    )
    ai_costs_this_month = float(ai_cost_month_result.scalar() or 0)

    ai_cost_total_result = await db.execute(
        select(func.coalesce(func.sum(AIUsage.cost), 0))
    )
    ai_costs_total = float(ai_cost_total_result.scalar() or 0)

    # ── Outreach stats ────────────────────────────────────────────
    outreach_result = await db.execute(
        select(Lead.outreach_status, func.count(Lead.id)).group_by(
            Lead.outreach_status
        )
    )
    outreach_stats = {row[0]: row[1] for row in outreach_result.all()}

    total_leads_result = await db.execute(select(func.count(Lead.id)))
    outreach_stats["total_leads"] = total_leads_result.scalar() or 0

    # ── Deliverables stats ────────────────────────────────────────
    del_result = await db.execute(
        select(Deliverable.status, func.count(Deliverable.id)).group_by(
            Deliverable.status
        )
    )
    deliverables_stats = {row[0]: row[1] for row in del_result.all()}

    total_del_result = await db.execute(select(func.count(Deliverable.id)))
    deliverables_stats["total"] = total_del_result.scalar() or 0

    # ── Recent activity (last 10 tasks) ───────────────────────────
    recent_tasks_result = await db.execute(
        select(Task)
        .order_by(Task.created_at.desc())
        .limit(10)
    )
    recent_tasks = recent_tasks_result.scalars().all()
    recent_activity = [
        {
            "id": str(t.id),
            "title": t.title,
            "type": t.task_type,
            "status": t.status,
            "agent": t.assigned_agent,
            "created_at": t.created_at.isoformat() if t.created_at else None,
        }
        for t in recent_tasks
    ]

    return DashboardMetrics(
        active_clients=active_clients,
        total_clients=total_clients,
        mrr=mrr,
        pipeline_counts=pipeline_counts,
        ai_costs_this_month=round(ai_costs_this_month, 2),
        ai_costs_total=round(ai_costs_total, 2),
        outreach_stats=outreach_stats,
        deliverables_stats=deliverables_stats,
        recent_activity=recent_activity,
    )


@router.post("/generate/{client_id}")
async def generate_report(
    client_id: uuid.UUID,
    payload: ReportGenerateRequest = ReportGenerateRequest(),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Generate a weekly or monthly report for a client.

    Compiles deliverables, experiments, AI usage, and engagement
    metrics into a structured report.
    """
    # Verify client
    client_result = await db.execute(
        select(Client).where(Client.id == client_id)
    )
    client = client_result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=404, detail="Client not found")

    # Determine date range
    now = datetime.utcnow()
    if payload.start_date and payload.end_date:
        start = datetime.combine(payload.start_date, datetime.min.time())
        end = datetime.combine(payload.end_date, datetime.max.time())
    elif payload.report_type == "weekly":
        start = now - timedelta(days=7)
        end = now
    else:  # monthly
        start = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        end = now

    report = {
        "client_id": str(client_id),
        "client_name": client.name,
        "company": client.company,
        "report_type": payload.report_type,
        "period": {
            "start": start.isoformat(),
            "end": end.isoformat(),
        },
        "generated_at": now.isoformat(),
        "generated_by": current_user.username,
    }

    # ── Engine engagements summary ────────────────────────────────
    eng_result = await db.execute(
        select(EngineEngagement).where(EngineEngagement.client_id == client_id)
    )
    engagements = eng_result.scalars().all()
    report["engine_engagements"] = [
        {
            "id": str(e.id),
            "engine_name": e.engine_name,
            "status": e.status,
            "monthly_value": float(e.monthly_value) if e.monthly_value else None,
        }
        for e in engagements
    ]

    # ── Deliverables in period ────────────────────────────────────
    if payload.include_deliverables:
        del_result = await db.execute(
            select(Deliverable).where(
                and_(
                    Deliverable.client_id == client_id,
                    Deliverable.created_at >= start,
                    Deliverable.created_at <= end,
                )
            )
        )
        deliverables = del_result.scalars().all()
        report["deliverables"] = {
            "count": len(deliverables),
            "by_status": {},
            "items": [
                {
                    "id": str(d.id),
                    "title": d.title,
                    "type": d.type,
                    "status": d.status,
                    "created_at": d.created_at.isoformat() if d.created_at else None,
                }
                for d in deliverables
            ],
        }
        for d in deliverables:
            report["deliverables"]["by_status"][d.status] = (
                report["deliverables"]["by_status"].get(d.status, 0) + 1
            )

    # ── AI usage in period ────────────────────────────────────────
    if payload.include_ai_usage:
        ai_result = await db.execute(
            select(AIUsage).where(
                and_(
                    AIUsage.client_id == client_id,
                    AIUsage.created_at >= start,
                    AIUsage.created_at <= end,
                )
            )
        )
        ai_records = ai_result.scalars().all()
        total_cost = sum(float(a.cost or 0) for a in ai_records)
        total_input = sum(a.input_tokens or 0 for a in ai_records)
        total_output = sum(a.output_tokens or 0 for a in ai_records)
        report["ai_usage"] = {
            "total_cost": round(total_cost, 4),
            "total_input_tokens": total_input,
            "total_output_tokens": total_output,
            "request_count": len(ai_records),
            "by_agent": {},
        }
        for a in ai_records:
            agent = a.agent_name or "unknown"
            if agent not in report["ai_usage"]["by_agent"]:
                report["ai_usage"]["by_agent"][agent] = {
                    "cost": 0.0,
                    "requests": 0,
                }
            report["ai_usage"]["by_agent"][agent]["cost"] += float(a.cost or 0)
            report["ai_usage"]["by_agent"][agent]["requests"] += 1

    # Create a task to generate the full formatted report
    task = Task(
        id=uuid.uuid4(),
        client_id=client_id,
        title=f"{payload.report_type.title()} Report: {client.name}",
        description=f"Generate {payload.report_type} report for period {start.date()} to {end.date()}",
        task_type="report_generation",
        assigned_agent="report_generator",
        status="completed",
        metadata={"report_data": report},
    )
    db.add(task)
    await db.flush()

    report["task_id"] = str(task.id)
    return report


@router.get("/ai-costs", response_model=AICostBreakdown)
async def get_ai_costs(
    start_date: Optional[date] = Query(None, description="Start date for the range"),
    end_date: Optional[date] = Query(None, description="End date for the range"),
    agent_name: Optional[str] = Query(None, description="Filter by AI agent"),
    client_id: Optional[uuid.UUID] = Query(None, description="Filter by client"),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get AI cost breakdown by agent, client, and date range."""
    filters = []
    if start_date:
        filters.append(AIUsage.created_at >= datetime.combine(start_date, datetime.min.time()))
    if end_date:
        filters.append(AIUsage.created_at <= datetime.combine(end_date, datetime.max.time()))
    if agent_name:
        filters.append(AIUsage.agent_name == agent_name)
    if client_id:
        filters.append(AIUsage.client_id == client_id)

    base_where = and_(*filters) if filters else True

    # Total cost
    total_result = await db.execute(
        select(func.coalesce(func.sum(AIUsage.cost), 0)).where(base_where)
    )
    total_cost = float(total_result.scalar() or 0)

    # Total tokens
    tokens_result = await db.execute(
        select(
            func.coalesce(func.sum(AIUsage.input_tokens), 0),
            func.coalesce(func.sum(AIUsage.output_tokens), 0),
        ).where(base_where)
    )
    tokens_row = tokens_result.one()
    total_input_tokens = int(tokens_row[0])
    total_output_tokens = int(tokens_row[1])

    # By agent
    agent_result = await db.execute(
        select(
            AIUsage.agent_name,
            func.sum(AIUsage.cost),
            func.count(AIUsage.id),
            func.sum(AIUsage.input_tokens),
            func.sum(AIUsage.output_tokens),
        )
        .where(base_where)
        .group_by(AIUsage.agent_name)
    )
    by_agent = {
        (row[0] or "unknown"): {
            "cost": round(float(row[1] or 0), 4),
            "requests": row[2],
            "input_tokens": int(row[3] or 0),
            "output_tokens": int(row[4] or 0),
        }
        for row in agent_result.all()
    }

    # By client
    client_result = await db.execute(
        select(
            AIUsage.client_id,
            func.sum(AIUsage.cost),
            func.count(AIUsage.id),
        )
        .where(base_where)
        .group_by(AIUsage.client_id)
    )
    by_client_raw = client_result.all()

    # Resolve client names
    by_client = {}
    for row in by_client_raw:
        client_id_val = row[0]
        if client_id_val:
            name_result = await db.execute(
                select(Client.name).where(Client.id == client_id_val)
            )
            name = name_result.scalar_one_or_none() or "Unknown"
        else:
            name = "No Client"
        by_client[name] = {
            "client_id": str(client_id_val) if client_id_val else None,
            "cost": round(float(row[1] or 0), 4),
            "requests": row[2],
        }

    # By date (daily aggregation)
    date_result = await db.execute(
        select(
            cast(AIUsage.created_at, Date),
            func.sum(AIUsage.cost),
            func.count(AIUsage.id),
        )
        .where(base_where)
        .group_by(cast(AIUsage.created_at, Date))
        .order_by(cast(AIUsage.created_at, Date))
    )
    by_date = [
        {
            "date": row[0].isoformat() if row[0] else None,
            "cost": round(float(row[1] or 0), 4),
            "requests": row[2],
        }
        for row in date_result.all()
    ]

    return AICostBreakdown(
        total_cost=round(total_cost, 4),
        by_agent=by_agent,
        by_client=by_client,
        by_date=by_date,
        total_input_tokens=total_input_tokens,
        total_output_tokens=total_output_tokens,
    )


@router.get("/revenue", response_model=RevenueData)
async def get_revenue(
    months: int = Query(6, ge=1, le=24, description="Number of months for MRR trend"),
    db: AsyncSession = Depends(get_db),
    current_user: UserInfo = Depends(get_current_user),
):
    """Get revenue tracking data including MRR trend and breakdown by engine type."""
    # Current MRR
    mrr_result = await db.execute(
        select(func.coalesce(func.sum(Client.monthly_value), 0)).where(
            Client.status == "active"
        )
    )
    current_mrr = float(mrr_result.scalar() or 0)

    # Average client value
    avg_result = await db.execute(
        select(func.coalesce(func.avg(Client.monthly_value), 0)).where(
            Client.status == "active"
        )
    )
    average_client_value = float(avg_result.scalar() or 0)

    # Revenue by engine type
    engine_rev_result = await db.execute(
        select(
            EngineEngagement.engine_name,
            func.sum(EngineEngagement.monthly_value),
            func.count(EngineEngagement.id),
        )
        .where(EngineEngagement.status == "active")
        .group_by(EngineEngagement.engine_name)
    )
    by_engine_type = {
        row[0]: {
            "monthly_value": round(float(row[1] or 0), 2),
            "engagement_count": row[2],
        }
        for row in engine_rev_result.all()
    }

    # Clients by status
    status_result = await db.execute(
        select(Client.status, func.count(Client.id)).group_by(Client.status)
    )
    total_clients_by_status = {row[0]: row[1] for row in status_result.all()}

    # MRR trend (from invoices if available, otherwise synthetic from engagements)
    mrr_trend = []
    now = datetime.utcnow()
    for i in range(months - 1, -1, -1):
        month_date = now - timedelta(days=30 * i)
        month_start = month_date.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        if month_start.month == 12:
            month_end = month_start.replace(year=month_start.year + 1, month=1)
        else:
            month_end = month_start.replace(month=month_start.month + 1)

        # Try invoices first
        inv_result = await db.execute(
            select(func.coalesce(func.sum(Invoice.amount), 0)).where(
                and_(
                    Invoice.created_at >= month_start,
                    Invoice.created_at < month_end,
                )
            )
        )
        invoice_total = float(inv_result.scalar() or 0)

        # If no invoices, estimate from active engagements at that time
        if invoice_total == 0:
            eng_result = await db.execute(
                select(func.coalesce(func.sum(EngineEngagement.monthly_value), 0)).where(
                    and_(
                        EngineEngagement.status == "active",
                        EngineEngagement.created_at <= month_end,
                    )
                )
            )
            invoice_total = float(eng_result.scalar() or 0)

        mrr_trend.append(
            {
                "month": month_start.strftime("%Y-%m"),
                "mrr": round(invoice_total, 2),
            }
        )

    return RevenueData(
        current_mrr=round(current_mrr, 2),
        mrr_trend=mrr_trend,
        by_engine_type=by_engine_type,
        total_clients_by_status=total_clients_by_status,
        average_client_value=round(average_client_value, 2),
    )
