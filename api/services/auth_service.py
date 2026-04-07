from functools import wraps
from flask import jsonify, g
from uuid import UUID
from typing import List
from models.tenant import TenantUser

# 权限定义
PERMISSIONS = {
    'tenant_admin': [
        'tenant:read', 'tenant:update',
        'user:create', 'user:read', 'user:update', 'user:delete',
        'app:create', 'app:read', 'app:update', 'app:delete',
        'workflow:create', 'workflow:execute',
        'knowledge:create', 'knowledge:manage',
    ],
    'member': [
        'app:create', 'app:read', 'app:update', 'app:delete',
        'workflow:create', 'workflow:execute',
        'knowledge:create', 'knowledge:read',
    ]
}


class AuthService:
    """权限认证服务"""

    @staticmethod
    def get_user_role_in_tenant(user_id: UUID, tenant_id: UUID) -> str:
        """获取用户在租户中的角色"""
        tenant_user = TenantUser.query.filter_by(
            user_id=user_id,
            tenant_id=tenant_id
        ).first()
        return tenant_user.role if tenant_user else None

    @staticmethod
    def check_permission(user_id: UUID, tenant_id: UUID, permission: str) -> bool:
        """检查用户是否具有特定权限"""
        role = AuthService.get_user_role_in_tenant(user_id, tenant_id)
        if not role:
            return False
        return permission in PERMISSIONS.get(role, [])

    @staticmethod
    def get_user_permissions(user_id: UUID, tenant_id: UUID) -> List[str]:
        """获取用户在租户中的所有权限"""
        role = AuthService.get_user_role_in_tenant(user_id, tenant_id)
        return PERMISSIONS.get(role, [])

    @staticmethod
    def require_permission(permission: str):
        """权限验证装饰器"""
        def decorator(f):
            @wraps(f)
            def decorated_function(*args, **kwargs):
                user_id = getattr(g, 'user_id', None)
                tenant_id = getattr(g, 'tenant_id', None)

                if not user_id or not tenant_id:
                    return jsonify({'error': 'Unauthorized'}), 401

                if not AuthService.check_permission(user_id, tenant_id, permission):
                    return jsonify({'error': 'Permission denied'}), 403

                return f(*args, **kwargs)
            return decorated_function
        return decorator
