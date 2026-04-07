#!/bin/bash
# NexusAI 健康检查脚本

set -e

WEB_URL=${WEB_PORT:-3000}
API_URL=${API_PORT:-5001}

echo "执行 NexusAI 健康检查..."
echo ""

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

failed=0

check_service "Web UI" "http://localhost:$WEB_URL" || ((failed++))
check_service "API" "http://localhost:$API_URL/health" || ((failed++))

echo ""
echo "容器状态:"
docker compose -f docker/docker-compose.simple.yaml ps 2>/dev/null || echo "无法获取容器状态"

if [ $failed -gt 0 ]; then
    echo ""
    echo "健康检查失败: $failed 项"
    exit 1
else
    echo ""
    echo "所有检查通过"
    exit 0
fi