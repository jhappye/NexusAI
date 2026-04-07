# NexusAI 企业级 AI 中台 - 实施计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 将 Dify 改造为 NexusAI 企业级 AI 中台，完成品牌重塑、ToB 功能增强、私有化部署支持

**Architecture:** 基于 Dify 0.x 最新代码进行深度二次开发，采用模块化注入方式，新增多租户、权限、计费、审计模块，保持核心 AI 能力（工作流/RAG/Agent/模型管理）完整兼容

**Tech Stack:** Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui (前端) | Python Flask + SQLAlchemy + Celery (后端) | PostgreSQL 15 + Redis 6 (数据库)

---

## 阶段一：品牌重塑

### 任务 1.1: 前端 Logo 和 Favicon 替换

**Files:**
- Create: `web/public/logo/nexusai-logo.svg`
- Create: `web/public/logo/nexusai-logo-monochrome-white.svg`
- Create: `web/public/logo/nexusai-logo-site.svg`
- Create: `web/public/logo/nexusai-logo-site-dark.png`
- Create: `web/public/favicon.ico`
- Modify: `web/next.config.ts`
- Modify: `web/app/layout.tsx`
- Modify: `web/app/(shared)/layout.tsx`

- [ ] **Step 1: 创建设计规范中的 NexusAI Logo 文件**

创建 SVG 文件（深蓝六边形 + 金色神经元图案）:
```svg
<!-- web/public/logo/nexusai-logo.svg -->
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 200 200">
  <defs>
    <linearGradient id="gold" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:#E5C878"/>
      <stop offset="100%" style="stop-color:#D4A84B"/>
    </linearGradient>
  </defs>
  <!-- 六边形背景 -->
  <path d="M100 10 L180 55 L180 145 L100 190 L20 145 L20 55 Z" fill="#1E3A5F"/>
  <!-- 神经元图案 -->
  <circle cx="100" cy="100" r="30" fill="url(#gold)"/>
  <circle cx="70" cy="70" r="12" fill="#D4A84B"/>
  <circle cx="130" cy="70" r="12" fill="#D4A84B"/>
  <circle cx="70" cy="130" r="12" fill="#D4A84B"/>
  <circle cx="130" cy="130" r="12" fill="#D4A84B"/>
  <line x1="70" y1="70" x2="100" y2="100" stroke="#D4A84B" stroke-width="4"/>
  <line x1="130" y1="70" x2="100" y2="100" stroke="#D4A84B" stroke-width="4"/>
  <line x1="70" y1="130" x2="100" y2="100" stroke="#D4A84B" stroke-width="4"/>
  <line x1="130" y1="130" x2="100" y2="100" stroke="#D4A84B" stroke-width="4"/>
</svg>
```

```bash
# 复制 Logo 到各尺寸变体
cp web/public/logo/nexusai-logo.svg web/public/logo/nexusai-logo-monochrome-white.svg
cp web/public/logo/nexusai-logo.svg web/public/logo/nexusai-logo-site.svg
# 注意：PNG 需要使用图形工具转换，这里先用 SVG 占位
```

- [ ] **Step 2: 更新 next.config.ts 中的 favicon 配置**

```typescript
// web/next.config.ts
import path from 'path'

const nextConfig = {
  // ... existing config
  images: {
    // ... existing images config
  },
}

// favicon 配置（指向新文件）
// 原有: images/icon.svg -> nexusai-favicon.svg

export default nextConfig
```

- [ ] **Step 3: 更新页面布局中的 Logo 引用**

```tsx
// web/app/layout.tsx 或相关布局文件
// 查找并替换所有 Logo 引用路径
// "Dify" -> "NexusAI"
// logo.svg -> nexusai-logo.svg
```

- [ ] **Step 4: 提交变更**

```bash
git add web/public/logo/
git commit -m "feat(brand): add NexusAI logo files"
```

---

### 任务 1.2: 全局文本替换（Dify → NexusAI）

**Files:**
- Modify: `web/package.json`
- Modify: `web/i18n/en-US/*.json` (所有英文翻译文件)
- Modify: `web/i18n/zh-Hans/*.json` (简体中文)
- Modify: `web/i18n/zh-Hant/*.json` (繁体中文)
- Modify: `web/i18n/ja-JP/*.json`, `web/i18n/ko-KR/*.json` 等所有语言

- [ ] **Step 1: 创建品牌替换脚本**

```bash
#!/bin/bash
# scripts/replace-brand.sh - 品牌替换脚本

set -e

echo "开始替换 Dify 品牌标识..."

# 前端文本替换
find web -type f \( -name "*.tsx" -o -name "*.ts" -o -name "*.json" \) -exec sed -i \
  -e 's/Dify/NexusAI/g' \
  -e 's/dify/nexusai/g' \
  -e 's/DIFY/NEXUSAI/g' \
  -e 's/dify\.ai/nexusai.io/g' \
  -e 's/Dify Team/NexusAI Team/g' \
  {} \;

# 后端文本替换
find api -type f \( -name "*.py" -o -name "*.md" -o -name "*.yaml" -o -name "*.yml" \) -exec sed -i \
  -e 's/Dify/NexusAI/g' \
  -e 's/dify/nexusai/g' \
  -e 's/DIFY/NEXUSAI/g' \
  -e 's/dify\.ai/nexusai.io/g' \
  -e 's/Dify Team/NexusAI Team/g' \
  {} \;

echo "品牌替换完成"
```

