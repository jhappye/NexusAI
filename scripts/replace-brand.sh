#!/bin/bash
# scripts/replace-brand.sh - 品牌替换脚本

set -e

echo "开始替换 Dify 品牌标识..."

# 前端文本替换
find web -type f \( -name "*.tsx" -o -name "*.ts" -o -name "*.json" \) ! -path "*/node_modules/*" ! -path "*/.next/*" -exec sed -i \
  -e 's/Dify/NexusAI/g' \
  -e 's/dify/nexusai/g' \
  -e 's/DIFY/NEXUSAI/g' \
  -e 's/dify\.ai/nexusai.io/g' \
  -e 's/Dify Team/NexusAI Team/g' \
  -e "s/Dify's/NexusAI's/g" \
  {} \;

# 后端文本替换
find api -type f \( -name "*.py" -o -name "*.md" -o -name "*.yaml" -o -name "*.yml" \) ! -path "*/.git/*" ! -path "*/__pycache__/*" ! -path "*/node_modules/*" -exec sed -i \
  -e 's/Dify/NexusAI/g' \
  -e 's/dify/nexusai/g' \
  -e 's/DIFY/NEXUSAI/g' \
  -e 's/dify\.ai/nexusai.io/g' \
  -e 's/Dify Team/NexusAI Team/g' \
  -e "s/Dify's/NexusAI's/g" \
  {} \;

# 根目录文件
find . -maxdepth 2 -type f \( -name "*.md" -o -name "*.json" \) ! -path "./node_modules/*" ! -path "./.git/*" ! -path "./web/node_modules/*" ! -path "./api/.venv/*" -exec sed -i \
  -e 's/Dify/NexusAI/g' \
  -e 's/dify/nexusai/g' \
  -e 's/DIFY/NEXUSAI/g' \
  -e 's/dify\.ai/nexusai.io/g' \
  -e 's/Dify Team/NexusAI Team/g' \
  {} \;

echo "品牌替换完成"