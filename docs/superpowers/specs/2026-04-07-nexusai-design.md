# NexusAI 企业级 AI 中台设计方案

**版本**: v1.0
**日期**: 2026-04-07
**项目**: Dify → NexusAI 企业级改造
**目标客户**: 传统企业/政务（私有化部署优先）

---

## 1. 概述

NexusAI 是基于 Dify 深度二次开发的企业级 AI 中台平台，代号 "Nexus" 寓意"连接"与"智能中枢"。

### 1.1 核心改造目标

1. **品牌重塑**: 完全去除 Dify 品牌标识，替换为 NexusAI
2. **视觉升级**: 深蓝+金色企业级 UI 风格
3. **ToB 功能**: 多租户管理、企业权限、计费用量、私有化部署
4. **能力保留**: 工作流编排、RAG 知识库、Agent、模型管理

### 1.2 技术栈

| 层级 | 技术选型 |
|------|---------|
| 前端 | Next.js 14 + TypeScript + Tailwind CSS + shadcn/ui |
| 后端 | Python Flask + SQLAlchemy + Celery |
| 数据库 | PostgreSQL 15 + Redis 6 + Weaviate/Qdrant |
| 部署 | Docker Compose（极简部署） |

---

## 2. 架构设计

### 2.1 整体架构

```
┌─────────────────────────────────────────────────────────────┐
│                      NexusAI Platform                        │
├─────────────┬─────────────┬─────────────┬─────────────────┤
│   工作流编排  │   RAG 知识库   │    Agent     │    模型管理      │
├─────────────┴─────────────┴─────────────┴─────────────────┤
│                     核心能力层（增强保留）                     │
├─────────────┬─────────────┬─────────────┬─────────────────┤
│  多租户管理   │  企业权限体系  │  计费用量统计  │  私有化部署支持   │
├─────────────┴─────────────┴─────────────┴─────────────────┤
│                     ToB 增强功能层                            │
├─────────────────────────────────────────────────────────────┤
│              Flask API + SQLAlchemy + Celery                │
├─────────────────────────────────────────────────────────────┤
│         PostgreSQL  │  Redis  │  Weaviate/Qdrant           │
└─────────────────────────────────────────────────────────────┘
```

### 2.2 多租户隔离策略（混合模式）

| 租户等级 | 隔离级别 | 适用场景 |
|---------|---------|---------|
| 基础版 | 逻辑隔离（tenant_id） | 小规模团队 |
| 专业版 | Schema 隔离 | 中型企业 |
| 企业版 | 独立数据库 | 金融/政务高安全需求 |

