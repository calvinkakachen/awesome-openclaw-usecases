#!/bin/bash
# imagetest 一键启动脚本
# 用法：bash start.sh
# 功能：自动拉取最新代码，服务崩溃自动重启

set -e

BRANCH="claude/chinese-language-setup-M1Mm7"
PORT=8000

cd "$(dirname "$0")"

echo "================================================"
echo " imagetest 启动脚本"
echo "================================================"

# 拉取最新代码
echo "[1/3] 拉取最新代码..."
git pull origin "$BRANCH" 2>&1 || echo "  ⚠ git pull 失败，使用本地代码继续"

# 安装/更新依赖
echo "[2/3] 检查依赖..."
pip3 install -q -r requirements.txt 2>&1 | tail -3

echo "[3/3] 启动服务器 (端口 $PORT)..."
echo ""
echo "  访问地址：http://localhost:$PORT"
echo "  按 Ctrl+C 停止"
echo "================================================"
echo ""

# 崩溃自动重启循环
while true; do
    python3 -m uvicorn app:app --host 0.0.0.0 --port $PORT --reload 2>&1
    EXIT_CODE=$?
    if [ $EXIT_CODE -eq 0 ]; then
        # 用户主动 Ctrl+C
        echo ""
        echo "服务已停止。"
        break
    fi
    echo ""
    echo "  ⚠ 服务崩溃 (exit $EXIT_CODE)，3秒后自动重启..."
    sleep 3
done