```bash
chmod +x scripts/replace-brand.sh
./scripts/replace-brand.sh
```

- [ ] **Step 2: 手动检查并修复遗漏的 brand 引用**

```bash
# 检查是否还有遗漏的 dify 引用
grep -ri "dify" web/app/ --include="*.tsx" --include="*.ts" | head -20
grep -ri "dify" api/ --include="*.py" | head -20
```

- [ ] **Step 3: 更新 package.json**

```json
// web/package.json
{
  "name": "nexusai-web",
  "version": "1.0.0",
  "description": "NexusAI Enterprise AI Platform - 企业级 AI 中台",
  // ... 其他配置保持不变
}
```

- [ ] **Step 4: 提交变更**

```bash
git add -A
git commit -m "feat(brand): replace all Dify branding with NexusAI"
```

---

### 任务 1.3: UI 主题色调整（深蓝+金色）

**Files:**
- Modify: `web/tailwind.config.ts`
- Modify: `web/tailwind-common-config.ts`
- Modify: `web/themes/tailwind-theme-var-define.ts`
- Create: `web/themes/nexusai-theme.ts`

- [ ] **Step 1: 更新 Tailwind 主题配置**

```typescript
// web/tailwind.config.ts
import type { Config } from 'tailwindcss'
import tailwindCommonConfig from './tailwind-common-config'

const config: Config = {
  content: [
    // ... existing content
  ],
  theme: {
    extend: {
      colors: {
        // 主色调 - 深海蓝系
        primary: {
          DEFAULT: '#1E3A5F',
          dark: '#152A45',
          light: '#2A4F7F',
          50: '#E8EEF4',
          100: '#D1DEE9',
          200: '#A3BDD3',
          300: '#759CBD',
          400: '#477BA7',
          500: '#1E3A5F',
          600: '#1A3354',
          700: '#162C49',
          800: '#12253E',
          900: '#0D1B2A',
        },
        // 强调色 - 金色系
        accent: {
          DEFAULT: '#D4A84B',
          dark: '#B8923F',
          light: '#E5C878',
          50: '#FDF8ED',
          100: '#FBF0DB',
          200: '#F7E1B7',
          300: '#F3D293',
          400: '#EFC36F',
          500: '#D4A84B',
          600: '#C4963F',
          700: '#A88233',
          800: '#8C6E27',
          900: '#705A1B',
        },
        // 背景色
        background: {
          dark: '#0D1B2A',
          main: '#F8FAFC',
          card: '#FFFFFF',
        },
        // 文字色
        text: {
          primary: '#1A202C',
          secondary: '#64748B',
          inverse: '#F8FAFC',
        },
      },
      fontFamily: {
        heading: ['Inter', 'Noto Sans SC', '-apple-system', 'sans-serif'],
        body: ['Inter', 'Noto Sans SC', '-apple-system', 'sans-serif'],
        mono: ['JetBrains Mono', 'Fira Code', 'monospace'],
      },
    },
  },
  plugins: [
    // ... existing plugins
  ],
}

export default config
```

- [ ] **Step 2: 更新通用主题变量**

```typescript
// web/tailwind-common-config.ts 或 web/themes/tailwind-theme-var-define.ts

export const themeVariables = {
  // 主色调
  '--color-primary': '#1E3A5F',
  '--color-primary-dark': '#152A45',
  '--color-primary-light': '#2A4F7F',

  // 强调色
  '--color-accent': '#D4A84B',
  '--color-accent-dark': '#B8923F',
  '--color-accent-light': '#E5C878',

  // 背景色
  '--color-bg-dark': '#0D1B2A',
  '--color-bg-main': '#F8FAFC',
  '--color-bg-card': '#FFFFFF',

  // 文字色
  '--color-text-primary': '#1A202C',
  '--color-text-secondary': '#64748B',
  '--color-text-inverse': '#F8FAFC',

  // 语义色
  '--color-success': '#2E7D32',
  '--color-warning': '#ED6C02',
  '--color-danger': '#D32F2F',
  '--color-info': '#0288D1',
}
```

- [ ] **Step 3: 更新组件样式（按钮、侧边栏等）**

