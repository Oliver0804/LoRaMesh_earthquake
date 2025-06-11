#!/usr/bin/env bash

echo "=== 啟動API服務器測試 ==="

# 在背景啟動API服務器
cd /root/python/earthquake
python api_server.py &
API_PID=$!

echo "API服務器 PID: $API_PID"
echo "等待服務器啟動..."
sleep 5

echo "=== 測試健康檢查端點 ==="
curl -s http://localhost:5000/health | jq . 2>/dev/null || curl -s http://localhost:5000/health

echo -e "\n=== 測試狀態端點 ==="
curl -s http://localhost:5000/status | jq . 2>/dev/null || curl -s http://localhost:5000/status

echo -e "\n=== 測試發送訊息端點 ==="
curl -s -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "API測試訊息", "channel": 2}' \
  | jq . 2>/dev/null || curl -s -X POST http://localhost:5000/send -H "Content-Type: application/json" -d '{"message": "API測試訊息", "channel": 2}'

echo -e "\n=== 測試錯誤處理 ==="
curl -s -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "", "channel": 2}' \
  | jq . 2>/dev/null || curl -s -X POST http://localhost:5000/send -H "Content-Type: application/json" -d '{"message": "", "channel": 2}'

echo -e "\n=== 清理：停止API服務器 ==="
kill $API_PID 2>/dev/null
sleep 2
kill -9 $API_PID 2>/dev/null

echo "測試完成！"
