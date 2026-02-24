"""
Apex AI Marketing - Invoice Model

Tracks billing and payment for client engine engagements.
"""

import uuid
from datetime import date, datetime
from decimal import Decimal

from sqlalchemy import String, Text, Numeric, Date, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Invoice(Base):
    """Invoice record - billing item for a client."""

    __tablename__ = "invoices"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    client_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False
    )
    amount: Mapped[Decimal | None] = mapped_column(
        Numeric(10, 2), nullable=True
    )
    currency: Mapped[str] = mapped_column(String(10), default="USD")
    status: Mapped[str] = mapped_column(
        String(50),
        default="draft",
        comment="draft | sent | paid | overdue",
    )
    due_date: Mapped[date | None] = mapped_column(Date, nullable=True)
    paid_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    items: Mapped[dict | None] = mapped_column(JSONB, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationships
    client = relationship("Client", backref="invoices", lazy="selectin")

    def __repr__(self) -> str:
        return f"<Invoice {self.id} client={self.client_id} {self.amount} {self.currency} [{self.status}]>"