```typescript
// web/themes/nexusai-theme.ts - 创建新主题配置

export const nexusAITheme = {
  button: {
    primary: {
      backgroundColor: '#D4A84B',
      color: '#0D1B2A',
      hoverBackgroundColor: '#B8923F',
    },
    secondary: {
      borderColor: '#1E3A5F',
      color: '#1E3A5F',
      hoverBackgroundColor: '#1E3A5F',
      hoverColor: '#F8FAFC',
    },
  },
  sidebar: {
    backgroundColor: '#0D1B2A',
    textColor: '#F8FAFC',
    activeItemColor: '#D4A84B',
  },
  card: {
    backgroundColor: '#FFFFFF',
    borderRadius: '8px',
    boxShadow: '0 2px 8px rgba(0, 0, 0, 0.08)',
  },
  input: {
    borderColor: '#E2E8F0',
    focusBorderColor: '#D4A84B',
  },
}
```

- [ ] **Step 4: 提交变更**

```bash
git add web/tailwind.config.ts web/themes/
git commit -m "feat(ui): apply NexusAI deep blue + gold theme"
```

---

### 任务 1.4: 后端品牌替换

**Files:**
- Modify: `api/app_factory.py`
- Modify: `api/app.py`
- Modify: `api/dify_app.py`
- Modify: `api/pyproject.toml`
- Modify: `api/README.md`
- Modify: `api/.env.example`
- Modify: `api/services/account_service.py` (邮件模板)

- [ ] **Step 1: 更新应用工厂**

```python
# api/app_factory.py
import os
from flask import Flask
from werkzeug.utils import import_string

# 应用名称配置
APP_NAME = os.getenv('APP_NAME', 'NexusAI')
API_VERSION = os.getenv('API_VERSION', 'v1')

def create_app(config_name: str = None) -> Flask:
    """创建并配置 NexusAI 应用实例"""
    app = Flask(__name__)

    # 应用配置
    app.config['APP_NAME'] = APP_NAME
    app.config['API_PREFIX'] = f'/api/{API_VERSION}'

    # ... 其他初始化代码保持不变

    return app
```

- [ ] **Step 2: 更新 pyproject.toml**

```toml
# api/pyproject.toml
[project]
name = "nexusai-api"
version = "1.0.0"
description = "NexusAI Enterprise AI Platform API"
readme = "README.md"
license = {text = "Apache-2.0"}

[project.urls]
Homepage = "https://github.com/nexusai/nexusai"
Documentation = "https://docs.nexusai.io"

# ... 其他配置保持不变
```

- [ ] **Step 3: 更新 .env.example**

```bash
# api/.env.example
# 品牌配置
APP_NAME=NexusAI
NEXUSAI_COMPATIBILITY_MODE=true  # 是否启用 Dify 兼容模式

# 域名配置
CONSOLE_WEB_URL=http://localhost:3000
SERVICE_API_URL=http://localhost:8080
APP_WEB_URL=http://localhost:3000
# 等等...
```

- [ ] **Step 4: 提交变更**

```bash
git add api/app_factory.py api/pyproject.toml api/.env.example
git commit -m "feat(brand): update backend branding to NexusAI"
```

---

## 阶段二：多租户架构

### 任务 2.1: 数据库 Schema 设计

**Files:**
- Create: `api/models/tenant.py`
- Create: `api/models/tenant_quota.py`
- Create: `api/models/usage_record.py`
- Create: `api/models/audit_log.py`
- Create: `api/migrations/versions/xxxx_add_tenant_tables.py`

- [ ] **Step 1: 创建租户模型**

```python
# api/models/tenant.py
from datetime import datetime
from typing import Optional
from uuid import uuid4
from sqlalchemy import Column, String, Integer, Enum, DateTime, ForeignKey, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from extensions import db

class Tenant(db.Model):
    """租户模型"""
    __tablename__ = 'tenants'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    name = Column(String(255), nullable=False)
    tier = Column(Enum('basic', 'professional', 'enterprise', name='tenant_tier'),
                  default='basic')
    status = Column(Enum('active', 'suspended', 'trial', name='tenant_status'),
                     default='trial')

    # 资源配额
    quota_users = Column(Integer, default=10)
    quota_apps = Column(Integer, default=20)
    quota_api_calls = Column(Integer, default=100000)

    # 企业版专用
    db_schema = Column(String(63), nullable=True)

    # 时间戳
    expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系
    users = relationship('TenantUser', back_populates='tenant', cascade='all, delete-orphan')
    quotas = relationship('TenantQuota', back_populates='tenant', cascade='all, delete-orphan')
    usage_records = relationship('UsageRecord', back_populates='tenant', cascade='all, delete-orphan')

    def to_dict(self):
        return {
            'id': str(self.id),
            'name': self.name,
            'tier': self.tier,
            'status': self.status,
            'quota_users': self.quota_users,
            'quota_apps': self.quota_apps,
            'quota_api_calls': self.quota_api_calls,
            'expires_at': self.expires_at.isoformat() if self.expires_at else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }


class TenantUser(db.Model):
    """租户用户关联模型"""
    __tablename__ = 'tenant_users'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'),
                        nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'),
                      nullable=False)
    role = Column(Enum('tenant_admin', 'member', name='tenant_user_role'), default='member')
    status = Column(Enum('active', 'inactive', name='tenant_user_status'), default='active')
    created_at = Column(DateTime, default=datetime.utcnow)

    # 关系
    tenant = relationship('Tenant', back_populates='users')
    user = relationship('User', back_populates='tenant_users')

    __table_args__ = (
        db.UniqueConstraint('tenant_id', 'user_id', name='uq_tenant_user'),
    )
```

