# Meshtastic API 服務器使用說明

## 概述

此API服務器允許外部設備通過HTTP請求發送訊息到Meshtastic網絡。服務器在背景運行並與主程式共享Meshtastic連接。

## API端點

### 1. 健康檢查
```
GET /health
```
檢查API服務器是否正常運行。

**回應範例:**
```json
{
  "status": "healthy",
  "timestamp": "2025-06-12T10:30:00.123456",
  "meshtastic_connected": true
}
```

### 2. 系統狀態
```
GET /status
```
獲取詳細的系統狀態資訊。

**回應範例:**
```json
{
  "success": true,
  "data": {
    "api_server": "運行中",
    "meshtastic_connection": "已連接",
    "timestamp": "2025-06-12T10:30:00.123456",
    "uptime": 3600
  }
}
```

### 3. 發送訊息
```
POST /send
```
發送訊息到指定的Meshtastic頻道。

**請求參數:**
```json
{
  "message": "要發送的訊息內容",
  "channel": 2
}
```

**參數說明:**
- `message` (必須): 要發送的訊息內容 (字串)
- `channel` (可選): 目標頻道，預設為2 (0-7之間的整數)

**回應範例:**
```json
{
  "success": true,
  "message": "訊息發送成功",
  "data": {
    "sent_message": "要發送的訊息內容",
    "channel": 2,
    "timestamp": "2025-06-12T10:30:00.123456"
  }
}
```

### 4. 廣播訊息
```
POST /send/broadcast
```
將訊息廣播到多個頻道。

**請求參數:**
```json
{
  "message": "廣播訊息內容",
  "channels": [1, 2, 3]
}
```

**參數說明:**
- `message` (必須): 要廣播的訊息內容 (字串)
- `channels` (可選): 目標頻道列表，預設為[1, 2, 3] (整數陣列)

**回應範例:**
```json
{
  "success": true,
  "message": "成功發送到 3/3 個頻道",
  "data": {
    "sent_message": "廣播訊息內容",
    "results": [
      {"channel": 1, "success": true, "message": "訊息發送成功"},
      {"channel": 2, "success": true, "message": "訊息發送成功"},
      {"channel": 3, "success": true, "message": "訊息發送成功"}
    ],
    "timestamp": "2025-06-12T10:30:00.123456"
  }
}
```

## 使用範例

### Python 範例
```python
import requests
import json

# 發送單一訊息
data = {
    "message": "Hello Meshtastic!",
    "channel": 2
}

response = requests.post(
    "http://localhost:5000/send",
    json=data,
    headers={'Content-Type': 'application/json'}
)

print(response.json())
```

### curl 範例
```bash
# 發送訊息
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from curl!", "channel": 2}'

# 廣播訊息
curl -X POST http://localhost:5000/send/broadcast \
  -H "Content-Type: application/json" \
  -d '{"message": "Broadcast message", "channels": [1, 2, 3]}'

# 檢查狀態
curl http://localhost:5000/status
```

## 錯誤處理

所有錯誤回應都會包含以下格式:
```json
{
  "success": false,
  "error": "錯誤描述"
}
```

**常見錯誤:**
- 400: 請求參數錯誤
- 404: 端點不存在
- 500: 服務器內部錯誤

## 啟動方式

API服務器會在主程式啟動時自動在背景運行。預設監聽所有網路介面的5000端口:
- 本機存取: `http://localhost:5000`
- 網路存取: `http://[你的IP]:5000`

## 日誌記錄

API活動會記錄在 `./logs/api_YYYY-MM-DD.log` 文件中，包含:
- 請求詳情
- 發送成功/失敗記錄
- 錯誤資訊

## 安全注意事項

1. API服務器目前沒有身份驗證，請在受信任的網路環境中使用。
2. 建議通過防火牆限制對5000端口的存取。
3. 訊息大小限制為200字節，超過會自動截斷。

## 測試

使用提供的測試腳本驗證API功能:
```bash
python test_api_client.py
```
