from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import DateTime, Index, JSON, String, Text, func
from sqlalchemy.dialects.postgresql import INET, UUID
from sqlalchemy.orm import Mapped, mapped_column

from .base import TypeBase


class AuditLog(TypeBase):
    """审计日志模型

    记录所有租户内的关键操作，用于安全审计和合规性检查。
    """
    __tablename__ = "audit_logs"
    __table_args__ = (
        sa.PrimaryKeyConstraint("id", name="audit_log_pkey"),
        Index("idx_audit_logs_tenant_time", "tenant_id", "created_at"),
        Index("idx_audit_logs_user_time", "user_id", "created_at"),
        Index("idx_audit_logs_action", "action"),
        Index("idx_audit_logs_resource", "resource_type", "resource_id"),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        init=False,
    )
    tenant_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    user_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    action: Mapped[str] = mapped_column(String(100), nullable=False)
    # action 示例: 'app.create', 'user.login', 'workflow.publish'
    resource_type: Mapped[str | None] = mapped_column(String(50), nullable=True)
    # resource_type 示例: 'app', 'user', 'workflow'
    resource_id: Mapped[str | None] = mapped_column(UUID(as_uuid=True), nullable=True)
    resource_name: Mapped[str | None] = mapped_column(String(255), nullable=True)
    details: Mapped[dict | None] = mapped_column(JSON, nullable=True)  # 额外详情
    ip_address: Mapped[str | None] = mapped_column(INET, nullable=True)
    user_agent: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), nullable=False, init=False
    )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "tenant_id": str(self.tenant_id) if self.tenant_id else None,
            "user_id": str(self.user_id) if self.user_id else None,
            "action": self.action,
            "resource_type": self.resource_type,
            "resource_id": str(self.resource_id) if self.resource_id else None,
            "resource_name": self.resource_name,
            "details": self.details,
            "ip_address": str(self.ip_address) if self.ip_address else None,
            "user_agent": self.user_agent,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }
