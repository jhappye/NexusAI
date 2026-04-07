"""add tenant profile and related tables

This migration creates the multi-tenant architecture tables:
- tenant_profiles: Core tenant model with tier, quotas, and status
- tenant_users: User-tenant associations with roles
- tenant_quotas: Resource quota tracking per tenant
- usage_records: Detailed usage tracking for billing
- audit_logs: Security audit trail

Revision ID: tenant_profiles_v1
Revises: 2beac44e5f5f
Create Date: 2026-04-07 00:00:00.000000

"""
import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

import models.types

# revision identifiers, used by Alembic.
revision = 'tenant_profiles_v1'
down_revision = '2beac44e5f5f'
branch_labels = None
depends_on = None


def upgrade():
    # Create tenant_tier enum
    tenant_tier_enum = postgresql.ENUM('basic', 'professional', 'enterprise', name='tenant_tier', create_type=False)
    tenant_tier_enum.create(op.get_bind(), checkfirst=True)

    # Create tenant_status enum
    tenant_status_enum = postgresql.ENUM('active', 'suspended', 'trial', name='tenant_status', create_type=False)
    tenant_status_enum.create(op.get_bind(), checkfirst=True)

    # Create tenant_user_role enum
    tenant_user_role_enum = postgresql.ENUM('tenant_admin', 'member', name='tenant_user_role', create_type=False)
    tenant_user_role_enum.create(op.get_bind(), checkfirst=True)

    # Create tenant_user_status enum
    tenant_user_status_enum = postgresql.ENUM('active', 'inactive', name='tenant_user_status', create_type=False)
    tenant_user_status_enum.create(op.get_bind(), checkfirst=True)

    # Create tenant_profiles table
    op.create_table(
        'tenant_profiles',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('tier', tenant_tier_enum, server_default='basic', nullable=False),
        sa.Column('status', tenant_status_enum, server_default='trial', nullable=False),
        sa.Column('quota_users', sa.Integer, server_default='10', nullable=False),
        sa.Column('quota_apps', sa.Integer, server_default='20', nullable=False),
        sa.Column('quota_api_calls', sa.Integer, server_default='100000', nullable=False),
        sa.Column('db_schema', sa.String(63), nullable=True),
        sa.Column('expires_at', sa.DateTime, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
    )
    op.create_index('idx_tenant_profiles_status', 'tenant_profiles', ['status'])
    op.create_index('idx_tenant_profiles_tier', 'tenant_profiles', ['tier'])

    # Create tenant_users table
    op.create_table(
        'tenant_users',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('accounts.id', ondelete='CASCADE'), nullable=False),
        sa.Column('role', tenant_user_role_enum, server_default='member', nullable=False),
        sa.Column('status', tenant_user_status_enum, server_default='active', nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
    )
    op.create_index('idx_tenant_users_tenant_id', 'tenant_users', ['tenant_id'])
    op.create_index('idx_tenant_users_user_id', 'tenant_users', ['user_id'])
    op.create_unique_constraint('uq_tenant_user', 'tenant_users', ['tenant_id', 'user_id'])

    # Create tenant_quotas table
    op.create_table(
        'tenant_quotas',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('quota', sa.Integer, nullable=False),
        sa.Column('used', sa.Integer, server_default='0', nullable=False),
        sa.Column('period', sa.String(7), nullable=False),
        sa.Column('updated_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
    )
    op.create_index('idx_tenant_quotas_tenant_resource', 'tenant_quotas', ['tenant_id', 'resource_type', 'period'])
    op.create_unique_constraint('uq_tenant_resource_period', 'tenant_quotas', ['tenant_id', 'resource_type', 'period'])

    # Create usage_records table
    op.create_table(
        'usage_records',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), sa.ForeignKey('tenant_profiles.id', ondelete='CASCADE'), nullable=False),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('resource_type', sa.String(50), nullable=False),
        sa.Column('amount', sa.Integer, nullable=False),
        sa.Column('cost', sa.Numeric(10, 4), server_default='0', nullable=False),
        sa.Column('period', sa.String(7), nullable=False),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
    )
    op.create_index('idx_usage_records_tenant_period', 'usage_records', ['tenant_id', 'period'])
    op.create_index('idx_usage_records_user_id', 'usage_records', ['user_id'])
    op.create_index('idx_usage_records_resource_type', 'usage_records', ['resource_type'])

    # Create audit_logs table
    op.create_table(
        'audit_logs',
        sa.Column('id', postgresql.UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('user_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('action', sa.String(100), nullable=False),
        sa.Column('resource_type', sa.String(50), nullable=True),
        sa.Column('resource_id', postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column('resource_name', sa.String(255), nullable=True),
        sa.Column('details', postgresql.JSON, nullable=True),
        sa.Column('ip_address', postgresql.INET, nullable=True),
        sa.Column('user_agent', sa.Text, nullable=True),
        sa.Column('created_at', sa.DateTime, server_default=sa.func.current_timestamp(), nullable=False),
    )
    op.create_index('idx_audit_logs_tenant_time', 'audit_logs', ['tenant_id', 'created_at'])
    op.create_index('idx_audit_logs_user_time', 'audit_logs', ['user_id', 'created_at'])
    op.create_index('idx_audit_logs_action', 'audit_logs', ['action'])
    op.create_index('idx_audit_logs_resource', 'audit_logs', ['resource_type', 'resource_id'])


def downgrade():
    # Drop audit_logs table
    op.drop_table('audit_logs')

    # Drop usage_records table
    op.drop_table('usage_records')

    # Drop tenant_quotas table
    op.drop_table('tenant_quotas')

    # Drop tenant_users table
    op.drop_table('tenant_users')

    # Drop tenant_profiles table
    op.drop_table('tenant_profiles')

    # Drop enums (only if not used by other tables)
    op.execute('DROP TYPE IF EXISTS tenant_user_status')
    op.execute('DROP TYPE IF EXISTS tenant_user_role')
    op.execute('DROP TYPE IF EXISTS tenant_status')
    op.execute('DROP TYPE IF EXISTS tenant_tier')
