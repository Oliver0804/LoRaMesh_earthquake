#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試地震查詢功能的更新
驗證獲取10筆地震資料的功能是否正常
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from cwa_client import CWAClient
from main import get_earthquake_info_for_llm

def test_earthquake_query_update():
    """測試更新後的地震查詢功能"""
    print("=== 測試地震查詢功能更新 ===\n")
    
    try:
        # 建立 CWA 客戶端
        client = CWAClient()
        
        # 測試 1: 直接調用 get_latest_earthquake (現在預設10筆)
        print("📊 測試 1: 直接調用 get_latest_earthquake")
        print("-" * 50)
        
        earthquake_data = client.get_latest_earthquake()
        
        if earthquake_data.get('success') == 'true':
            earthquakes = earthquake_data.get('records', {}).get('Earthquake', [])
            print(f"✅ 成功獲取 {len(earthquakes)} 筆地震資料")
            
            # 顯示前3筆地震的簡要資訊
            for i, eq in enumerate(earthquakes[:3]):
                eq_info = eq.get('EarthquakeInfo', {})
                origin_time = eq_info.get('OriginTime', '未知時間')
                magnitude = eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', '未知')
                location = eq_info.get('Epicenter', {}).get('Location', '未知位置')
                
                print(f"  {i+1}. {origin_time} | M{magnitude} | {location}")
            
            if len(earthquakes) > 3:
                print(f"  ... 還有 {len(earthquakes) - 3} 筆地震資料")
        else:
            print("❌ 無法獲取地震資料")
        
        # 測試 2: 使用 main.py 中的 get_earthquake_info_for_llm
        print(f"\n📋 測試 2: main.py 中的地震資訊格式化")
        print("-" * 50)
        
        formatted_earthquake_info = get_earthquake_info_for_llm(client)
        print(formatted_earthquake_info)
        
        # 測試 3: 驗證格式化內容的特性
        print(f"\n🔍 測試 3: 驗證格式化內容特性")
        print("-" * 50)
        
        # 檢查是否包含新增的功能
        has_latest_info = '最新地震資訊' in formatted_earthquake_info
        has_recent_overview = '近期地震概況' in formatted_earthquake_info
        has_magnitude_stats = '規模4.0以上' in formatted_earthquake_info
        has_emojis = '🌍' in formatted_earthquake_info
        
        print(f"包含最新地震資訊: {'✅' if has_latest_info else '❌'}")
        print(f"包含近期地震概況: {'✅' if has_recent_overview else '❌'}")
        print(f"包含規模統計: {'✅' if has_magnitude_stats else '❌'}")
        print(f"包含表情符號增強: {'✅' if has_emojis else '❌'}")
        
        # 測試 4: 自定義筆數查詢
        print(f"\n🎯 測試 4: 自定義筆數查詢")
        print("-" * 50)
        
        # 測試獲取不同筆數的地震資料
        for count in [1, 5, 15]:
            test_data = client.get_latest_earthquake(count=count)
            if test_data.get('success') == 'true':
                test_earthquakes = test_data.get('records', {}).get('Earthquake', [])
                print(f"要求 {count:2} 筆，實際獲得 {len(test_earthquakes):2} 筆：{'✅' if len(test_earthquakes) <= count else '❌'}")
        
        print(f"\n✅ 地震查詢功能更新測試完成")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {str(e)}")
        import traceback
        traceback.print_exc()

def test_earthquake_statistics():
    """測試地震統計功能"""
    print("\n=== 地震統計功能測試 ===\n")
    
    try:
        client = CWAClient()
        earthquake_data = client.get_latest_earthquake()
        
        if earthquake_data.get('success') == 'true':
            earthquakes = earthquake_data.get('records', {}).get('Earthquake', [])
            
            print(f"🔢 地震資料統計（最近 {len(earthquakes)} 筆）")
            print("-" * 50)
            
            # 統計不同規模的地震
            magnitude_ranges = {
                '小型 (M < 4.0)': 0,
                '輕微 (4.0 ≤ M < 5.0)': 0,
                '中等 (5.0 ≤ M < 6.0)': 0,
                '強烈 (6.0 ≤ M < 7.0)': 0,
                '重大 (M ≥ 7.0)': 0
            }
            
            for eq in earthquakes:
                eq_mag = eq.get('EarthquakeInfo', {}).get('EarthquakeMagnitude', {}).get('MagnitudeValue', '0')
                try:
                    mag_value = float(eq_mag)
                    if mag_value < 4.0:
                        magnitude_ranges['小型 (M < 4.0)'] += 1
                    elif mag_value < 5.0:
                        magnitude_ranges['輕微 (4.0 ≤ M < 5.0)'] += 1
                    elif mag_value < 6.0:
                        magnitude_ranges['中等 (5.0 ≤ M < 6.0)'] += 1
                    elif mag_value < 7.0:
                        magnitude_ranges['強烈 (6.0 ≤ M < 7.0)'] += 1
                    else:
                        magnitude_ranges['重大 (M ≥ 7.0)'] += 1
                except:
                    pass
            
            for range_name, count in magnitude_ranges.items():
                if count > 0:
                    print(f"  {range_name}: {count} 次")
            
            # 顯示地震發生地區統計
            print(f"\n📍 地震發生地區統計")
            print("-" * 30)
            
            location_count = {}
            for eq in earthquakes:
                location = eq.get('EarthquakeInfo', {}).get('Epicenter', {}).get('Location', '未知位置')
                # 簡化地名（取縣市名稱）
                if '縣' in location:
                    simplified_location = location.split('縣')[0] + '縣'
                elif '市' in location:
                    simplified_location = location.split('市')[0] + '市'
                else:
                    simplified_location = location
                
                location_count[simplified_location] = location_count.get(simplified_location, 0) + 1
            
            # 按次數排序顯示
            sorted_locations = sorted(location_count.items(), key=lambda x: x[1], reverse=True)
            for location, count in sorted_locations[:5]:  # 顯示前5個地區
                print(f"  {location}: {count} 次")
        
        print(f"\n✅ 地震統計功能測試完成")
        
    except Exception as e:
        print(f"❌ 統計測試中發生錯誤: {str(e)}")

if __name__ == "__main__":
    test_earthquake_query_update()
    test_earthquake_statistics()
