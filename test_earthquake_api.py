#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
地震資訊查詢測試程式
Earthquake Information Query Test
"""

from cwa_client import CWAClient
import json
from datetime import datetime

def test_earthquake_api():
    """測試地震 API 功能"""
    print("🌏 地震資訊查詢測試")
    print("=" * 50)
    
    try:
        # 建立客戶端
        client = CWAClient()
        
        # 1. 測試取得最新地震報告
        print("\n📋 1. 取得最新地震報告...")
        latest_eq = client.get_latest_earthquake(count=1)
        
        if latest_eq.get('success') == 'true':
            earthquakes = latest_eq.get('records', {}).get('Earthquake', [])
            if earthquakes:
                eq = earthquakes[0]
                eq_info = eq.get('EarthquakeInfo', {})
                
                print("✅ 最新地震資訊:")
                print(f"  🕐 發生時間: {eq_info.get('OriginTime')}")
                print(f"  📍 震央位置: {eq_info.get('Epicenter', {}).get('Location')}")
                print(f"  📊 規模: {eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue')}")
                print(f"  📏 深度: {eq_info.get('FocalDepth')} 公里")
                print(f"  📝 報告內容: {eq.get('ReportContent')}")
                print(f"  🎨 警報顏色: {eq.get('ReportColor')}")
                print(f"  🔗 詳細資訊: {eq.get('Web')}")
                
                # 顯示震度資訊
                intensity = eq.get('Intensity', {})
                shaking_areas = intensity.get('ShakingArea', [])
                if shaking_areas:
                    print(f"\n  📈 震度分布 (共 {len(shaking_areas)} 個區域):")
                    for i, area in enumerate(shaking_areas[:5]):  # 只顯示前5個區域
                        county = area.get('CountyName', '未知')
                        max_intensity = area.get('AreaIntensity', '未知')
                        print(f"    {i+1}. {county}: {max_intensity}")
                        
                        # 顯示該區域的測站資訊
                        stations = area.get('EqStation', [])
                        if stations:
                            print(f"       測站數量: {len(stations)} 個")
                            for j, station in enumerate(stations[:2]):  # 只顯示前2個測站
                                station_name = station.get('StationName', '未知')
                                station_intensity = station.get('SeismicIntensity', '未知')
                                print(f"       - {station_name}: {station_intensity}")
            else:
                print("ℹ️  目前無最新地震資料")
        else:
            print("❌ 無法取得最新地震資料")
        
        # 2. 測試取得多筆地震報告
        print("\n\n📊 2. 取得最近5筆地震報告...")
        recent_eqs = client.get_significant_earthquake_report(limit=5, offset=0)
        
        if recent_eqs.get('success') == 'true':
            earthquakes = recent_eqs.get('records', {}).get('Earthquake', [])
            print(f"✅ 成功取得 {len(earthquakes)} 筆地震資料:")
            
            for i, eq in enumerate(earthquakes):
                eq_info = eq.get('EarthquakeInfo', {})
                origin_time = eq_info.get('OriginTime')
                location = eq_info.get('Epicenter', {}).get('Location')
                magnitude = eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue')
                depth = eq_info.get('FocalDepth')
                
                print(f"\n  🌊 地震 {i+1}:")
                print(f"    時間: {origin_time}")
                print(f"    位置: {location}")
                print(f"    規模: {magnitude}")
                print(f"    深度: {depth} 公里")
        else:
            print("❌ 無法取得地震資料")
        
        # 3. 測試小區域地震報告
        print("\n\n🏘️  3. 取得小區域地震報告...")
        local_eqs = client.get_local_earthquake_report(limit=3, offset=0)
        
        if local_eqs.get('success') == 'true':
            earthquakes = local_eqs.get('records', {}).get('Earthquake', [])
            print(f"✅ 成功取得 {len(earthquakes)} 筆小區域地震資料")
            
            for i, eq in enumerate(earthquakes):
                eq_info = eq.get('EarthquakeInfo', {})
                origin_time = eq_info.get('OriginTime')
                location = eq_info.get('Epicenter', {}).get('Location')
                magnitude = eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue')
                
                print(f"  {i+1}. {origin_time} | {location} | M{magnitude}")
        else:
            print("❌ 無法取得小區域地震資料")
        
        # 4. 測試英文地震報告
        print("\n\n🌍 4. 取得英文地震報告...")
        en_eqs = client.get_significant_earthquake_report(language='en', limit=1, offset=0)
        
        if en_eqs.get('success') == 'true':
            earthquakes = en_eqs.get('records', {}).get('Earthquake', [])
            if earthquakes:
                eq = earthquakes[0]
                eq_info = eq.get('EarthquakeInfo', {})
                
                print("✅ 英文地震報告:")
                print(f"  Time: {eq_info.get('OriginTime')}")
                print(f"  Location: {eq_info.get('Epicenter', {}).get('Location')}")
                print(f"  Magnitude: {eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue')}")
                print(f"  Depth: {eq_info.get('FocalDepth')} km")
                print(f"  Report: {eq.get('ReportContent')}")
        else:
            print("❌ 無法取得英文地震資料")
        
        # 5. 測試海嘯資訊
        print("\n\n🌊 5. 取得海嘯資訊...")
        tsunami_info = client.get_tsunami_info()
        
        if tsunami_info.get('success') == 'true':
            tsunamis = tsunami_info.get('records', {}).get('tsunami', [])
            if tsunamis:
                print(f"⚠️  有海嘯資訊 (共 {len(tsunamis)} 筆)")
                for i, tsunami in enumerate(tsunamis[:3]):
                    print(f"  {i+1}. 海嘯資訊: {tsunami}")
            else:
                print("✅ 目前無海嘯資訊")
        else:
            print("❌ 無法取得海嘯資訊")
        
        # 6. 儲存最新地震資料
        print("\n\n💾 6. 儲存最新地震資料...")
        if latest_eq.get('success') == 'true':
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"latest_earthquake_{timestamp}.json"
            client.save_data_to_file(latest_eq, filename)
            print(f"✅ 地震資料已儲存到 {filename}")
        
        print("\n" + "=" * 50)
        print("✅ 地震 API 測試完成！")
        
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")

def display_earthquake_details():
    """顯示地震資料的詳細結構"""
    print("\n\n🔍 地震資料結構分析")
    print("=" * 50)
    
    try:
        client = CWAClient()
        earthquake_data = client.get_latest_earthquake(count=1)
        
        if earthquake_data.get('success') == 'true':
            earthquakes = earthquake_data.get('records', {}).get('Earthquake', [])
            if earthquakes:
                eq = earthquakes[0]
                
                print("📊 地震資料包含的主要欄位:")
                print(f"  🆔 地震編號: {eq.get('EarthquakeNo')}")
                print(f"  📄 報告類型: {eq.get('ReportType')}")
                print(f"  🎨 報告顏色: {eq.get('ReportColor')}")
                print(f"  📝 報告內容: {eq.get('ReportContent')}")
                print(f"  🖼️  報告圖片: {eq.get('ReportImageURI')}")
                print(f"  🌊 震波圖片: {eq.get('ShakemapImageURI')}")
                print(f"  📝 備註: {eq.get('ReportRemark')}")
                print(f"  🔗 網頁連結: {eq.get('Web')}")
                
                eq_info = eq.get('EarthquakeInfo', {})
                print(f"\n📍 地震基本資訊:")
                print(f"  🕐 發生時間: {eq_info.get('OriginTime')}")
                print(f"  📏 深度: {eq_info.get('FocalDepth')} 公里")
                print(f"  📊 規模類型: {eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeType')}")
                print(f"  📊 規模數值: {eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue')}")
                print(f"  🌐 資料來源: {eq_info.get('Source')}")
                
                epicenter = eq_info.get('Epicenter', {})
                print(f"\n🎯 震央資訊:")
                print(f"  📍 位置描述: {epicenter.get('Location')}")
                print(f"  🌐 經度: {epicenter.get('EpicenterLongitude')}")
                print(f"  🌐 緯度: {epicenter.get('EpicenterLatitude')}")
                
                intensity = eq.get('Intensity', {})
                shaking_areas = intensity.get('ShakingArea', [])
                print(f"\n📈 震度資訊:")
                print(f"  🗺️  受震區域數量: {len(shaking_areas)}")
                
                if shaking_areas:
                    max_intensity_area = max(shaking_areas, 
                                           key=lambda x: int(x.get('AreaIntensity', '0級').replace('級', '')) 
                                           if x.get('AreaIntensity', '0級').replace('級', '').isdigit() else 0)
                    print(f"  📊 最大震度: {max_intensity_area.get('AreaIntensity')} ({max_intensity_area.get('CountyName')})")
                    
                    total_stations = sum(len(area.get('EqStation', [])) for area in shaking_areas)
                    print(f"  🏠 測站總數: {total_stations}")
        
    except Exception as e:
        print(f"❌ 分析地震資料時發生錯誤: {e}")

if __name__ == "__main__":
    # 執行地震 API 測試
    test_earthquake_api()
    
    # 顯示地震資料詳細結構
    display_earthquake_details()
