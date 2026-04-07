from typing import Optional, List
from uuid import UUID
from datetime import datetime, timedelta
from extensions import db
from models.tenant import Tenant, TenantUser
from models.account import Account

class TenantService:
    """租户管理服务"""

    @staticmethod
    def create_tenant(name: str, tier: str = 'basic',
                      admin_email: str = None, **kwargs) -> Tenant:
        """创建新租户"""
        tenant = Tenant(
            name=name,
            tier=tier,
            status='trial',
            expires_at=datetime.utcnow() + timedelta(days=30),
            **kwargs
        )
        db.session.add(tenant)
        db.session.flush()  # 获取 ID

        # 如果提供了管理员邮箱，创建租户管理员关联
        if admin_email:
            user = Account.query.filter_by(email=admin_email).first()
            if user:
                TenantService.add_user_to_tenant(tenant.id, user.id, 'tenant_admin')

        db.session.commit()
        return tenant

    @staticmethod
    def get_tenant(tenant_id: UUID) -> Optional[Tenant]:
        """获取租户详情"""
        return Tenant.query.get(tenant_id)

    @staticmethod
    def update_tenant(tenant_id: UUID, **kwargs) -> Optional[Tenant]:
        """更新租户信息"""
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return None

        for key, value in kwargs.items():
            if hasattr(tenant, key):
                setattr(tenant, key, value)

        tenant.updated_at = datetime.utcnow()
        db.session.commit()
        return tenant

    @staticmethod
    def delete_tenant(tenant_id: UUID) -> bool:
        """删除租户"""
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return False

        db.session.delete(tenant)
        db.session.commit()
        return True

    @staticmethod
    def add_user_to_tenant(tenant_id: UUID, user_id: UUID,
                           role: str = 'member') -> TenantUser:
        """添加用户到租户"""
        tenant_user = TenantUser(
            tenant_id=tenant_id,
            user_id=user_id,
            role=role
        )
        db.session.add(tenant_user)
        db.session.commit()
        return tenant_user

    @staticmethod
    def remove_user_from_tenant(tenant_id: UUID, user_id: UUID) -> bool:
        """从租户移除用户"""
        tenant_user = TenantUser.query.filter_by(
            tenant_id=tenant_id,
            user_id=user_id
        ).first()

        if not tenant_user:
            return False

        db.session.delete(tenant_user)
        db.session.commit()
        return True

    @staticmethod
    def get_tenant_users(tenant_id: UUID) -> List[TenantUser]:
        """获取租户下所有用户"""
        return TenantUser.query.filter_by(tenant_id=tenant_id).all()

    @staticmethod
    def activate_tenant(tenant_id: UUID) -> Optional[Tenant]:
        """激活租户"""
        return TenantService.update_tenant(tenant_id, status='active')

    @staticmethod
    def suspend_tenant(tenant_id: UUID) -> Optional[Tenant]:
        """暂停租户"""
        return TenantService.update_tenant(tenant_id, status='suspended')

    @staticmethod
    def check_quota(tenant_id: UUID, resource: str, amount: int) -> bool:
        """检查租户配额是否足够

        对于 users 配额：检查当前用户数量 + amount 是否超过配额
        对于其他配额：检查 UsageRecord 中的实际使用量
        """
        from sqlalchemy import func
        from models.usage_record import UsageRecord

        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return False

        quota_map = {
            'users': tenant.quota_users,
            'apps': tenant.quota_apps,
            'api_calls': tenant.quota_api_calls,
        }

        quota = quota_map.get(resource, float('inf'))

        if resource == 'users':
            # 检查用户配额：当前用户数 + 申请数 <= 配额
            current_usage = TenantUser.query.filter_by(tenant_id=tenant_id).count()
            return (current_usage + amount) <= quota

        if resource in ('apps', 'api_calls'):
            # 检查应用/API配额：从 UsageRecord 获取当前使用量
            period = datetime.utcnow().strftime('%Y-%m')
            usage = db.session.query(
                func.coalesce(func.sum(UsageRecord.amount), 0)
            ).filter(
                UsageRecord.tenant_id == tenant_id,
                UsageRecord.resource_type == resource,
                UsageRecord.period == period
            ).scalar()

            return (int(usage) + amount) <= quota

        # 未知资源类型，默认允许
        return True
