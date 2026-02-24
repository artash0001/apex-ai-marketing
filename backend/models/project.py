"""
Apex AI Marketing - Engine Engagement Model

Represents a specific engine engagement (project) for a client,
including scope, deliverables, timeline, and KPI targets.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import String, Text, Integer, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class EngineEngagement(Base):
    """Engine engagement record - a running engine for a specific client."""

    __tablename__ = "engine_engagements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False
    )
    engine_name: Mapped[str] = mapped_column(String(100), nullable=False)
    status: Mapped[str] = mapped_column(
        String(50),
        default="proposed",
        comment="proposed | active | paused | completed",
    )
    scope_doc: Mapped[str | None] = mapped_column(
        Text, nullable=True, comment="What is included and excluded"
    )
    deliverables: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True, comment="List of deliverables with status"
    )
    timeline_weeks: Mapped[int | None] = mapped_column(Integer, nullable=True)
    monthly_price: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    start_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    end_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    kpi_targets: Mapped[dict | None] = mapped_column(
        JSONB, nullable=True, comment="{metric: target} pairs"
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationships
    client = relationship("Client", backref="engine_engagements", lazy="selectin")

    def __repr__(self) -> str:
        return f"<EngineEngagement {self.engine_name} for client={self.client_id} [{self.status}]>"
