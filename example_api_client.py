#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Meshtastic API客戶端範例

此範例展示如何使用API發送訊息到Meshtastic網絡
"""

import requests
import json
import time

# API服務器配置
API_BASE_URL = "http://localhost:5000"

def send_simple_message(message, channel=2):
    """發送簡單訊息"""
    try:
        data = {
            "message": message,
            "channel": channel
        }
        
        response = requests.post(
            f"{API_BASE_URL}/send",
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=10
        )
        
        result = response.json()
        if result.get('success'):
            print(f"✓ 訊息發送成功: {message}")
            return True
        else:
            print(f"✗ 發送失敗: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"✗ 網絡錯誤: {e}")
        return False

def broadcast_message(message, channels=[1, 2, 3]):
    """廣播訊息到多個頻道"""
    try:
        data = {
            "message": message,
            "channels": channels
        }
        
        response = requests.post(
            f"{API_BASE_URL}/send/broadcast",
            json=data,
            headers={'Content-Type': 'application/json'},
            timeout=15
        )
        
        result = response.json()
        if result.get('success'):
            results = result['data']['results']
            successful = [r for r in results if r['success']]
            print(f"✓ 廣播成功: {len(successful)}/{len(channels)} 個頻道")
            return True
        else:
            print(f"✗ 廣播失敗: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"✗ 網絡錯誤: {e}")
        return False

def check_api_status():
    """檢查API狀態"""
    try:
        response = requests.get(f"{API_BASE_URL}/status", timeout=5)
        result = response.json()
        
        if result.get('success'):
            data = result['data']
            print(f"API狀態: {data['api_server']}")
            print(f"Meshtastic連接: {data['meshtastic_connection']}")
            print(f"運行時間: {data['uptime']:.1f} 秒")
            return True
        else:
            print(f"狀態檢查失敗: {result.get('error')}")
            return False
            
    except Exception as e:
        print(f"無法連接到API服務器: {e}")
        return False

def main():
    """主程式範例"""
    print("=== Meshtastic API客戶端範例 ===")
    
    # 檢查API狀態
    print("\n1. 檢查API狀態:")
    if not check_api_status():
        print("請確保主程式正在運行並且API服務器已啟動")
        return
    
    # 發送簡單訊息
    print("\n2. 發送簡單訊息:")
    send_simple_message("Hello from API client! 你好！", channel=2)
    
    # 等待一下
    time.sleep(1)
    
    # 廣播訊息
    print("\n3. 廣播訊息:")
    broadcast_message("廣播測試訊息 - API客戶端", channels=[1, 2, 3])
    
    # 發送到不同頻道
    print("\n4. 發送到不同頻道:")
    send_simple_message("頻道1訊息", channel=1)
    time.sleep(0.5)
    send_simple_message("頻道3訊息", channel=3)
    
    print("\n=== 範例完成 ===")

if __name__ == "__main__":
    main()
