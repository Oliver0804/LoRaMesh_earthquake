#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import subprocess
import threading
import sys
import os

def start_test_server():
    """在背景啟動測試服務器"""
    try:
        # 啟動API服務器
        cmd = [sys.executable, "api_server.py"]
        process = subprocess.Popen(
            cmd,
            cwd="/root/python/earthquake",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE
        )
        return process
    except Exception as e:
        print(f"啟動服務器失敗: {e}")
        return None

def test_api_endpoints():
    """測試API端點（不需要Meshtastic硬件）"""
    BASE_URL = "http://localhost:5000"
    
    # 等待服務器啟動
    print("等待API服務器啟動...")
    time.sleep(3)
    
    # 測試健康檢查
    print("=== 測試健康檢查 ===")
    try:
        response = requests.get(f"{BASE_URL}/health", timeout=5)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"健康檢查失敗: {e}")
    
    # 測試狀態端點
    print("\n=== 測試系統狀態 ===")
    try:
        response = requests.get(f"{BASE_URL}/status", timeout=5)
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"狀態檢查失敗: {e}")
    
    # 測試發送訊息（會嘗試連接Meshtastic，但不會影響API結構測試）
    print("\n=== 測試發送訊息端點結構 ===")
    try:
        data = {"message": "Test message", "channel": 2}
        response = requests.post(
            f"{BASE_URL}/send",
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        print(f"狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"發送測試失敗: {e}")
    
    # 測試錯誤處理
    print("\n=== 測試錯誤處理 ===")
    try:
        # 測試空訊息
        data = {"message": "", "channel": 2}
        response = requests.post(f"{BASE_URL}/send", json=data, timeout=5)
        print(f"空訊息測試 - 狀態碼: {response.status_code}")
        print(f"回應: {json.dumps(response.json(), indent=2, ensure_ascii=False)}")
    except Exception as e:
        print(f"錯誤處理測試失敗: {e}")

def main():
    """主測試函數"""
    print("開始API結構測試（不需要Meshtastic硬件）...")
    print("=" * 60)
    
    # 啟動測試服務器
    server_process = start_test_server()
    if server_process is None:
        print("無法啟動測試服務器")
        return
    
    try:
        # 執行API測試
        test_api_endpoints()
        
    finally:
        # 清理：停止服務器
        print(f"\n停止測試服務器...")
        server_process.terminate()
        time.sleep(1)
        if server_process.poll() is None:
            server_process.kill()
        print("測試完成")

if __name__ == "__main__":
    main()
