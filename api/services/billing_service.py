from datetime import datetime
from typing import Optional, Dict
from uuid import UUID
from sqlalchemy import func, and_
from decimal import Decimal
from extensions import db
from models.usage_record import UsageRecord
from models.tenant import Tenant

# 计费规则（元/1K tokens 或 元/次）
BILLING_RULES = {
    'token_input': Decimal('0.001'),
    'token_output': Decimal('0.002'),
    'api_call': Decimal('0.01'),
    'storage': Decimal('0.001'),  # 元/MB/月
}


class BillingService:
    """计费服务"""

    @staticmethod
    def calculate_cost(resource_type: str, amount: int) -> Decimal:
        """根据资源类型和用量计算费用"""
        rate = BILLING_RULES.get(resource_type, Decimal('0'))
        if 'token' in resource_type:
            return Decimal(amount) * rate / 1000
        return Decimal(amount) * rate

    @staticmethod
    def record_usage(tenant_id: UUID, user_id: Optional[UUID],
                    resource_type: str, amount: int,
                    period: str = None) -> UsageRecord:
        """记录用量"""
        if period is None:
            period = datetime.utcnow().strftime('%Y-%m')

        cost = BillingService.calculate_cost(resource_type, amount)

        record = UsageRecord(
            tenant_id=tenant_id,
            user_id=user_id,
            resource_type=resource_type,
            amount=amount,
            cost=cost,
            period=period
        )
        db.session.add(record)
        db.session.commit()
        return record

    @staticmethod
    def get_tenant_usage(tenant_id: UUID, period: str = None) -> Dict:
        """获取租户指定周期的用量汇总"""
        if period is None:
            period = datetime.utcnow().strftime('%Y-%m')

        results = db.session.query(
            UsageRecord.resource_type,
            func.sum(UsageRecord.amount).label('total_amount'),
            func.sum(UsageRecord.cost).label('total_cost')
        ).filter(
            and_(
                UsageRecord.tenant_id == tenant_id,
                UsageRecord.period == period
            )
        ).group_by(UsageRecord.resource_type).all()

        return {
            'period': period,
            'tenant_id': str(tenant_id),
            'items': [
                {
                    'resource_type': r.resource_type,
                    'total_amount': r.total_amount or 0,
                    'total_cost': float(r.total_cost or 0)
                }
                for r in results
            ],
            'total_cost': sum(float(r.total_cost or 0) for r in results)
        }

    @staticmethod
    def get_tenant_usage_trend(tenant_id: UUID, months: int = 6) -> list:
        """获取租户用量趋势"""
        results = db.session.query(
            UsageRecord.period,
            func.sum(UsageRecord.cost).label('total_cost')
        ).filter(
            UsageRecord.tenant_id == tenant_id
        ).group_by(UsageRecord.period).order_by(
            UsageRecord.period.desc()
        ).limit(months).all()

        return [
            {
                'period': r.period,
                'total_cost': float(r.total_cost or 0)
            }
            for r in results
        ]

    @staticmethod
    def check_budget_alert(tenant_id: UUID) -> bool:
        """检查是否超过预算告警阈值"""
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return False

        current_usage = BillingService.get_tenant_usage(tenant_id)
        monthly_budget = getattr(tenant, 'monthly_budget', None)

        if not monthly_budget:
            return False

        return current_usage['total_cost'] >= monthly_budget
