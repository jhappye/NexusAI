from flask import Blueprint, request, jsonify, g
from uuid import UUID
from services.billing_service import BillingService
from middleware.tenant_middleware import tenant_required

billing_bp = Blueprint('billing', __name__, url_prefix='/billing')


@billing_bp.route('/usage', methods=['GET'])
@tenant_required
def get_usage():
    """获取当前租户用量"""
    period = request.args.get('period')  # YYYY-MM 格式
    usage = BillingService.get_tenant_usage(g.tenant_id, period)
    return jsonify({'code': 0, 'data': usage})


@billing_bp.route('/usage/trend', methods=['GET'])
@tenant_required
def get_usage_trend():
    """获取用量趋势"""
    months = int(request.args.get('months', 6))
    trend = BillingService.get_tenant_usage_trend(g.tenant_id, months)
    return jsonify({'code': 0, 'data': trend})


@billing_bp.route('/record', methods=['POST'])
@tenant_required
def record_usage():
    """记录用量（通常由内部服务调用）"""
    data = request.get_json()
    resource_type = data.get('resource_type')
    amount = data.get('amount')
    user_id = data.get('user_id')

    if not resource_type or not amount:
        return jsonify({'error': 'resource_type and amount are required'}), 400

    record = BillingService.record_usage(
        tenant_id=g.tenant_id,
        user_id=UUID(user_id) if user_id else None,
        resource_type=resource_type,
        amount=amount
    )

    return jsonify({
        'code': 0,
        'data': {
            'id': str(record.id),
            'cost': float(record.cost)
        }
    }), 201