- [ ] **Step 2: 创建配额和使用记录模型**

```python
# api/models/tenant_quota.py
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from extensions import db

class TenantQuota(db.Model):
    """租户配额模型"""
    __tablename__ = 'tenant_quotas'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'),
                        nullable=False)
    resource_type = Column(String(50), nullable=False)  # 'token', 'api_call', 'storage'
    quota = Column(Integer, nullable=False)
    used = Column(Integer, default=0)
    period = Column(String(7), nullable=False)  # 'YYYY-MM'
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    tenant = relationship('Tenant', back_populates='quotas')

    __table_args__ = (
        UniqueConstraint('tenant_id', 'resource_type', 'period', name='uq_tenant_resource_period'),
    )


# api/models/usage_record.py
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Numeric, Enum
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from extensions import db

class UsageRecord(db.Model):
    """用量记录模型"""
    __tablename__ = 'usage_records'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey('tenants.id', ondelete='CASCADE'),
                        nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    resource_type = Column(String(50), nullable=False)  # 'token_input', 'token_output', 'api_call'
    amount = Column(Integer, nullable=False)
    cost = Column(Numeric(10, 4), default=0)
    period = Column(String(7), nullable=False)  # 'YYYY-MM'
    created_at = Column(DateTime, default=datetime.utcnow)

    tenant = relationship('Tenant', back_populates='usage_records')
```

- [ ] **Step 3: 创建审计日志模型**

```python
# api/models/audit_log.py
from datetime import datetime
from uuid import uuid4
from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Enum, JSON
from sqlalchemy.dialects.postgresql import UUID, INET
from extensions import db

class AuditLog(db.Model):
    """审计日志模型"""
    __tablename__ = 'audit_logs'

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    tenant_id = Column(UUID(as_uuid=True), nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    action = Column(String(100), nullable=False)  # 'app.create', 'user.login'
    resource_type = Column(String(50), nullable=True)  # 'app', 'user', 'workflow'
    resource_id = Column(UUID(as_uuid=True), nullable=True)
    resource_name = Column(String(255), nullable=True)
    details = Column(JSON, nullable=True)  # 额外详情
    ip_address = Column(INET, nullable=True)
    user_agent = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    __table_args__ = (
        db.Index('idx_audit_logs_tenant_time', 'tenant_id', 'created_at'),
    )
```

- [ ] **Step 4: 创建数据库迁移**

```bash
# 使用 Flask-Migrate 生成迁移
cd api
export FLASK_APP=app.py
flask db revision --autogenerate -m "Add tenant tables"
flask db upgrade
```

- [ ] **Step 5: 提交变更**

```bash
git add api/models/tenant.py api/models/tenant_quota.py api/models/usage_record.py api/models/audit_log.py
git add api/migrations/
git commit -m "feat(tenant): add multi-tenant database schema"
```

---

### 任务 2.2: 租户管理服务

**Files:**
- Create: `api/services/tenant_service.py`
- Create: `api/services/auth_service.py`
- Create: `api/middleware/tenant_middleware.py`

- [ ] **Step 1: 创建租户服务**

```python
# api/services/tenant_service.py
from typing import Optional, List
from uuid import UUID
from datetime import datetime, timedelta
from sqlalchemy import and_
from extensions import db
from models.tenant import Tenant, TenantUser
from models.user import User

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
            user = User.query.filter_by(email=admin_email).first()
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
        """检查租户配额是否足够"""
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return False

        quota_map = {
            'users': tenant.quota_users,
            'apps': tenant.quota_apps,
            'api_calls': tenant.quota_api_calls,
        }

        quota = quota_map.get(resource, float('inf'))
        return amount <= quota
```

- [ ] **Step 2: 创建租户中间件**

```python
# api/middleware/tenant_middleware.py
from functools import wraps
from flask import request, g, jsonify
from uuid import UUID
from services.tenant_service import TenantService
from models.tenant import TenantUser

def tenant_required(f):
    """租户验证装饰器"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        # 从请求头或 JWT 获取租户 ID
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
```

- [ ] **Step 3: 创建权限服务**

```python
# api/services/auth_service.py
from typing import Optional, List
from uuid import UUID
from models.user import User
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
    def get_user_role_in_tenant(user_id: UUID, tenant_id: UUID) -> Optional[str]:
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
                from flask import g
                user_id = getattr(g, 'user_id', None)
                tenant_id = getattr(g, 'tenant_id', None)

                if not user_id or not tenant_id:
                    return jsonify({'error': 'Unauthorized'}), 401

                if not AuthService.check_permission(user_id, tenant_id, permission):
                    return jsonify({'error': 'Permission denied'}), 403

                return f(*args, **kwargs)
            return decorated_function
        return decorator
```

