#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 main.py 中 @bashcat 指令的詳細天氣查詢功能
模擬用戶輸入，驗證完整的 LLM 聊天流程
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import get_weather_info_for_llm, get_earthquake_info_for_llm
from cwa_client import CWAClient

def simulate_bashcat_weather_query():
    """模擬 @bashcat 天氣查詢流程"""
    print("=== 模擬 @bashcat 天氣查詢流程 ===\n")
    
    try:
        # 建立 CWA 客戶端
        cwa_client = CWAClient()
        
        # 模擬用戶查詢
        test_queries = [
            "台北今天天氣如何？",
            "明天高雄會下雨嗎？",
            "桃園這週的天氣預報",
            "新竹現在天氣怎麼樣？"
        ]
        
        for query in test_queries:
            print(f"🙋 用戶查詢: {query}")
            print("-" * 50)
            
            # 檢查是否包含天氣關鍵詞
            if '天氣' in query:
                print("✅ 檢測到天氣關鍵詞，獲取天氣資料...")
                
                # 獲取天氣資訊
                weather_info = get_weather_info_for_llm(query, cwa_client)
                
                # 構建增強的 prompt
                enhanced_prompt = f"用戶查詢：{query}\n\n相關天氣資料：\n{weather_info}\n\n請根據以上天氣資料回答用戶的問題。"
                
                print("📊 增強的 LLM Prompt:")
                print(enhanced_prompt)
                
            print("\n" + "=" * 80 + "\n")
            
        print("✅ @bashcat 天氣查詢流程測試完成")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

def simulate_bashcat_earthquake_query():
    """模擬 @bashcat 地震查詢流程"""
    print("=== 模擬 @bashcat 地震查詢流程 ===\n")
    
    try:
        # 建立 CWA 客戶端
        cwa_client = CWAClient()
        
        # 模擬用戶查詢
        query = "最近有地震嗎？"
        
        print(f"🙋 用戶查詢: {query}")
        print("-" * 50)
        
        # 檢查是否包含地震關鍵詞
        if '地震' in query:
            print("✅ 檢測到地震關鍵詞，獲取地震資料...")
            
            # 獲取地震資訊
            earthquake_info = get_earthquake_info_for_llm(cwa_client)
            
            # 構建增強的 prompt
            enhanced_prompt = f"用戶查詢：{query}\n\n相關地震資料：\n{earthquake_info}\n\n請根據以上地震資料回答用戶的問題。"
            
            print("📊 增強的 LLM Prompt:")
            print(enhanced_prompt)
            
        print("\n✅ @bashcat 地震查詢流程測試完成")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

def test_detailed_weather_features():
    """測試詳細天氣功能的各種特性"""
    print("=== 測試詳細天氣功能特性 ===\n")
    
    try:
        client = CWAClient()
        
        # 測試不同的城市簡化名稱
        test_cities = [
            ("台北", "臺北市"),
            ("高雄", "高雄市"),
            ("台中", "臺中市"),
            ("桃園", "桃園市"),
            ("新竹", "新竹市"),
            ("台南", "臺南市")
        ]
        
        for simple_name, full_name in test_cities:
            print(f"🏙️ 測試城市: {simple_name} ({full_name})")
            
            # 直接調用詳細天氣方法
            detailed_weather = client.get_detailed_weather_for_llm(full_name)
            
            # 只顯示前幾行以節省空間
            lines = detailed_weather.split('\n')
            preview = '\n'.join(lines[:8])  # 顯示前8行
            
            print(preview)
            print("... (更多詳細資訊)")
            print("-" * 40)
            
        print("✅ 詳細天氣功能特性測試完成")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    simulate_bashcat_weather_query()
    print("\n" + "=" * 100 + "\n")
    simulate_bashcat_earthquake_query()
    print("\n" + "=" * 100 + "\n")
    test_detailed_weather_features()
