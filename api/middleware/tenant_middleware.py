from functools import wraps
from flask import request, g, jsonify
from uuid import UUID
from services.tenant_service import TenantService

def tenant_required(f):
    """租户验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头获取租户 ID
        tenant_id = request.headers.get('X-Tenant-ID')
        if not tenant_id:
            return jsonify({'error': 'Tenant ID required'}), 401

        try:
            tenant_uuid = UUID(tenant_id)
        except ValueError:
            return jsonify({'error': 'Invalid Tenant ID format'}), 400

        # 验证租户存在
        tenant = TenantService.get_tenant(tenant_uuid)
        if not tenant:
            return jsonify({'error': 'Tenant not found'}), 404

        if tenant.status != 'active':
            return jsonify({'error': 'Tenant is not active'}), 403

        # 存储租户信息到请求上下文
        g.tenant_id = tenant_uuid
        g.tenant = tenant

        return f(*args, **kwargs)

    return decorated_function


def get_current_tenant_id() -> UUID:
    """获取当前请求的租户 ID"""
    return getattr(g, 'tenant_id', None)


def get_current_tenant():
    """获取当前租户对象"""
    return getattr(g, 'tenant', None)