- [ ] **Step 4: 提交变更**

```bash
git add api/services/tenant_service.py api/services/auth_service.py
git add api/middleware/tenant_middleware.py
git commit -m "feat(tenant): add tenant service and middleware"
```

---

### 任务 2.3: 租户 API 控制器

**Files:**
- Create: `api/controllers/tenant_controller.py`
- Modify: `api/app_factory.py` (注册新路由)

- [ ] **Step 1: 创建租户控制器**

```python
# api/controllers/tenant_controller.py
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
```

- [ ] **Step 2: 注册租户路由**

```python
# api/app_factory.py 中添加
from controllers.tenant_controller import tenant_bp

def create_app(config_name: str = None) -> Flask:
    app = Flask(__name__)

    # 注册蓝图
    app.register_blueprint(tenant_bp, url_prefix='/api/v1/tenants')

    # ... 其他代码
```

- [ ] **Step 3: 提交变更**

```bash
git add api/controllers/tenant_controller.py api/app_factory.py
git commit -m "feat(tenant): add tenant API endpoints"
```

---

### 任务 2.4: 前端租户管理页面

**Files:**
- Create: `web/app/(main)/tenant/page.tsx`
- Create: `web/app/(main)/tenant/layout.tsx`
- Create: `web/app/(main)/tenant/[id]/page.tsx`
- Create: `web/service/tenant.ts`
- Modify: `web/app/(main)/layout.tsx` (导航菜单)

- [ ] **Step 1: 创建租户服务 API 客户端**

```typescript
// web/service/tenant.ts
import type { Tenant } from '@/types/tenant'
import { fetchApi } from './fetch'

export const tenantService = {
  /**
   * 获取租户列表
   */
  list: async (): Promise<Tenant[]> => {
    return fetchApi('/tenants')
  },

  /**
   * 获取租户详情
   */
  get: async (id: string): Promise<Tenant> => {
    return fetchApi(`/tenants/${id}`)
  },

  /**
   * 创建租户
   */
  create: async (data: Partial<Tenant>): Promise<Tenant> => {
    return fetchApi('/tenants', {
      method: 'POST',
      body: JSON.stringify(data),
    })
  },

  /**
   * 更新租户
   */
  update: async (id: string, data: Partial<Tenant>): Promise<Tenant> => {
    return fetchApi(`/tenants/${id}`, {
      method: 'PUT',
      body: JSON.stringify(data),
    })
  },

  /**
   * 激活租户
   */
  activate: async (id: string): Promise<Tenant> => {
    return fetchApi(`/tenants/${id}/activate`, {
      method: 'POST',
    })
  },

  /**
   * 暂停租户
   */
  suspend: async (id: string): Promise<Tenant> => {
    return fetchApi(`/tenants/${id}/suspend`, {
      method: 'POST',
    })
  },

  /**
   * 获取租户用户
   */
  getUsers: async (id: string) => {
    return fetchApi(`/tenants/${id}/users`)
  },

  /**
   * 移除租户用户
   */
  removeUser: async (tenantId: string, userId: string) => {
    return fetchApi(`/tenants/${tenantId}/users/${userId}`, {
      method: 'DELETE',
    })
  },
}
```

- [ ] **Step 2: 创建租户类型定义**

```typescript
// web/types/tenant.ts
export type TenantTier = 'basic' | 'professional' | 'enterprise'
export type TenantStatus = 'active' | 'suspended' | 'trial'

export interface Tenant {
  id: string
  name: string
  tier: TenantTier
  status: TenantStatus
  quota_users: number
  quota_apps: number
  quota_api_calls: number
  expires_at: string | null
  created_at: string
  updated_at: string
}

export interface TenantUser {
  id: string
  user_id: string
  role: 'tenant_admin' | 'member'
  status: 'active' | 'inactive'
  created_at: string
}
```

- [ ] **Step 3: 创建租户列表页面**

