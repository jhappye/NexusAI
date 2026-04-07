from datetime import datetime
from flask import Blueprint, request, jsonify, g
from uuid import UUID
from services.audit_service import AuditService
from middleware.tenant_middleware import tenant_required

audit_bp = Blueprint('audit', __name__, url_prefix='/audit')


@audit_bp.route('/logs', methods=['GET'])
@tenant_required
def get_logs():
    """获取审计日志列表"""
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 50))
    action = request.args.get('action')

    start_date = None
    end_date = None
    if request.args.get('start_date'):
        start_date = datetime.fromisoformat(request.args['start_date'])
    if request.args.get('end_date'):
        end_date = datetime.fromisoformat(request.args['end_date'])

    result = AuditService.get_logs(
        tenant_id=g.tenant_id,
        page=page,
        page_size=page_size,
        action=action,
        start_date=start_date,
        end_date=end_date
    )
    return jsonify({'code': 0, 'data': result})


@audit_bp.route('/logs/<log_id>', methods=['GET'])
@tenant_required
def get_log_detail(log_id):
    """获取审计日志详情"""
    try:
        log_uuid = UUID(log_id)
    except ValueError:
        return jsonify({'error': 'Invalid log ID'}), 400

    log = AuditService.get_log_detail(log_uuid)
    if not log:
        return jsonify({'error': 'Log not found'}), 404

    return jsonify({'code': 0, 'data': log.to_dict()})
