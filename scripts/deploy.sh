#!/bin/bash
# NexusAI 一键部署脚本
# 适用于 Docker Compose 极简部署

set -e

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

log_info() { echo -e "${GREEN}[INFO]${NC} $1"; }
log_warn() { echo -e "${YELLOW}[WARN]${NC} $1"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1"; }

# 检查 Docker
check_docker() {
    log_info "检查 Docker 环境..."
    if ! command -v docker &> /dev/null; then
        log_error "Docker 未安装，请先安装 Docker"
        exit 1
    fi
    if ! docker compose version &> /dev/null; then
        log_error "Docker Compose 未安装"
        exit 1
    fi
    log_info "Docker 环境检查通过"
}

# 主函数
main() {
    echo "=========================================="
    echo "     NexusAI 企业级 AI 中台部署脚本"
    echo "=========================================="
    echo ""

    check_docker

    log_info "启动 NexusAI 服务..."
    docker compose -f docker/docker-compose.simple.yaml up -d

    log_info "等待服务启动..."
    sleep 10

    log_info "检查服务状态..."
    docker compose -f docker/docker-compose.simple.yaml ps

    echo ""
    echo "=========================================="
    log_info "NexusAI 部署完成！"
    echo "=========================================="
    echo ""
    echo "访问地址: http://localhost:${WEB_PORT:-3000}"
    echo "API 地址: http://localhost:${API_PORT:-5001}"
    echo ""
}

main "$@"