**数据库 Schema 设计**:
```sql
-- 租户表
CREATE TABLE tenants (
    id UUID PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    tier ENUM('basic', 'professional', 'enterprise') DEFAULT 'basic',
    quota_users INT DEFAULT 10,
    quota_apps INT DEFAULT 20,
    quota_api_calls INT DEFAULT 100000,
    db_schema VARCHAR(63),  -- 企业版专用 schema
    status ENUM('active', 'suspended', 'trial') DEFAULT 'trial',
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 租户下用户表
CREATE TABLE tenant_users (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    email VARCHAR(255) NOT NULL,
    role ENUM('tenant_admin', 'member') DEFAULT 'member',
    status ENUM('active', 'inactive') DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

---

## 3. 品牌重塑清单

### 3.1 标识替换

| 原 Dify 标识 | 替换方案 | 文件位置 |
|-------------|---------|---------|
| Logo (蜜蜂图形) | NexusAI Logo (六边形+神经元) | web/public/logo.svg |
| "Dify" 文字 | "NexusAI" 全局替换 | 所有文件 |
| dify.ai 域名引用 | nexusai.io (可配置) | .env, 配置文件 |
| 版权 "Dify Team" | "NexusAI Team" | footer, LICENSE |
| @dify.ai 邮箱 | @nexusai.io | 代码中所有邮箱 |

### 3.2 前端品牌替换

**文件清单** (`web/` 目录):
- `public/logo.svg` → 新 Logo
- `public/favicon.ico` → 新 favicon
- `app/(shared)/layout.tsx` → 页脚版权
- `i18n/` → 所有国际化文件中的 "Dify" → "NexusAI"
- `package.json` → name: "nexusai-web"
- `next.config.ts` → 配置中的域名

**替换规则**:
```typescript
// 全局文本替换
"Dify" → "NexusAI"
"dify.ai" → "nexusai.io"
"Dify Team" → "NexusAI Team"
"dify" → "nexusai"
```

### 3.3 后端品牌替换

**文件清单** (`api/` 目录):
- `app.py` / `app_factory.py` → 应用名称
- `services/account_service.py` → 邮件模板
- `controllers/` → API 响应中的产品名
- `pyproject.toml` → name: "nexusai-api"
- `.env.example` → CONSOLE_WEB_URL 等配置

---

## 4. UI 设计规范

### 4.1 配色系统

```css
:root {
  /* 主色调 - 深海蓝系 */
  --color-primary: #1E3A5F;        /* 专业蓝 */
  --color-primary-dark: #152A45;  /* 深蓝 */
  --color-primary-light: #2A4F7F;  /* 亮蓝 */

  /* 强调色 - 金色系 */
  --color-accent: #D4A84B;         /* 金色 */
  --color-accent-dark: #B8923F;    /* 深金 */
  --color-accent-light: #E5C878;   /* 浅金 */

  /* 背景色 */
  --color-bg-dark: #0D1B2A;        /* 午夜蓝（侧边栏） */
  --color-bg-main: #F8FAFC;        /* 浅灰白（主背景） */
  --color-bg-card: #FFFFFF;        /* 卡片白 */

  /* 文字色 */
  --color-text-primary: #1A202C;   /* 主文字 */
  --color-text-secondary: #64748B; /* 次要文字 */
  --color-text-inverse: #F8FAFC;   /* 反色文字 */

  /* 语义色 */
  --color-success: #2E7D32;
  --color-warning: #ED6C02;
  --color-danger: #D32F2F;
  --color-info: #0288D1;
}
```

### 4.2 字体系统

```css
/* 标题字体 */
--font-heading: 'Inter', 'Noto Sans SC', -apple-system, sans-serif;

/* 正文字体 */
--font-body: 'Inter', 'Noto Sans SC', -apple-system, sans-serif;

/* 等宽字体（代码） */
--font-mono: 'JetBrains Mono', 'Fira Code', monospace;

