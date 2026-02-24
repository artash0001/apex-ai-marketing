"""
Apex AI Marketing - Deliverable (Content) Model

Represents content deliverables produced by AI agents, including
audits, reports, articles, email sequences, ad copy, and more.
"""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Text, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Deliverable(Base):
    """Deliverable record - any content piece produced for a client."""

    __tablename__ = "deliverables"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    engine_engagement_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("engine_engagements.id"),
        nullable=True,
    )
    client_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.id"), nullable=True
    )
    type: Mapped[str | None] = mapped_column(
        String(100),
        nullable=True,
        comment="audit_report | content_brief | article | email_sequence | ad_copy | report | etc.",
    )
    title: Mapped[str | None] = mapped_column(String(500), nullable=True)
    body: Mapped[str | None] = mapped_column(Text, nullable=True)
    meta_data: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default="draft",
        comment="draft | in_review | approved | delivered | rejected",
    )
    review_notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    ai_agent_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ai_model_used: Mapped[str | None] = mapped_column(String(100), nullable=True)
    ai_cost: Mapped[Decimal | None] = mapped_column(
        Numeric(8, 4), nullable=True
    )
    language: Mapped[str] = mapped_column(String(10), default="en")
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    delivered_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )

    # Relationships
    engine_engagement = relationship(
        "EngineEngagement", backref="deliverable_items", lazy="selectin"
    )
    client = relationship("Client", backref="deliverables", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Deliverable {self.title} ({self.type}) [{self.status}]>"