```tsx
// web/app/(main)/tenant/page.tsx
'use client'

import { useState, useEffect } from 'react'
import { tenantService } from '@/service/tenant'
import type { Tenant } from '@/types/tenant'
import { Button } from '@/components/ui/button'
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from '@/components/ui/table'

export default function TenantListPage() {
  const [tenants, setTenants] = useState<Tenant[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    loadTenants()
  }, [])

  const loadTenants = async () => {
    try {
      const data = await tenantService.list()
      setTenants(data)
    } catch (error) {
      console.error('Failed to load tenants:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleActivate = async (id: string) => {
    try {
      await tenantService.activate(id)
      loadTenants()
    } catch (error) {
      console.error('Failed to activate tenant:', error)
    }
  }

  const handleSuspend = async (id: string) => {
    try {
      await tenantService.suspend(id)
      loadTenants()
    } catch (error) {
      console.error('Failed to suspend tenant:', error)
    }
  }

  const getStatusBadgeColor = (status: Tenant['status']) => {
    switch (status) {
      case 'active':
        return 'bg-green-100 text-green-800'
      case 'suspended':
        return 'bg-red-100 text-red-800'
      case 'trial':
        return 'bg-yellow-100 text-yellow-800'
    }
  }

  if (loading) {
    return <div>加载中...</div>
  }

  return (
    <div className="container mx-auto py-8">
      <div className="flex justify-between items-center mb-6">
        <h1 className="text-2xl font-bold text-gray-900">租户管理</h1>
        <Button className="bg-accent hover:bg-accent-dark text-background">
          创建租户
        </Button>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>租户列表</CardTitle>
        </CardHeader>
        <CardContent>
          <Table>
            <TableHeader>
              <TableRow>
                <TableHead>名称</TableHead>
                <TableHead>等级</TableHead>
                <TableHead>状态</TableHead>
                <TableHead>用户配额</TableHead>
                <TableHead>应用配额</TableHead>
                <TableHead>API配额</TableHead>
                <TableHead>到期时间</TableHead>
                <TableHead>操作</TableHead>
              </TableRow>
            </TableHeader>
            <TableBody>
              {tenants.map((tenant) => (
                <TableRow key={tenant.id}>
                  <TableCell className="font-medium">{tenant.name}</TableCell>
                  <TableCell>
                    <span className="px-2 py-1 rounded text-xs bg-primary text-white">
                      {tenant.tier}
                    </span>
                  </TableCell>
                  <TableCell>
                    <span className={`px-2 py-1 rounded text-xs ${getStatusBadgeColor(tenant.status)}`}>
                      {tenant.status}
                    </span>
                  </TableCell>
                  <TableCell>{tenant.quota_users}</TableCell>
                  <TableCell>{tenant.quota_apps}</TableCell>
                  <TableCell>{tenant.quota_api_calls.toLocaleString()}</TableCell>
                  <TableCell>
                    {tenant.expires_at
                      ? new Date(tenant.expires_at).toLocaleDateString()
                      : '-'}
                  </TableCell>
                  <TableCell>
                    <div className="flex gap-2">
                      {tenant.status === 'trial' && (
                        <Button
                          size="sm"
                          variant="outline"
                          onClick={() => handleActivate(tenant.id)}
                        >
                          激活
                        </Button>
                      )}
                      {tenant.status === 'active' && (
                        <Button
                          size="sm"
                          variant="destructive"
                          onClick={() => handleSuspend(tenant.id)}
                        >
                          暂停
                        </Button>
                      )}
                      <Button size="sm" variant="ghost">
                        编辑
                      </Button>
                    </div>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </CardContent>
      </Card>
    </div>
  )
}
```

- [ ] **Step 4: 提交变更**

```bash
git add web/service/tenant.ts web/types/tenant.ts web/app/\(main\)/tenant/
git commit -m "feat(tenant): add tenant management frontend pages"
```

---

## 阶段三：计费与用量统计

### 任务 3.1: 计费服务

**Files:**
- Create: `api/services/billing_service.py`
- Create: `api/controllers/billing_controller.py`

- [ ] **Step 1: 创建计费服务**

```python
# api/services/billing_service.py
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
        return Decimal(amount) * rate / 1000 if 'token' in resource_type else Decimal(amount) * rate

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
        from models.account import Account
        tenant = Tenant.query.get(tenant_id)
        if not tenant:
            return False

        current_usage = BillingService.get_tenant_usage(tenant_id)
        monthly_budget = getattr(tenant, 'monthly_budget', None)

        if not monthly_budget:
            return False

        return current_usage['total_cost'] >= monthly_budget
```

- [ ] **Step 2: 创建计费控制器**

```python
# api/controllers/billing_controller.py
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
```

- [ ] **Step 3: 提交变更**

```bash
git add api/services/billing_service.py api/controllers/billing_controller.py
git commit -m "feat(billing): add billing and usage tracking service"
```

---

### 任务 3.2: 审计日志服务

**Files:**
- Create: `api/services/audit_service.py`
- Create: `api/controllers/audit_controller.py`

- [ ] **Step 1: 创建审计日志服务**

```python
# api/services/audit_service.py
from datetime import datetime
from typing import Optional, Dict, List
from uuid import UUID
from flask import request
from sqlalchemy import and_, desc
from extensions import db
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
            from flask import request
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
```

- [ ] **Step 2: 创建审计控制器**

```python
# api/controllers/audit_controller.py
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
```

- [ ] **Step 3: 提交变更**

```bash
git add api/services/audit_service.py api/controllers/audit_controller.py
git commit -m "feat(audit): add audit logging service"
```

---

## 阶段四：私有化部署支持

### 任务 4.1: Docker Compose 优化

**Files:**
- Modify: `docker/docker-compose.yaml`
- Create: `docker/docker-compose-simple.yaml`
- Modify: `docker/.env.example`

- [ ] **Step 1: 更新 docker-compose.yaml**