/* 字号阶梯 */
--text-xs: 0.75rem;    /* 12px */
--text-sm: 0.875rem;   /* 14px */
--text-base: 1rem;     /* 16px */
--text-lg: 1.125rem;   /* 18px */
--text-xl: 1.25rem;    /* 20px */
--text-2xl: 1.5rem;    /* 24px */
--text-3xl: 1.875rem;  /* 30px */
```

### 4.3 组件风格

| 组件 | 风格规范 |
|-----|---------|
| 按钮 Primary | 背景 #D4A84B, 文字 #0D1B2A, hover 加深 10% |
| 按钮 Secondary | 边框 #1E3A5F, 文字 #1E3A5F, hover 填充 |
| 侧边栏 | 背景 #0D1B2A, 文字 #F8FAFC, 选中项 #D4A84B |
| 卡片 | 白色背景, 圆角 8px, 阴影 0 2px 8px rgba(0,0,0,0.08) |
| 输入框 | 边框 #E2E8F0, focus 边框 #D4A84B |
| 表格 | 表头 #F1F5F9, 斑马纹 #FAFBFC |

### 4.4 Logo 设计

```
NexusAI Logo 概念：
- 形状：六边形（象征企业级、稳定）
- 内部：抽象神经元图案（象征 AI）
- 颜色：主色 #1E3A5F, 强调色 #D4A84B
- 字体：Inter Bold "NexusAI"
```

---

## 5. 功能模块详细设计

### 5.1 多租户管理模块

**模块路径**: `api/services/tenant_service.py`, `web/app/(main)/tenant/`

**功能清单**:
| 功能 | 描述 |
|-----|------|
| 租户注册 | 企业信息提交，基础信息录入 |
| 租户审批 | 系统管理员审批新租户（可选自动审批） |
| 租户等级管理 | 基础版/专业版/企业版切换 |
| 资源配额管理 | 用户数/应用数/API调用量配额 |
| 租户状态管理 | 激活/暂停/试用状态 |

**API 端点**:
```
POST   /api/tenants              # 创建租户
GET    /api/tenants              # 租户列表（系统管理员）
GET    /api/tenants/:id          # 租户详情
PUT    /api/tenants/:id          # 更新租户
DELETE /api/tenants/:id          # 删除租户
POST   /api/tenants/:id/activate # 激活租户
POST   /api/tenants/:id/suspend  # 暂停租户
```

### 5.2 企业权限体系

**模块路径**: `api/services/auth_service.py`, `web/app/(main)/admin/`

**角色定义**:
| 角色 | 范围 | 权限 |
|-----|------|-----|
| 系统管理员 | 全局 | 所有租户管理、系统配置 |
| 租户管理员 | 租户内 | 用户管理、应用管理、设置 |
| 普通用户 | 租户内 | 创建/使用自己的应用 |

**权限矩阵**:
```python
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
```

### 5.3 计费与用量统计

**模块路径**: `api/services/billing_service.py`, `web/app/(main)/billing/`

**计费模型**:
```python
# Token 计费（兼容 OpenAI 格式）
billing_rules = {
    'token_input': 0.001,   # 元/1K input tokens
    'token_output': 0.002,  # 元/1K output tokens
    'api_call': 0.01,       # 元/次 API 调用
}

# 租户配额检查
def check_quota(tenant_id: str, resource: str, amount: int) -> bool:
    tenant = get_tenant(tenant_id)
    quota = get_quota(tenant, resource)
    usage = get_usage(tenant_id, resource)
    return (usage + amount) <= quota
