# Meshtastic API 外部訊息發送系統

## 功能概述

已成功為您的地震監控系統添加了API功能，允許外部設備通過HTTP請求發送訊息到Meshtastic網絡。

## 主要特點

✅ **RESTful API**: 提供標準的HTTP API接口  
✅ **多頻道支持**: 支援向指定頻道(0-7)發送訊息  
✅ **廣播功能**: 支援向多個頻道同時廣播訊息  
✅ **錯誤處理**: 完善的錯誤處理和驗證機制  
✅ **線程安全**: 與主程式安全共享Meshtastic連接  
✅ **日誌記錄**: 詳細的API活動日誌  
✅ **CORS支持**: 支援跨域請求  

## 系統架構

```
外部設備 -> HTTP API -> Flask服務器 -> Meshtastic接口 -> 無線網絡
```

## 啟動方式

1. **自動啟動**: 運行主程式時，API服務器會自動在背景啟動
   ```bash
   python main.py
   ```

2. **獨立啟動**: 也可以單獨運行API服務器
   ```bash
   python api_server.py
   ```

API服務器將監聽: `http://0.0.0.0:5000`

## API端點

### 1. 健康檢查
```http
GET /health
```

### 2. 系統狀態
```http
GET /status
```

### 3. 發送單一訊息
```http
POST /send
Content-Type: application/json

{
  "message": "要發送的訊息",
  "channel": 2
}
```

### 4. 廣播到多頻道
```http
POST /send/broadcast
Content-Type: application/json

{
  "message": "廣播訊息",
  "channels": [1, 2, 3]
}
```

## 使用範例

### Python範例
```python
import requests

# 發送訊息
response = requests.post(
    "http://localhost:5000/send",
    json={"message": "Hello Meshtastic!", "channel": 2}
)
print(response.json())
```

### curl範例
```bash
# 發送訊息
curl -X POST http://localhost:5000/send \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello from curl!", "channel": 2}'

# 檢查狀態
curl http://localhost:5000/status
```

### Arduino/ESP32範例
```cpp
#include <WiFi.h>
#include <HTTPClient.h>
#include <ArduinoJson.h>

void sendMeshtasticMessage(String message, int channel) {
  HTTPClient http;
  http.begin("http://192.168.1.100:5000/send");  // 替換為實際IP
  http.addHeader("Content-Type", "application/json");
  
  DynamicJsonDocument doc(1024);
  doc["message"] = message;
  doc["channel"] = channel;
  
  String jsonString;
  serializeJson(doc, jsonString);
  
  int httpResponseCode = http.POST(jsonString);
  
  if (httpResponseCode > 0) {
    String response = http.getString();
    Serial.println("Response: " + response);
  }
  
  http.end();
}
```

## 測試工具

提供了多個測試工具：

1. **完整測試**: `python test_api_client.py`
2. **結構測試**: `python test_api_structure.py`
3. **簡單測試**: `./test_api_simple.sh`
4. **使用範例**: `python example_api_client.py`

## 安全考量

⚠️ **重要安全提醒**:
- API目前沒有身份驗證
- 建議在受信任的內網環境中使用
- 可考慮通過防火牆限制5000端口存取
- 訊息大小限制為200字節

## 日誌記錄

- **主程式日誌**: `./logs/YYYY-MM-DD.log`
- **API日誌**: `./logs/api_YYYY-MM-DD.log`

## 故障排除

### 常見問題

1. **API無法存取**
   - 檢查主程式是否運行
   - 確認5000端口未被佔用
   - 檢查防火牆設定

2. **Meshtastic連接失敗**
   - 檢查USB裝置連接
   - 確認Meshtastic裝置正常
   - 查看日誌檔案

3. **訊息發送失敗**
   - 檢查頻道設定(0-7)
   - 確認訊息不為空
   - 查看API日誌

### 檢查服務狀態
```bash
# 檢查API是否運行
curl http://localhost:5000/health

# 檢查系統狀態
curl http://localhost:5000/status

# 檢查進程
ps aux | grep python
```

## 整合建議

### 物聯網設備整合
- ESP32/ESP8266可通過WiFi連接API
- Arduino配合網路擴展版使用
- 樹莓派可直接調用API

### 自動化系統整合
- 與Home Assistant整合
- 連接智能家居系統
- 整合監控告警系統

### 移動應用整合
- 開發手機App調用API
- 網頁應用程式介面
- 微信小程式整合

## 更新記錄

- ✅ 添加Flask API服務器
- ✅ 實現訊息發送功能
- ✅ 添加廣播功能
- ✅ 完善錯誤處理
- ✅ 添加CORS支持
- ✅ 創建測試工具
- ✅ 撰寫使用文檔

API功能已成功添加並測試通過！🎉