```yaml
# docker/docker-compose.yaml
version: '3.8'

services:
  # NexusAI Web 前端
  nexusai-web:
    image: nexusai/web:${NEXUSAI_WEB_VERSION:-latest}
    restart: unless-stopped
    ports:
      - "${CONSOLE_WEB_PORT:-3000}:3000"
    environment:
      - APP_API_URL=${APP_API_URL:-http://nexusai-api:8080}
      - SENTRY_DSN=${SENTRY_DSN}
    networks:
      - nexusai-network
    depends_on:
      - nexusai-api

  # NexusAI API 后端
  nexusai-api:
    image: nexusai/api:${NEXUSAI_API_VERSION:-latest}
    restart: unless-stopped
    ports:
      - "${API_PORT:-8080}:8080"
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_USERNAME=${DB_USERNAME}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_DATABASE=${DB_DATABASE}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
      - WEAVIATE_URL=http://weaviate:8080
      - APP_NAME=NexusAI
    networks:
      - nexusai-network
    depends_on:
      - postgres
      - redis
      - weaviate
    volumes:
      - ./volumes/api:/app/api/storage

  # NexusAI Worker
  nexusai-worker:
    image: nexusai/api:${NEXUSAI_API_VERSION:-latest}
    restart: unless-stopped
    command: celery worker -A celery_app.app --loglevel=info
    environment:
      - DB_HOST=postgres
      - DB_PORT=5432
      - DB_USERNAME=${DB_USERNAME}
      - DB_PASSWORD=${DB_PASSWORD}
      - DB_DATABASE=${DB_DATABASE}
      - REDIS_HOST=redis
      - REDIS_PORT=6379
    networks:
      - nexusai-network
    depends_on:
      - postgres
      - redis

  # PostgreSQL 数据库
  postgres:
    image: postgres:15-alpine
    restart: unless-stopped
    ports:
      - "${DB_EXTERNAL_PORT:-5432}:5432"
    environment:
      - POSTGRES_DB=${DB_DATABASE}
      - POSTGRES_USER=${DB_USERNAME}
      - POSTGRES_PASSWORD=${DB_PASSWORD}
    volumes:
      - postgres-data:/var/lib/postgresql/data
    networks:
      - nexusai-network

  # Redis 缓存
  redis:
    image: redis:6-alpine
    restart: unless-stopped
    ports:
      - "${REDIS_EXTERNAL_PORT:-6379}:6379"
    volumes:
      - redis-data:/data
    networks:
      - nexusai-network

  # Weaviate 向量数据库
  weaviate:
    image: cr.weaviate.io/semitechnics/weaviate:latest
    restart: unless-stopped
    ports:
      - "${WEAVIATE_PORT:-8080}:8080"
    environment:
      - QUERY_DEFAULTS_LIMIT=25
      - AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true
      - PERSISTENCE_DATA_PATH=/var/lib/weaviate
      - ENABLE_MODULES=text2vec-transformers
    volumes:
      - weaviate-data:/var/lib/weaviate
    networks:
      - nexusai-network

networks:
  nexusai-network:
    driver: bridge

volumes:
  postgres-data:
  redis-data:
  weaviate-data:
```

- [ ] **Step 2: 更新 .env.example**

```bash
# docker/.env.example

# ===================
# NexusAI 配置
# ===================
APP_NAME=NexusAI
NEXUSAI_COMPATIBILITY_MODE=true

# ===================
# 版本配置
# ===================
NEXUSAI_WEB_VERSION=latest
NEXUSAI_API_VERSION=latest

# ===================
# 端口配置
# ===================
CONSOLE_WEB_PORT=3000
API_PORT=8080
DB_EXTERNAL_PORT=5432
REDIS_EXTERNAL_PORT=6379
WEAVIATE_PORT=8080

# ===================
# 数据库配置
# ===================
DB_DATABASE=nexusai
DB_USERNAME=nexusai
DB_PASSWORD=your_secure_password_here

# ===================
# Redis 配置
# ===================
# REDIS_HOST=redis
# REDIS_PORT=6379

# ===================
# 可选：第三方服务
# ===================
# SENTRY_DSN=
```

- [ ] **Step 3: 提交变更**

```bash
git add docker/docker-compose.yaml docker/.env.example
git commit -m "feat(deploy): update Docker configuration for NexusAI"
```

---

### 任务 4.2: 部署脚本

**Files:**
- Create: `scripts/deploy.sh`
- Create: `scripts/health-check.sh`
- Create: `scripts/backup.sh`

- [ ] **Step 1: 创建一键部署脚本**