```

**用量统计表**:
```sql
CREATE TABLE usage_records (
    id UUID PRIMARY KEY,
    tenant_id UUID REFERENCES tenants(id),
    user_id UUID,
    resource_type ENUM('token', 'api_call', 'storage'),
    amount INT NOT NULL,
    cost DECIMAL(10, 4),
    period VARCHAR(7),  -- YYYY-MM
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**前端页面**:
- 用量仪表板：饼图展示各应用用量占比
- 月度报表：柱状图展示趋势
- 预算告警：设置阈值，超限通知

### 5.4 审计日志

**模块路径**: `api/services/audit_service.py`, `web/app/(main)/audit/`

**日志格式**:
```python
audit_log = {
    'tenant_id': 'uuid',
    'user_id': 'uuid',
    'action': 'app.create',        # 资源.操作
    'resource_id': 'uuid',
    'resource_name': 'My App',
    'ip_address': '192.168.1.1',
    'user_agent': 'Mozilla/5.0...',
    'details': {'model': 'gpt-4'},
    'timestamp': '2026-04-07T12:00:00Z'
}
```

**记录的操作**:
- 用户管理：创建/更新/删除/登录
- 应用管理：创建/更新/删除/发布
- 知识库：上传/删除/修改
- 租户管理：配额变更/状态变更

### 5.5 私有化部署支持

**模块路径**: `docker/`, `scripts/deploy/`

**部署架构**（Docker Compose）:
```yaml
# docker-compose.yml
services:
  nexusai-web:
    image: nexusai/web:latest
    ports:
      - "3000:3000"

  nexusai-api:
    image: nexusai/api:latest
    ports:
      - "8080:8080"
    environment:
      - DB_HOST=postgres
      - REDIS_HOST=redis

  nexusai-worker:
    image: nexusai/api:latest
    command: celery worker

  postgres:
    image: postgres:15

  redis:
    image: redis:6

  weaviate:
    image: cr.weaviate.io/semitechnics/weaviate:latest
```

**部署脚本**:
```bash
#!/bin/bash
# deploy.sh - 一键部署脚本

set -e

echo "=== NexusAI 私有化部署 ==="

# 检查 Docker
check_docker

# 加载环境配置
load_env

# 初始化数据库
init_database

# 启动服务
docker compose up -d

# 健康检查
health_check

echo "=== 部署完成 ==="
echo "访问地址: http://localhost:3000"
```

---

## 6. 数据库迁移

### 6.1 新增表

```sql
-- 租户表
CREATE TABLE tenants (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    tier VARCHAR(50) DEFAULT 'basic',
    quota_users INT DEFAULT 10,
    quota_apps INT DEFAULT 20,
    quota_api_calls INT DEFAULT 100000,
    db_schema VARCHAR(63),
    status VARCHAR(50) DEFAULT 'trial',
    expires_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 租户用户关联表
CREATE TABLE tenant_users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    role VARCHAR(50) DEFAULT 'member',
    status VARCHAR(50) DEFAULT 'active',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tenant_id, user_id)
);

-- 用量记录表
CREATE TABLE usage_records (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    user_id UUID,
    resource_type VARCHAR(50) NOT NULL,
    amount INT NOT NULL,
    cost DECIMAL(10, 4),
    period VARCHAR(7),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 审计日志表
CREATE TABLE audit_logs (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID,
    user_id UUID,
    action VARCHAR(100) NOT NULL,
    resource_type VARCHAR(50),
    resource_id UUID,
    details JSONB,
    ip_address INET,
    user_agent TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 租户配额表
CREATE TABLE tenant_quotas (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    tenant_id UUID REFERENCES tenants(id) ON DELETE CASCADE,
    resource_type VARCHAR(50) NOT NULL,
    quota INT NOT NULL,
    used INT DEFAULT 0,
    period VARCHAR(7),
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(tenant_id, resource_type, period)
);
```

### 6.2 索引策略

```sql
-- 租户查询优化
CREATE INDEX idx_tenant_users_tenant_id ON tenant_users(tenant_id);
CREATE INDEX idx_usage_records_tenant_period ON usage_records(tenant_id, period);
CREATE INDEX idx_audit_logs_tenant_time ON audit_logs(tenant_id, created_at);
CREATE INDEX idx_tenants_status ON tenants(status);
```

---

## 7. API 兼容性策略

为保证现有 Dify 用户平滑迁移，API 层面采用以下策略：

### 7.1 向后兼容

```python
# 兼容旧路由（可选配置）
COMPATIBILITY_MODE = os.getenv('NEXUSAI_COMPATIBILITY_MODE', 'true')

if COMPATIBILITY_MODE:
    # 注册 Dify 兼容路由
    @app.route('/api/dify/v1/<path:subpath>')
    def dify_compat_route(subpath):
        # 重定向到新路由
        return redirect(f'/api/nexusai/v1/{subpath}')
```

### 7.2 响应格式

```json
{
  "code": 0,
  "message": "success",
  "data": { ... },
  "meta": {
    "tenant_id": "uuid",
    "request_id": "uuid"
  }
}
```

---

## 8. 实施计划

### Phase 1: 品牌重塑（第 1-2 周）

| 任务 | 工作量 | 优先级 |
|-----|-------|-------|
| 前端 Logo 和 favicon 替换 | 1天 | P0 |
| 全局文本替换（Dify → NexusAI） | 2天 | P0 |
| UI 主题色调整（深蓝+金色） | 3天 | P0 |
| 版权信息和元数据更新 | 1天 | P1 |
| 国际化文件更新 | 2天 | P1 |

### Phase 2: 多租户架构（第 2-3 周）

| 任务 | 工作量 | 优先级 |
|-----|-------|-------|
| 数据库 schema 设计 | 2天 | P0 |
| 租户管理 CRUD API | 3天 | P0 |
| 租户隔离中间件 | 2天 | P0 |
| 租户管理前端页面 | 3天 | P1 |

### Phase 3: 权限体系（第 3-4 周）

| 任务 | 工作量 | 优先级 |
|-----|-------|-------|
| RBAC 权限模型设计 | 2天 | P0 |
| 权限服务开发 | 3天 | P0 |
| 部门/团队管理 | 2天 | P1 |
| 权限管理前端 | 3天 | P1 |

### Phase 4: 计费与审计（第 4-5 周）

| 任务 | 工作量 | 优先级 |
|-----|-------|-------|
| 用量统计服务 | 3天 | P0 |
| 计费规则配置 | 2天 | P0 |
| 审计日志服务 | 2天 | P1 |
| 用量仪表板前端 | 3天 | P1 |

### Phase 5: 私有化部署（第 5-6 周）

| 任务 | 工作量 | 优先级 |
|-----|-------|-------|
| Docker Compose 优化 | 2天 | P0 |
| 部署脚本开发 | 2天 | P0 |
| 健康检查脚本 | 1天 | P1 |
| 部署文档编写 | 2天 | P1 |

---

## 9. 文件变更清单

### 9.1 前端变更（web/）

| 文件 | 变更类型 | 说明 |
|-----|---------|-----|
| `public/logo.svg` | 替换 | 新 Logo |
| `public/favicon.ico` | 替换 | 新 favicon |
| `package.json` | 修改 | name → nexusai-web |
| `tailwind.config.ts` | 修改 | 添加深蓝+金色主题 |
| `app/layout.tsx` | 修改 | 应用名称、版权 |
| `i18n/**/*.json` | 修改 | 品牌文案替换 |
| `app/**/page.tsx` | 检查 | 品牌标识检查 |

### 9.2 后端变更（api/）

| 文件 | 变更类型 | 说明 |
|-----|---------|-----|
| `app_factory.py` | 修改 | 应用名称 |
| `pyproject.toml` | 修改 | name → nexusai-api |
| `services/tenant_service.py` | 新增 | 租户管理服务 |
| `services/billing_service.py` | 新增 | 计费服务 |
| `services/audit_service.py` | 新增 | 审计日志服务 |
| `models/tenant.py` | 新增 | 租户模型 |
| `controllers/tenant_controller.py` | 新增 | 租户 API |
| `middleware/tenant_middleware.py` | 新增 | 租户隔离中间件 |
| `migrations/` | 新增 | 租户相关迁移 |

### 9.3 部署文件变更

| 文件 | 变更类型 | 说明 |
|-----|---------|-----|
| `docker/docker-compose.yaml` | 修改 | 服务名更新 |
| `docker/.env.example` | 修改 | 配置项说明 |
| `scripts/deploy.sh` | 新增 | 一键部署脚本 |

---

## 10. 风险与缓解

| 风险 | 影响 | 缓解措施 |
|-----|-----|---------|
| Dify 升级同步困难 | 中 | 保持核心模块解耦，使用补丁方式同步 |
| 多租户隔离不完整 | 高 | 严格的中间件检查，CI/CD 自动化测试 |
| 性能下降（租户查询） | 中 | 数据库索引优化，缓存层 |
| 品牌替换遗漏 | 中 | 自动化脚本扫描 + 代码审查清单 |

---

## 11. 验收标准

### 11.1 品牌重塑

- [ ] 前端无任何 "Dify" 或 "dify" 字样
- [ ] 后端 API 响应中无 Dify 品牌标识
- [ ] Logo、favicon 全部替换
- [ ] 版权信息更新为 NexusAI Team

### 11.2 功能验收

- [ ] 租户创建、审批、上线流程完整
- [ ] 三级权限（系统管理员/租户管理员/用户）正常工作
- [ ] 用量统计精确到应用级别
- [ ] 审计日志记录所有关键操作
- [ ] Docker Compose 一键部署成功

### 11.3 兼容性验收

- [ ] 原有 Dify API 调用兼容（可选开启）
- [ ] 数据库迁移脚本可回滚
- [ ] 原有工作流、RAG、Agent 功能正常

---

**文档状态**: 已完成设计，待用户审批后进入实施阶段
**下次更新**: 根据用户反馈修订
