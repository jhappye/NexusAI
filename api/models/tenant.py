import enum
from datetime import datetime
from uuid import uuid4

import sqlalchemy as sa
from sqlalchemy import DateTime, Enum, ForeignKey, Integer, String, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import TypeBase


class TenantTier(enum.StrEnum):
    BASIC = "basic"
    PROFESSIONAL = "professional"
    ENTERPRISE = "enterprise"


class TenantStatus(enum.StrEnum):
    ACTIVE = "active"
    SUSPENDED = "suspended"
    TRIAL = "trial"


class TenantUserRole(enum.StrEnum):
    TENANT_ADMIN = "tenant_admin"
    MEMBER = "member"


class TenantUserStatus(enum.StrEnum):
    ACTIVE = "active"
    INACTIVE = "inactive"


class Tenant(TypeBase):
    """租户模型 - 多租户架构核心模型

    支持三种隔离级别：
    - 基础版 (basic): 逻辑隔离 (tenant_id)
    - 专业版 (professional): Schema 隔离
    - 企业版 (enterprise): 独立数据库
    """
    __tablename__ = "tenant_profiles"
    __table_args__ = (
        sa.PrimaryKeyConstraint("id", name="tenant_profile_pkey"),
        sa.Index("idx_tenant_profiles_status", "status"),
        sa.Index("idx_tenant_profiles_tier", "tier"),
    )

    id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid4,
        init=False,
    )
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    tier: Mapped[TenantTier] = mapped_column(
        Enum(TenantTier, name="tenant_tier", create_type=False),
        server_default=sa.text("'basic'"),
        default=TenantTier.BASIC,
    )
    status: Mapped[TenantStatus] = mapped_column(
        Enum(TenantStatus, name="tenant_status", create_type=False),
        server_default=sa.text("'trial'"),
        default=TenantStatus.TRIAL,
    )

    # 资源配额
    quota_users: Mapped[int] = mapped_column(Integer, server_default=sa.text("10"), default=10)
    quota_apps: Mapped[int] = mapped_column(Integer, server_default=sa.text("20"), default=20)
    quota_api_calls: Mapped[int] = mapped_column(Integer, server_default=sa.text("100000"), default=100000)

    # 企业版专用
    db_schema: Mapped[str | None] = mapped_column(String(63), nullable=True)

    # 时间戳
    expires_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), nullable=False, init=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), init=False, onupdate=func.current_timestamp()
    )

    # 关系
    users: Mapped[list["TenantUser"]] = relationship(
        "TenantUser",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    quotas: Mapped[list["TenantQuota"]] = relationship(
        "TenantQuota",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )
    usage_records: Mapped[list["UsageRecord"]] = relationship(
        "UsageRecord",
        back_populates="tenant",
        cascade="all, delete-orphan",
        lazy="dynamic",
    )

    def to_dict(self) -> dict:
        return {
            "id": str(self.id),
            "name": self.name,
            "tier": self.tier.value if self.tier else None,
            "status": self.status.value if self.status else None,
            "quota_users": self.quota_users,
            "quota_apps": self.quota_apps,
            "quota_api_calls": self.quota_api_calls,
            "db_schema": self.db_schema,
            "expires_at": self.expires_at.isoformat() if self.expires_at else None,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class TenantUser(TypeBase):
    """租户用户关联模型

    建立用户与租户的多对多关系，支持在租户内的角色定义。
    """
    __tablename__ = "tenant_users"
    __table_args__ = (
        sa.PrimaryKeyConstraint("id", name="tenant_user_pkey"),
        sa.Index("idx_tenant_users_tenant_id", "tenant_id"),
        sa.Index("idx_tenant_users_user_id", "user_id"),
        sa.UniqueConstraint("tenant_id", "user_id", name="uq_tenant_user"),
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
    user_id: Mapped[str] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("accounts.id", ondelete="CASCADE"),
        nullable=False,
    )
    role: Mapped[TenantUserRole] = mapped_column(
        Enum(TenantUserRole, name="tenant_user_role", create_type=False),
        server_default=sa.text("'member'"),
        default=TenantUserRole.MEMBER,
    )
    status: Mapped[TenantUserStatus] = mapped_column(
        Enum(TenantUserStatus, name="tenant_user_status", create_type=False),
        server_default=sa.text("'active'"),
        default=TenantUserStatus.ACTIVE,
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.current_timestamp(), nullable=False, init=False
    )

    # 关系
    tenant: Mapped["Tenant"] = relationship("Tenant", back_populates="users")
    user: Mapped["Account"] = relationship(
        "Account",
        back_populates="tenant_users",
        foreign_keys=[user_id],
    )
