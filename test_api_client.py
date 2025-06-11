#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time

# API服務器URL
BASE_URL = "http://localhost:5000"

def test_health_check():
    """測試健康檢查端點"""
    print("=== 測試健康檢查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"錯誤: {e}")
        return False

def test_status():
    """測試狀態端點"""
    print("\n=== 測試系統狀態 ===")
    try:
        response = requests.get(f"{BASE_URL}/status")
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"錯誤: {e}")
        return False

def test_send_message():
    """測試發送訊息"""
    print("\n=== 測試發送訊息 ===")
    try:
        # 測試數據
        data = {
            "message": "Hello from API test! 您好，這是API測試訊息！",
            "channel": 2
        }
        
        response = requests.post(
            f"{BASE_URL}/send",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"錯誤: {e}")
        return False

def test_broadcast_message():
    """測試廣播訊息"""
    print("\n=== 測試廣播訊息 ===")
    try:
        # 測試數據
        data = {
            "message": "Broadcast test message! 廣播測試訊息！",
            "channels": [1, 2, 3]
        }
        
        response = requests.post(
            f"{BASE_URL}/send/broadcast",
            json=data,
            headers={'Content-Type': 'application/json'}
        )
        
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
        return response.status_code == 200
    except Exception as e:
        print(f"錯誤: {e}")
        return False

def test_invalid_requests():
    """測試無效請求"""
    print("\n=== 測試無效請求 ===")
    
    # 測試空訊息
    print("測試空訊息:")
    try:
        data = {"message": "", "channel": 2}
        response = requests.post(f"{BASE_URL}/send", json=data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"錯誤: {e}")
    
    # 測試無效頻道
    print("\n測試無效頻道:")
    try:
        data = {"message": "Test", "channel": 10}
        response = requests.post(f"{BASE_URL}/send", json=data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"錯誤: {e}")
    
    # 測試缺少訊息欄位
    print("\n測試缺少訊息欄位:")
    try:
        data = {"channel": 2}
        response = requests.post(f"{BASE_URL}/send", json=data)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"錯誤: {e}")

def main():
    """執行所有測試"""
    print("開始API測試...")
    print(f"API服務器URL: {BASE_URL}")
    print("=" * 50)
    
    # 等待一下，確保服務器已啟動
    print("等待服務器啟動...")
    time.sleep(2)
    
    # 執行測試
    tests = [
        ("健康檢查", test_health_check),
        ("系統狀態", test_status),
        ("發送訊息", test_send_message),
        ("廣播訊息", test_broadcast_message),
    ]
    
    results = []
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"測試 {test_name} 時發生錯誤: {e}")
            results.append((test_name, False))
        
        # 在測試之間稍作暫停
        time.sleep(1)
    
    # 測試無效請求
    test_invalid_requests()
    
    # 顯示測試結果摘要
    print("\n" + "=" * 50)
    print("測試結果摘要:")
    for test_name, result in results:
        status = "✓ 通過" if result else "✗ 失敗"
        print(f"  {test_name}: {status}")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    print(f"\n總計: {passed}/{total} 測試通過")

if __name__ == "__main__":
    main()
