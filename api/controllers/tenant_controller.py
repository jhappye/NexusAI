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
    """获取租户列表（系统管理员）"""
    from models.tenant import Tenant
    tenants = Tenant.query.all()
    return jsonify({
        'code': 0,
        'data': [t.to_dict() for t in tenants]
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
    """激活租户"""
    try:
        tenant_uuid = UUID(tenant_id)
    except ValueError:
        return jsonify({'error': 'Invalid tenant ID'}), 400

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
