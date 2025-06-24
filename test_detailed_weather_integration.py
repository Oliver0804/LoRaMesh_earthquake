#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試 main.py 中更新後的天氣查詢功能
驗證 get_detailed_weather_for_llm 是否正確整合
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cwa_client import CWAClient
from main import get_weather_info_for_llm

def test_detailed_weather_integration():
    """測試 main.py 中的詳細天氣查詢整合"""
    print("=== 測試 main.py 中的詳細天氣查詢整合 ===\n")
    
    try:
        # 建立 CWA 客戶端
        client = CWAClient()
        
        # 測試不同城市和查詢方式
        test_queries = [
            "台北今天天氣如何？",
            "高雄明天會下雨嗎？",
            "桃園的天氣預報",
            "新竹天氣怎麼樣",
            "台中這幾天的天氣",
            "花蓮天氣狀況"
        ]
        
        for i, query in enumerate(test_queries, 1):
            print(f"測試 {i}: {query}")
            print("-" * 50)
            
            # 使用 main.py 中的函數獲取天氣資訊
            weather_info = get_weather_info_for_llm(query, client)
            
            print(weather_info)
            print("\n" + "=" * 80 + "\n")
        
        print("✅ 詳細天氣查詢整合測試完成")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

def test_compare_old_vs_new():
    """比較舊版本和新版本的天氣資訊輸出差異"""
    print("=== 比較舊版本和新版本的天氣資訊 ===\n")
    
    try:
        client = CWAClient()
        city_name = "臺北市"
        
        print(f"測試城市: {city_name}")
        print("-" * 50)
        
        # 新版本：使用 get_detailed_weather_for_llm
        print("🆕 新版本（詳細天氣資訊）:")
        detailed_weather = client.get_detailed_weather_for_llm(city_name)
        print(detailed_weather)
        
        print("\n" + "=" * 80 + "\n")
        
        # 舊版本：直接使用 get_city_weather 的簡化版本
        print("🔧 舊版本（簡化天氣資訊）:")
        weather_data = client.get_city_weather(city_name)
        
        if weather_data.get('success') == 'true':
            locations = weather_data.get('records', {}).get('location', [])
            if locations:
                location_data = locations[0]
                weather_elements = location_data.get('weatherElement', [])
                
                weather_info = {}
                for element in weather_elements:
                    element_name = element.get('elementName')
                    if element_name in ['Wx', 'PoP', 'MinT', 'MaxT']:
                        time_periods = element.get('time', [])
                        if time_periods:
                            first_period = time_periods[0]
                            parameter = first_period.get('parameter', {})
                            weather_info[element_name] = parameter.get('parameterName', parameter.get('parameterValue', ''))
                
                old_summary = f"{city_name}天氣資訊：\n"
                if 'Wx' in weather_info:
                    old_summary += f"天氣狀況：{weather_info['Wx']}\n"
                if 'MinT' in weather_info and 'MaxT' in weather_info:
                    old_summary += f"溫度：{weather_info['MinT']}°C - {weather_info['MaxT']}°C\n"
                if 'PoP' in weather_info:
                    old_summary += f"降雨機率：{weather_info['PoP']}%\n"
                
                print(old_summary.strip())
        
        print("\n✅ 版本比較完成")
        print("📊 可以看到新版本提供了更多詳細資訊，包括多個時段、風向風速、溼度、舒適度、UV指數等。")
        
    except Exception as e:
        print(f"❌ 比較測試中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_detailed_weather_integration()
    print("\n" + "=" * 100 + "\n")
    test_compare_old_vs_new()
