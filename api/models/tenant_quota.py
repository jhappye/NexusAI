from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import DateTime, ForeignKey, Integer, String, UniqueConstraint, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TypeBase


class TenantQuota(TypeBase):
    """租户配额模型

    跟踪每个租户在不同时间段内的资源使用配额。
    支持按月统计 (period 格式: 'YYYY-MM')
    """
    __tablename__ = "tenant_quotas"
    __table_args__ = (
        sa.PrimaryKeyConstraint("id", name="tenant_quota_pkey"),
        sa.Index("idx_tenant_quotas_tenant_resource", "tenant_id", "resource_type", "period"),
        UniqueConstraint("tenant_id", "resource_type", "period", name="uq_tenant_resource_period"),
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
    resource_type: Mapped[str] = mapped_column(String(50), nullable=False)
    # resource_type 可选值: 'token', 'api_call', 'storage'
    quota: Mapped[int] = mapped_column(Integer, nullable=False)
    used: Mapped[int] = mapped_column(Integer, server_default=sa.text("0"), default=0)
    period: Mapped[str] = mapped_column(String(7), nullable=False)  # 'YYYY-MM'
    updated_at: Mapped[datetime] = mapped_column(
        DateTime,
        server_default=func.current_timestamp(),
        nullable=False,
        init=False,
        onupdate=func.current_timestamp(),
    )

    # 关系
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="quotas")
