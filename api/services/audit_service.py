from datetime import datetime
from typing import Optional, Dict, List
from uuid import UUID
from flask import request
from sqlalchemy import and_, desc
from extensions.ext_database import db
from models.audit_log import AuditLog

# 需要记录的操作
AUDIT_ACTIONS = {
    # 用户相关
    'user.login': 'user',
    'user.logout': 'user',
    'user.create': 'user',
    'user.update': 'user',
    'user.delete': 'user',
    # 应用相关
    'app.create': 'app',
    'app.update': 'app',
    'app.delete': 'app',
    'app.publish': 'app',
    # 知识库相关
    'knowledge.create': 'knowledge',
    'knowledge.upload': 'knowledge',
    'knowledge.delete': 'knowledge',
    # 工作流相关
    'workflow.create': 'workflow',
    'workflow.update': 'workflow',
    'workflow.delete': 'workflow',
    'workflow.execute': 'workflow',
}


class AuditService:
    """审计日志服务"""

    @staticmethod
    def log(tenant_id: Optional[UUID], user_id: Optional[UUID],
            action: str, resource_type: str = None,
            resource_id: UUID = None, resource_name: str = None,
            details: Dict = None):
        """记录审计日志"""
        ip_address = None
        user_agent = None

        try:
            if request:
                ip_address = request.remote_addr
                user_agent = request.headers.get('User-Agent', '')[:500]
        except RuntimeError:
            pass  # Outside request context

        audit_log = AuditLog(
            tenant_id=tenant_id,
            user_id=user_id,
            action=action,
            resource_type=resource_type or AUDIT_ACTIONS.get(action),
            resource_id=resource_id,
            resource_name=resource_name,
            details=details,
            ip_address=ip_address,
            user_agent=user_agent
        )
        db.session.add(audit_log)
        db.session.commit()
        return audit_log

    @staticmethod
    def get_logs(tenant_id: UUID, page: int = 1,
                 page_size: int = 50, action: str = None,
                 start_date: datetime = None, end_date: datetime = None) -> Dict:
        """获取审计日志列表"""
        query = AuditLog.query.filter(AuditLog.tenant_id == tenant_id)

        if action:
            query = query.filter(AuditLog.action == action)
        if start_date:
            query = query.filter(AuditLog.created_at >= start_date)
        if end_date:
            query = query.filter(AuditLog.created_at <= end_date)

        query = query.order_by(desc(AuditLog.created_at))

        total = query.count()
        logs = query.offset((page - 1) * page_size).limit(page_size).all()

        return {
            'total': total,
            'page': page,
            'page_size': page_size,
            'logs': [log.to_dict() for log in logs]
        }

    @staticmethod
    def get_log_detail(log_id: UUID) -> Optional[AuditLog]:
        """获取单条日志详情"""
        return AuditLog.query.get(log_id)


# 便捷函数
def audit_log(tenant_id: UUID, user_id: UUID, action: str, **kwargs):
    """记录审计日志的便捷函数"""
    return AuditService.log(tenant_id, user_id, action, **kwargs)