```bash
#!/bin/bash
# scripts/deploy.sh - NexusAI 私有化部署脚本

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查 Docker
check_docker() {
    log_info "检查 Docker 环境..."
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    if ! command -v docker compose &> /dev/null && ! docker compose version &> /dev/null; then
        log_error "Docker Compose 未安装"
        exit 1
    fi
    log_info "Docker 环境检查通过"
}

# 加载环境配置
load_env() {
    log_info "加载环境配置..."
    if [ -f docker/.env ]; then
        export $(grep -v '^#' docker/.env | xargs)
        log_info "已加载 .env 配置"
    else
        log_warn ".env 文件不存在，使用默认配置"
    fi
}

# 初始化数据库
init_database() {
    log_info "检查数据库连接..."
    # 等待 PostgreSQL 就绪
    local max_attempts=30
    local attempt=1
    while [ $attempt -le $max_attempts ]; do
        if docker compose exec -T postgres pg_isready -U ${DB_USERNAME:-nexusai} &> /dev/null; then
            log_info "数据库已就绪"
            return 0
        fi
        log_info "等待数据库启动... ($attempt/$max_attempts)"
        attempt=$((attempt + 1))
        sleep 2
    done
    log_error "数据库启动超时"
    return 1
}

# 启动服务
start_services() {
    log_info "启动 NexusAI 服务..."
    docker compose up -d
    log_info "服务启动完成"
}

# 健康检查
health_check() {
    log_info "执行健康检查..."

    local max_attempts=60
    local attempt=1

    # 检查 Web
    while [ $attempt -le $max_attempts ]; do
        if curl -sf http://localhost:${CONSOLE_WEB_PORT:-3000}/api/healthy &> /dev/null; then
            log_info "Web 服务健康检查通过"
            break
        fi
        log_info "等待 Web 服务... ($attempt/$max_attempts)"
        attempt=$((attempt + 1))
        sleep 2
    done

    if [ $attempt -gt $max_attempts ]; then
        log_error "Web 服务健康检查失败"
        return 1
    fi

    log_info "所有服务健康检查通过"
}

# 主函数
main() {
    echo "=========================================="
    echo "     NexusAI 企业级 AI 中台部署脚本"
    echo "=========================================="
    echo ""

    check_docker
    load_env
    start_services
    health_check

    echo ""
    echo "=========================================="
    log_info "NexusAI 部署完成！"
    echo "=========================================="
    echo ""
    echo "访问地址: http://localhost:${CONSOLE_WEB_PORT:-3000}"
    echo "API 地址: http://localhost:${API_PORT:-8080}"
    echo ""
}

main "$@"
```

- [ ] **Step 2: 创建健康检查脚本**

```bash
#!/bin/bash
# scripts/health-check.sh - 健康检查脚本

set -e

# 配置
WEB_URL=${CONSOLE_WEB_PORT:-3000}
API_URL=${API_PORT:-8080}

check_service() {
    local name=$1
    local url=$2

    if curl -sf "$url" > /dev/null 2>&1; then
        echo "[OK] $name"
        return 0
    else
        echo "[FAIL] $name"
        return 1
    fi
}

echo "执行 NexusAI 健康检查..."
echo ""

failed=0

check_service "Web UI" "http://localhost:$WEB_URL" || ((failed++))
check_service "API" "http://localhost:$API_URL/health" || ((failed++))

# 检查 Docker 容器状态
echo ""
echo "容器状态:"
docker compose ps --format "table {{.Name}}\t{{.Status}}" | grep nexusai || true

if [ $failed -gt 0 ]; then
    echo ""
    echo "健康检查失败: $failed 项"
    exit 1
else
    echo ""
    echo "所有检查通过"
    exit 0
fi
```

- [ ] **Step 3: 提交变更**

```bash
chmod +x scripts/deploy.sh scripts/health-check.sh
git add scripts/deploy.sh scripts/health-check.sh
git commit -m "feat(deploy): add deployment scripts"
```

---

## 实施检查清单

### 品牌重塑
- [ ] Logo 和 Favicon 已替换
- [ ] 全局文本已替换（Dify → NexusAI）
- [ ] Tailwind 主题色已更新（深蓝+金色）
- [ ] 后端品牌标识已替换

### 多租户架构
- [ ] 租户数据库表已创建
- [ ] 租户服务已实现
- [ ] 租户中间件已实现
- [ ] 租户 API 控制器已实现
- [ ] 前端租户管理页面已实现

### 权限体系
- [ ] RBAC 权限模型已实现
- [ ] 权限服务已实现
- [ ] 权限中间件已实现

### 计费与审计
- [ ] 计费服务已实现
- [ ] 用量记录功能已实现
- [ ] 审计日志服务已实现
- [ ] 审计日志 API 已实现

### 私有化部署
- [ ] Docker Compose 配置已更新
- [ ] 部署脚本已创建
- [ ] 健康检查脚本已创建

---

## 文档

**文件路径**: `/root/NexusAI/docs/superpowers/plans/2026-04-07-nexusai-implementation.md`

**Spec 参考**: `/root/NexusAI/docs/superpowers/specs/2026-04-07-nexusai-design.md`

---

**计划状态**: 已完成，待执行

**执行选项**:

**1. Subagent-Driven (推荐)** - 每个任务由独立的 subagent 执行，任务间有审查节点，快速迭代

**2. Inline Execution** - 在当前 session 中使用 executing-plans 批量执行任务，带审查节点

请选择执行方式。
