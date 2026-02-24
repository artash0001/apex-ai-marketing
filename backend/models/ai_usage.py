"""
Apex AI Marketing - AI Usage Model

Tracks every AI API call: model, token counts, cost, and the agent/task
that triggered it. Used for cost monitoring and per-client billing.
"""

import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class AIUsage(Base):
    """AI usage record - one row per Claude API call."""

    __tablename__ = "ai_usage"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    agent_name: Mapped[str | None] = mapped_column(String(100), nullable=True)
    model: Mapped[str | None] = mapped_column(String(100), nullable=True)
    input_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    output_tokens: Mapped[int | None] = mapped_column(Integer, nullable=True)
    cost: Mapped[Decimal | None] = mapped_column(Numeric(8, 6), nullable=True)
    task_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True), ForeignKey("tasks.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationships
    task = relationship("Task", backref="ai_usage_records", lazy="selectin")

    def __repr__(self) -> str:
        return f"<AIUsage agent={self.agent_name} model={self.model} cost={self.cost}>"
