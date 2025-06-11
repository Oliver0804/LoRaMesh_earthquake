#!/bin/bash

# 從.key檔案讀取API金鑰
API_KEY=$(cat .key | grep -v "^//" | head -n 1)

echo "使用的API金鑰: $API_KEY"

# 使用curl發送請求
curl -s \
  -X POST \
  -H "Authorization: Bearer $API_KEY" \
  -H "HTTP-Referer: https://n8n.bashcat.net" \
  -H "X-Title: n8n test" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "deepseek/deepseek-chat-v3-0324:free",
    "messages": [
      {
        "role": "user",
        "content": "請以不超過66個字符回答以下問題（請務必控制在66字以內）：地震是什麼？"
      }
    ],
    "max_tokens": 100
  }' \
  https://openrouter.ai/api/v1/chat/completions

echo -e "\n\n測試完成"
