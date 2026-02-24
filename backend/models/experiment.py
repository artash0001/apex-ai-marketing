"""
Apex AI Marketing - Experiment Model

Tracks structured marketing experiments: A/B tests, hypothesis-driven
changes, and measured outcomes with learnings.
"""

import uuid
from datetime import date, datetime

from sqlalchemy import String, Text, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Experiment(Base):
    """Experiment record - a structured marketing test."""

    __tablename__ = "experiments"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    client_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True
    )
    engine_engagement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("engine_engagements.id"),
        nullable=True,
    )
    hypothesis: Mapped[str] = mapped_column(Text, nullable=False)
    variable_changed: Mapped[str | None] = mapped_column(Text, nullable=True)
    primary_metric: Mapped[str | None] = mapped_column(
        String(255), nullable=True
    )
    guardrail_metrics: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True
    )
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    result_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    decision: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="implement | iterate | discard",
    )
    learning: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default="planned",
        comment="planned | running | completed | cancelled",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationships
    client = relationship("Client", backref="experiments", lazy="selectin")
    engine_engagement = relationship(
        "EngineEngagement", backref="experiments", lazy="selectin"
    )

    def __repr__(self) -> str:
        return f"<Experiment {self.id} [{self.status}] - {self.hypothesis[:60]}>"
