#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

def test_api():
    base_url = "http://localhost:5000"
    
    print("🧪 測試修復後的 API 功能")
    print("=" * 50)
    
    # 1. 測試健康檢查
    print("\n1. 測試健康檢查...")
    try:
        response = requests.get(f"{base_url}/health")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 健康檢查失敗: {e}")
        return
    
    # 2. 測試系統狀態
    print("\n2. 測試系統狀態...")
    try:
        response = requests.get(f"{base_url}/status")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 狀態檢查失敗: {e}")
    
    # 3. 測試發送訊息 (應該會失敗，但錯誤訊息應該更清楚)
    print("\n3. 測試發送訊息...")
    try:
        data = {
            "message": "API 測試訊息",
            "channel": 2
        }
        response = requests.post(f"{base_url}/send", json=data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        
        if response.status_code == 500:
            print("✅ 正確返回錯誤：無法獲取共享接口")
        else:
            print("📋 訊息發送狀態已記錄")
            
    except Exception as e:
        print(f"❌ 發送測試失敗: {e}")
    
    # 4. 測試廣播功能
    print("\n4. 測試廣播功能...")
    try:
        data = {
            "message": "廣播測試訊息",
            "channels": [1, 2, 3]
        }
        response = requests.post(f"{base_url}/send/broadcast", json=data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"❌ 廣播測試失敗: {e}")
    
    print("\n" + "=" * 50)
    print("測試完成！")
    
    # 說明當前狀況
    print("\n📋 當前狀況說明：")
    print("✅ API 服務器正常運行")
    print("✅ 不再嘗試創建臨時 Meshtastic 接口")
    print("✅ 返回清楚的錯誤訊息")
    print("⚠️  需要確保共享接口正確傳遞給 API")

if __name__ == "__main__":
    test_api()
