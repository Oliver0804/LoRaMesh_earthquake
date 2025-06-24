#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試@bashcat天氣和地震查詢功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import get_weather_info_for_llm, get_earthquake_info_for_llm, CITY_TO_FULL_NAME
from cwa_client import CWAClient

def test_weather_queries():
    """測試天氣查詢功能"""
    print("🌤️ 測試天氣查詢功能")
    print("=" * 50)
    
    try:
        cwa_client = CWAClient()
        
        test_queries = [
            "台北天氣如何？",
            "高雄今天會下雨嗎？",
            "花蓮的天氣預報",
            "臺中市天氣狀況",
            "新竹天氣"
        ]
        
        for query in test_queries:
            print(f"\n📋 查詢: {query}")
            result = get_weather_info_for_llm(query, cwa_client)
            print(f"✅ 結果: {result[:150]}{'...' if len(result) > 150 else ''}")
            
    except Exception as e:
        print(f"❌ 天氣查詢測試失敗: {e}")

def test_earthquake_query():
    """測試地震查詢功能"""
    print("\n\n🌏 測試地震查詢功能")
    print("=" * 50)
    
    try:
        cwa_client = CWAClient()
        
        print(f"\n📋 查詢: 最新地震資訊")
        result = get_earthquake_info_for_llm(cwa_client)
        print(f"✅ 結果: {result[:200]}{'...' if len(result) > 200 else ''}")
        
    except Exception as e:
        print(f"❌ 地震查詢測試失敗: {e}")

def test_city_mapping():
    """測試城市映射功能"""
    print("\n\n🗺️ 測試城市映射功能")
    print("=" * 50)
    
    test_cities = ['台北', '臺北', '高雄', '花蓮', '新竹', '新竹市', '嘉義', '嘉義市']
    
    for city in test_cities:
        if city in CITY_TO_FULL_NAME:
            full_name = CITY_TO_FULL_NAME[city]
            print(f"✅ {city} -> {full_name}")
        else:
            print(f"❌ {city} -> 未找到映射")

def test_keyword_detection():
    """測試關鍵詞檢測邏輯"""
    print("\n\n🔍 測試關鍵詞檢測功能")
    print("=" * 50)
    
    test_queries = [
        ("台北天氣如何？", True, False),
        ("高雄今天會下雨嗎？", False, False),  # 沒有"天氣"關鍵詞
        ("最近有地震嗎？", False, True),
        ("今天的地震情況", False, True),
        ("花蓮的天氣預報", True, False),
        ("天氣和地震都想知道", True, True),
        ("其他普通問題", False, False)
    ]
    
    for query, expected_weather, expected_earthquake in test_queries:
        has_weather = '天氣' in query
        has_earthquake = '地震' in query
        
        weather_status = "✅" if has_weather == expected_weather else "❌"
        earthquake_status = "✅" if has_earthquake == expected_earthquake else "❌"
        
        print(f"{query}:")
        print(f"  天氣檢測: {weather_status} {has_weather} (預期: {expected_weather})")
        print(f"  地震檢測: {earthquake_status} {has_earthquake} (預期: {expected_earthquake})")

if __name__ == "__main__":
    print("🚀 開始測試@bashcat天氣和地震查詢功能")
    print("=" * 60)
    
    test_city_mapping()
    test_keyword_detection()
    test_weather_queries()
    test_earthquake_query()
    
    print("\n\n🎉 測試完成！")
    print("=" * 60)
    print("💡 使用方式:")
    print("   @bashcat 台北天氣如何？")
    print("   @bashcat 最近有地震嗎？")
    print("   @bashcat 高雄今天會下雨嗎？")
