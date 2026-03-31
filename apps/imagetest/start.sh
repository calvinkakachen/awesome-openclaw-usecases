#!/bin/bash
# imagetest 一键启动脚本
# 用法：bash start.sh

set -e

PORT=8000

cd "$(dirname "$0")"

echo "================================================"
echo " imagetest 启动脚本"
echo "================================================"

echo "[1/2] 检查虚拟环境与依赖..."
if [ ! -f "venv/bin/activate" ]; then
  python3 -m venv venv
fi
venv/bin/pip install -q -r requirements.txt 2>&1 | tail -3

echo "[2/2] 启动服务器 (端口 $PORT)..."
echo ""
echo "  访问地址：http://localhost:$PORT"
echo "  按 Ctrl+C 停止"
echo "================================================"
echo ""

while true; do
    venv/bin/uvicorn app:app --host 0.0.0.0 --port $PORT 2>&1
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        echo ""
        echo "服务已停止。"
        break
    fi
    echo ""
    echo "  ⚠ 服务崩溃 (exit $EXIT_CODE)，3秒后自动重启..."
    sleep 3
done
