from datetime import datetime
from decimal import Decimal
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, Integer, Numeric, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TypeBase


class UsageRecord(TypeBase):
    """用量记录模型

    记录每个租户的详细使用情况，用于计费和审计。
    """
    __tablename__ = "usage_records"
    __table_args__ = (
        sa.PrimaryKeyConstraint("id", name="usage_record_pkey"),
        sa.Index("idx_usage_records_tenant_period", "tenant_id", "period"),
        sa.Index("idx_usage_records_user_id", "user_id"),
        sa.Index("idx_usage_records_resource_type", "resource_type"),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        init=False,
    )
    tenant_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("tenant_profiles.id", ondelete="CASCADE"),
        nullable=False,
    )
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # resource_type 可选值: 'token_input', 'token_output', 'api_call'
    amount: Mapped[int] = mapped_column(Integer, nullable=False)
    cost: Mapped[Decimal] = mapped_column(Numeric(10, 4), server_default=sa.text("0"), default=Decimal("0"))
    period: Mapped[str] = mapped_column(String(7), nullable=False)  # 'YYYY-MM'
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), nullable=False, init=False
    )

    # 关系
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="usage_records")
