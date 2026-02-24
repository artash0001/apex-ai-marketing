"""
Apex AI Marketing - Task Model

Tracks internal agent work queue items: pending work, agent assignments,
execution status, and cost tracking.
"""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Text, Integer, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Task(Base):
    """Task record - an item in the internal agent work queue."""

    __tablename__ = "tasks"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_engagement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("engine_engagements.id"),
        nullable=True,
    )
    assigned_agent: Mapped[str | None] = mapped_column(
        String(100), nullable=True
    )
    type: Mapped[str | None] = mapped_column(String(100), nullable=True)
    description: Mapped[str | None] = mapped_column(Text, nullable=True)
    input_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    output_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default="pending",
        comment="pending | in_progress | in_review | completed | failed",
    )
    priority: Mapped[int] = mapped_column(Integer, default=5)
    due_date: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    ai_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 4), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationships
    engine_engagement = relationship(
        "EngineEngagement", backref="tasks", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Task {self.type} [{self.status}] agent={self.assigned_agent}>"
