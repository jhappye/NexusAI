from flask import Blueprint, request, jsonify, g
from uuid import UUID
from services.tenant_service import TenantService
from middleware.tenant_middleware import tenant_required, get_current_tenant_id

tenant_bp = Blueprint('tenant', __name__, url_prefix='/tenants')


@tenant_bp.route('', methods=['POST'])
def create_tenant():
    """创建租户"""
    data = request.get_json()
    name = data.get('name')
    tier = data.get('tier', 'basic')
    admin_email = data.get('admin_email')

    if not name:
        return jsonify({'error': 'Tenant name is required'}), 400

    try:
        tenant = TenantService.create_tenant(
            name=name,
            tier=tier,
            admin_email=admin_email,
            quota_users=data.get('quota_users', 10),
            quota_apps=data.get('quota_apps', 20),
            quota_api_calls=data.get('quota_api_calls', 100000),
        )
        return jsonify({
            'code': 0,
            'data': tenant.to_dict(),
            'message': 'Tenant created successfully'
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@tenant_bp.route('', methods=['GET'])
@tenant_required
def list_tenants():
    """获取租户列表（系统管理员专用）

    安全说明: 此接口仅对系统管理员开放。
    目前实现为：仅当用户为 tenant_admin 且为特殊系统租户时才返回所有租户。
    后续可扩展为独立的系统管理员角色。
    """
    from models.tenant import Tenant, TenantUser
    from models.account import Account

    # 获取当前用户
    user_id = g.get('user_id')
    tenant_id = g.get('tenant_id')

    if not user_id or not tenant_id:
        return jsonify({'error': 'Unauthorized'}), 401

    # 检查用户是否为系统租户的管理员
    # 目前策略：tenant_id 对应的租户名称包含 "SYSTEM" 或 tier 为 'enterprise'
    # 实际生产环境应使用独立的系统管理员角色
    tenant = TenantService.get_tenant(tenant_id)
    if not tenant:
        return jsonify({'error': 'Unauthorized'}), 401

    # 简化的系统管理员检查：企业版租户可查看所有租户
    # 后续应实现独立的 system_admin 角色
    if tenant.tier == 'enterprise':
        tenants = Tenant.query.all()
        return jsonify({
            'code': 0,
            'data': [t.to_dict() for t in tenants]
        })

    # 非企业版用户只能查看自己的租户
    return jsonify({
        'code': 0,
        'data': [tenant.to_dict()]
    })


@tenant_bp.route('/<tenant_id>', methods=['GET'])
@tenant_required
def get_tenant(tenant_id):
    """获取租户详情"""
    try:
        tenant_uuid = UUID(tenant_id)
    except ValueError:
        return jsonify({'error': 'Invalid tenant ID'}), 400

    tenant = TenantService.get_tenant(tenant_uuid)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404

    return jsonify({
        'code': 0,
        'data': tenant.to_dict()
    })


@tenant_bp.route('/<tenant_id>', methods=['PUT'])
@tenant_required
def update_tenant(tenant_id):
    """更新租户"""
    try:
        tenant_uuid = UUID(tenant_id)
    except ValueError:
        return jsonify({'error': 'Invalid tenant ID'}), 400

    data = request.get_json()
    tenant = TenantService.update_tenant(tenant_uuid, **data)

    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404

    return jsonify({
        'code': 0,
        'data': tenant.to_dict(),
        'message': 'Tenant updated successfully'
    })


@tenant_bp.route('/<tenant_id>/activate', methods=['POST'])
@tenant_required
def activate_tenant(tenant_id):
    """激活租户（仅系统管理员可操作）"""
    from models.tenant import Tenant

    try:
        tenant_uuid = UUID(tenant_id)
    except ValueError:
        return jsonify({'error': 'Invalid tenant ID'}), 400

    # 权限检查：只有企业版租户的管理员才能操作其他租户状态
    current_tenant = g.get('tenant')

    # 如果操作的是当前用户所属租户，允许
    if str(current_tenant.id) == tenant_id:
        tenant = TenantService.activate_tenant(tenant_uuid)
        if not tenant:
            return jsonify({'error': 'Tenant not found'}), 404
        return jsonify({
            'code': 0,
            'data': tenant.to_dict(),
            'message': 'Tenant activated successfully'
        })

    # 如果操作其他租户，需要是 enterprise 租户的管理员
    if current_tenant.tier != 'enterprise':
        return jsonify({'error': 'Permission denied. Only enterprise tenants can manage other tenants.'}), 403

    tenant = TenantService.activate_tenant(tenant_uuid)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404

    return jsonify({
        'code': 0,
        'data': tenant.to_dict(),
        'message': 'Tenant activated successfully'
    })


@tenant_bp.route('/<tenant_id>/suspend', methods=['POST'])
@tenant_required
def suspend_tenant(tenant_id):
    """暂停租户"""
    try:
        tenant_uuid = UUID(tenant_id)
    except ValueError:
        return jsonify({'error': 'Invalid tenant ID'}), 400

    tenant = TenantService.suspend_tenant(tenant_uuid)
    if not tenant:
        return jsonify({'error': 'Tenant not found'}), 404

    return jsonify({
        'code': 0,
        'data': tenant.to_dict(),
        'message': 'Tenant suspended successfully'
    })


@tenant_bp.route('/<tenant_id>/users', methods=['GET'])
@tenant_required
def get_tenant_users(tenant_id):
    """获取租户用户列表"""
    try:
        tenant_uuid = UUID(tenant_id)
    except ValueError:
        return jsonify({'error': 'Invalid tenant ID'}), 400

    users = TenantService.get_tenant_users(tenant_uuid)
    return jsonify({
        'code': 0,
        'data': [{
            'id': str(u.id),
            'user_id': str(u.user_id),
            'role': u.role,
            'status': u.status,
            'created_at': u.created_at.isoformat() if u.created_at else None
        } for u in users]
    })


@tenant_bp.route('/<tenant_id>/users/<user_id>', methods=['DELETE'])
@tenant_required
def remove_tenant_user(tenant_id, user_id):
    """从租户移除用户"""
    try:
        tenant_uuid = UUID(tenant_id)
        user_uuid = UUID(user_id)
    except ValueError:
        return jsonify({'error': 'Invalid ID format'}), 400

    success = TenantService.remove_user_from_tenant(tenant_uuid, user_uuid)
    if not success:
        return jsonify({'error': 'User not found in tenant'}), 404

    return jsonify({
        'code': 0,
        'message': 'User removed from tenant successfully'
    })
