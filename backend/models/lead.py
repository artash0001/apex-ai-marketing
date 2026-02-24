"""
Apex AI Marketing - Lead Model

Represents sales leads for Apex's own outreach pipeline.
Tracks prospects from initial contact through to close.
"""

import uuid
from datetime import date, datetime

from sqlalchemy import String, Text, Integer, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Lead(Base):
    """Lead record - a prospect in the agency's outreach pipeline."""

    __tablename__ = "leads"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    linkedin_url: Mapped[str | None] = mapped_column(String(500), nullable=True)
    telegram: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    company_size: Mapped[str | None] = mapped_column(String(50), nullable=True)
    market: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="dubai | uk | global | russian_dubai",
    )
    language: Mapped[str] = mapped_column(String(10), default="en")
    pain_points: Mapped[str | None] = mapped_column(Text, nullable=True)
    outreach_status: Mapped[str] = mapped_column(
        String(50),
        default="new",
        comment="new | contacted | replied | meeting_booked | audit_sent | proposal_sent | won | lost",
    )
    outreach_channel: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="email | linkedin | telegram | whatsapp | referral",
    )
    last_contacted_at: Mapped[datetime | None] = mapped_column(
        DateTime, nullable=True
    )
    next_follow_up: Mapped[date | None] = mapped_column(Date, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    sequence_step: Mapped[int] = mapped_column(Integer, default=0)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Lead {self.name} ({self.company}) [{self.outreach_status}]>"
