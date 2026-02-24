"""
Apex AI Marketing - Client Model

Represents agency clients with full profile, status tracking,
and engine engagement metadata.
"""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import String, Text, Boolean, Numeric, DateTime
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class Client(Base):
    """Client record - companies/people the agency works with."""

    __tablename__ = "clients"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    company: Mapped[str | None] = mapped_column(String(255), nullable=True)
    email: Mapped[str | None] = mapped_column(String(255), nullable=True)
    phone: Mapped[str | None] = mapped_column(String(50), nullable=True)
    whatsapp: Mapped[str | None] = mapped_column(String(50), nullable=True)
    telegram: Mapped[str | None] = mapped_column(String(100), nullable=True)
    industry: Mapped[str | None] = mapped_column(String(100), nullable=True)
    website: Mapped[str | None] = mapped_column(String(500), nullable=True)
    language: Mapped[str] = mapped_column(String(10), default="en")
    brand_voice_doc: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        String(50),
        default="lead",
        comment="lead | audit_requested | audit_delivered | active | paused | churned",
    )
    active_engines: Mapped[dict | None] = mapped_column(JSONB, default=list)
    monthly_value: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    onboarding_completed: Mapped[bool] = mapped_column(Boolean, default=False)
    market: Mapped[str | None] = mapped_column(
        String(50),
        nullable=True,
        comment="dubai | uk | global | russian_dubai",
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )

    def __repr__(self) -> str:
        return f"<Client {self.name} ({self.company}) [{self.status}]>"
