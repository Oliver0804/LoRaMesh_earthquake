#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試多筆地震資訊顯示功能
驗證修改後的 get_earthquake_info_for_llm 能夠正確顯示多筆地震資料
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cwa_client import CWAClient
from main import get_earthquake_info_for_llm

def test_multiple_earthquake_display():
    """測試多筆地震資訊顯示功能"""
    print("=== 測試多筆地震資訊顯示功能 ===\n")
    
    try:
        # 建立 CWA 客戶端
        client = CWAClient()
        
        # 測試 1: 預設顯示（最多5筆）
        print("📊 測試 1: 預設顯示（最多5筆詳細資訊）")
        print("-" * 60)
        
        earthquake_info = get_earthquake_info_for_llm(client)
        print(earthquake_info)
        
        # 測試 2: 顯示不同筆數
        print(f"\n{'='*80}\n")
        print("📊 測試 2: 自定義顯示筆數")
        print("-" * 60)
        
        # 測試顯示3筆
        print("🔹 顯示3筆詳細資訊：")
        print("-" * 30)
        earthquake_info_3 = get_earthquake_info_for_llm(client, max_display=3)
        
        # 只顯示前10行以節省空間
        lines = earthquake_info_3.split('\n')
        for line in lines[:15]:
            print(line)
        print("... (省略)")
        
        # 測試 3: 驗證輸出格式
        print(f"\n📋 測試 3: 驗證輸出格式")
        print("-" * 60)
        
        # 檢查輸出格式
        has_multiple_entries = earthquake_info.count('📍 第') >= 2
        has_latest_marker = '（最新）' in earthquake_info
        has_overall_stats = '📈 整體統計' in earthquake_info
        has_detailed_info = earthquake_info.count('📅 發生時間') >= 2
        
        print(f"包含多筆地震條目: {'✅' if has_multiple_entries else '❌'}")
        print(f"標記最新地震: {'✅' if has_latest_marker else '❌'}")
        print(f"包含整體統計: {'✅' if has_overall_stats else '❌'}")
        print(f"包含多筆詳細資訊: {'✅' if has_detailed_info else '❌'}")
        
        # 測試 4: 統計資訊驗證
        print(f"\n📈 測試 4: 統計資訊驗證")
        print("-" * 60)
        
        # 統計實際地震筆數
        earthquake_count = earthquake_info.count('📅 發生時間')
        total_earthquakes = 10  # 預設獲取10筆
        
        print(f"顯示的詳細地震筆數: {earthquake_count}")
        print(f"總地震資料筆數: {total_earthquakes}")
        
        # 檢查統計資訊
        stats_section = earthquake_info.split('📈 整體統計')[1] if '📈 整體統計' in earthquake_info else ""
        has_magnitude_4_stats = '規模4.0以上' in stats_section
        
        print(f"包含規模統計: {'✅' if has_magnitude_4_stats else '❌'}")
        
        print(f"\n✅ 多筆地震資訊顯示功能測試完成")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

def test_earthquake_display_comparison():
    """比較不同顯示筆數的效果"""
    print("\n=== 比較不同顯示筆數的效果 ===\n")
    
    try:
        client = CWAClient()
        
        display_counts = [1, 3, 5]
        
        for count in display_counts:
            print(f"🔸 顯示 {count} 筆詳細地震資訊：")
            print("-" * 40)
            
            earthquake_info = get_earthquake_info_for_llm(client, max_display=count)
            
            # 統計並顯示摘要
            detailed_count = earthquake_info.count('📅 發生時間')
            total_chars = len(earthquake_info)
            
            print(f"實際顯示詳細資訊: {detailed_count} 筆")
            print(f"總字符數: {total_chars}")
            
            # 顯示前3行內容作為預覽
            lines = earthquake_info.split('\n')
            for line in lines[:3]:
                print(f"  {line}")
            print("  ...")
            print()
        
        print("✅ 顯示筆數比較測試完成")
        
    except Exception as e:
        print(f"❌ 比較測試中發生錯誤: {str(e)}")

def test_bashcat_integration_with_multiple_earthquakes():
    """測試 @bashcat 整合功能與多筆地震顯示"""
    print("\n=== 測試 @bashcat 整合功能 ===\n")
    
    try:
        client = CWAClient()
        query = "最近有地震嗎？需要詳細資訊"
        
        print(f"🙋 用戶查詢: {query}")
        print("-" * 50)
        
        if '地震' in query:
            print("✅ 檢測到地震關鍵詞，獲取詳細地震資料...")
            
            # 獲取地震資訊（顯示3筆詳細資訊）
            earthquake_info = get_earthquake_info_for_llm(client, max_display=3)
            
            # 構建增強的 prompt
            enhanced_prompt = f"用戶查詢：{query}\n\n相關地震資料：\n{earthquake_info}\n\n請根據以上地震資料回答用戶的問題。"
            
            print("📊 增強的 LLM Prompt 長度:", len(enhanced_prompt))
            print("📋 地震資料筆數:", earthquake_info.count('📅 發生時間'))
            
            # 顯示前幾行 prompt 內容
            lines = enhanced_prompt.split('\n')
            print("\n📝 Prompt 預覽（前10行）:")
            for line in lines[:10]:
                print(f"  {line}")
            print("  ...")
        
        print("\n✅ @bashcat 整合測試完成")
        
    except Exception as e:
        print(f"❌ 整合測試中發生錯誤: {str(e)}")

if __name__ == "__main__":
    test_multiple_earthquake_display()
    test_earthquake_display_comparison()
    test_bashcat_integration_with_multiple_earthquakes()
