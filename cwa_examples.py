#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中央氣象署 API 客戶端使用範例
CWA API Client Usage Examples
"""

import json
from datetime import datetime
from cwa_client import CWAClient, COUNTY_CODES

def print_json(data, title=""):
    """美化列印 JSON 資料"""
    if title:
        print(f"\n=== {title} ===")
    print(json.dumps(data, ensure_ascii=False, indent=2)[:500] + "..." if len(str(data)) > 500 else json.dumps(data, ensure_ascii=False, indent=2))

def main():
    """主程式範例"""
    try:
        # 建立 CWA 客戶端 (會自動從 .env 讀取 API 金鑰)
        client = CWAClient()
        
        print("🌤️  中央氣象署開放資料平臺 API 客戶端測試")
        print("=" * 50)
        
        # 1. 一般天氣預報範例
        print("\n📍 1. 一般天氣預報範例")
        print("-" * 30)
        
        # 取得臺北市天氣預報
        taipei_weather = client.get_city_weather('臺北市')
        if taipei_weather.get('success') == 'true':
            locations = taipei_weather.get('records', {}).get('location', [])
            for location in locations[:2]:  # 只顯示前2個地區
                print(f"地區: {location.get('locationName')}")
                weather_elements = location.get('weatherElement', [])
                for element in weather_elements[:1]:  # 只顯示第一個天氣要素
                    print(f"  要素: {element.get('elementName')}")
                    times = element.get('time', [])
                    for time_data in times[:2]:  # 只顯示前2個時間點
                        print(f"    時間: {time_data.get('startTime')} ~ {time_data.get('endTime')}")
                        print(f"    資料: {time_data.get('parameter', {}).get('parameterName')}")
        
        # 2. 鄉鎮天氣預報範例
        print("\n🏘️  2. 鄉鎮天氣預報範例")
        print("-" * 30)
        
        # 取得臺北市未來3天天氣預報
        taipei_3day = client.get_township_forecast_3days(
            county_code=COUNTY_CODES['臺北市_3天'],
            location_name='信義區'
        )
        
        if taipei_3day.get('success') == 'true':
            print("✅ 臺北市信義區未來3天天氣預報取得成功")
            print(f"資料筆數: {len(taipei_3day.get('records', {}).get('location', []))}")
        
        # 3. 地震資訊範例
        print("\n🌏 3. 地震資訊範例")
        print("-" * 30)
        
        # 取得最新地震報告
        earthquake_data = client.get_latest_earthquake()
        if earthquake_data.get('success') == 'true':
            earthquakes = earthquake_data.get('records', {}).get('earthquake', [])
            if earthquakes:
                latest_eq = earthquakes[0]
                print(f"最新地震時間: {latest_eq.get('earthquakeInfo', {}).get('originTime')}")
                print(f"震央位置: {latest_eq.get('earthquakeInfo', {}).get('epicenter', {}).get('location')}")
                print(f"規模: {latest_eq.get('earthquakeInfo', {}).get('magnitude', {}).get('magnitudeValue')}")
                print(f"深度: {latest_eq.get('earthquakeInfo', {}).get('depth', {}).get('value')} 公里")
        
        # 4. 觀測資料範例
        print("\n🌡️  4. 氣象觀測資料範例")
        print("-" * 30)
        
        # 取得氣象觀測資料
        weather_stations = client.get_weather_station_data()
        if weather_stations.get('success') == 'true':
            stations = weather_stations.get('records', {}).get('location', [])
            print(f"目前有 {len(stations)} 個氣象站提供觀測資料")
            
            # 顯示前3個氣象站的資料
            for station in stations[:3]:
                print(f"\n測站: {station.get('locationName')} ({station.get('stationId')})")
                elements = station.get('weatherElement', [])
                for element in elements[:3]:  # 只顯示前3個觀測要素
                    print(f"  {element.get('elementName')}: {element.get('elementValue')}")
        
        # 5. 天氣警特報範例
        print("\n⚠️  5. 天氣警特報範例")
        print("-" * 30)
        
        # 取得天氣警特報
        warnings = client.get_weather_warning_by_county()
        if warnings.get('success') == 'true':
            warning_records = warnings.get('records', [])
            if warning_records:
                print(f"目前有 {len(warning_records)} 個縣市有天氣警特報")
                for record in warning_records[:3]:  # 只顯示前3個
                    if isinstance(record, dict):
                        location = record.get('location', {})
                        print(f"地區: {location.get('locationName')}")
                        hazard_conditions = record.get('hazardConditions', {})
                        if isinstance(hazard_conditions, dict):
                            hazards = hazard_conditions.get('hazards', [])
                            if hazards:
                                for hazard in hazards[:2]:  # 只顯示前2個警報
                                    if isinstance(hazard, dict):
                                        print(f"  警報: {hazard.get('info')}")
            else:
                print("✅ 目前沒有天氣警特報")
        
        # 6. 健康氣象資訊範例
        print("\n🩺 6. 健康氣象資訊範例")
        print("-" * 30)
        
        # 取得熱傷害指數
        heat_index = client.get_heat_injury_index()
        if heat_index.get('success') == 'true':
            print("✅ 熱傷害指數資料取得成功")
            print(f"資料時間: {heat_index.get('records', {}).get('datasetDescription')}")
        
        # 7. 天文資料範例
        print("\n🌅 7. 天文資料範例")
        print("-" * 30)
        
        # 取得日出日沒時刻
        sunrise_sunset = client.get_sunrise_sunset()
        if sunrise_sunset.get('success') == 'true':
            locations = sunrise_sunset.get('records', {}).get('locations', {}).get('location', [])
            if locations:
                taipei_data = next((loc for loc in locations if '臺北' in loc.get('locationName', '')), None)
                if taipei_data:
                    times = taipei_data.get('time', [])
                    if times:
                        today_data = times[0]
                        print(f"臺北今日日出日沒時刻:")
                        print(f"  日期: {today_data.get('dataTime')}")
                        for parameter in today_data.get('parameter', []):
                            name = parameter.get('parameterName')
                            value = parameter.get('parameterValue')
                            if name in ['日出時刻', '日沒時刻']:
                                print(f"  {name}: {value}")
        
        # 8. 資料儲存範例
        print("\n💾 8. 資料儲存範例")
        print("-" * 30)
        
        # 儲存臺北市天氣預報到檔案
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"taipei_weather_{timestamp}.json"
        client.save_data_to_file(taipei_weather, filename)
        
        print("\n✅ 所有範例執行完成！")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

def demo_specific_functions():
    """特定功能演示"""
    try:
        client = CWAClient()
        
        print("\n🔧 特定功能演示")
        print("=" * 50)
        
        # 演示跨縣市查詢
        print("\n📋 跨縣市鄉鎮預報查詢")
        print("-" * 30)
        
        cross_county_data = client.get_cross_county_forecast([
            '中正區', '信義區', '大安區'  # 臺北市的3個區
        ])
        
        if cross_county_data.get('success') == 'true':
            print("✅ 跨縣市查詢成功")
            locations = cross_county_data.get('records', {}).get('location', [])
            for location in locations:
                print(f"  地區: {location.get('locationName')}")
        
        # 演示不同語言的地震報告
        print("\n🌍 多語言地震報告")
        print("-" * 30)
        
        # 中文地震報告
        eq_zh = client.get_significant_earthquake_report(language='zh')
        print("✅ 中文地震報告取得成功" if eq_zh.get('success') == 'true' else "❌ 中文地震報告取得失敗")
        
        # 英文地震報告
        eq_en = client.get_significant_earthquake_report(language='en')
        print("✅ 英文地震報告取得成功" if eq_en.get('success') == 'true' else "❌ 英文地震報告取得失敗")
        
        # 演示海象資料
        print("\n🌊 海象監測資料")
        print("-" * 30)
        
        marine_48h = client.get_marine_data_48h()
        marine_30d = client.get_marine_data_30d()
        
        print("✅ 48小時海象資料取得成功" if marine_48h.get('success') == 'true' else "❌ 48小時海象資料取得失敗")
        print("✅ 30天海象資料取得成功" if marine_30d.get('success') == 'true' else "❌ 30天海象資料取得失敗")
        
        print("\n✅ 特定功能演示完成！")
        
    except Exception as e:
        print(f"❌ 錯誤: {e}")

if __name__ == "__main__":
    # 執行主要範例
    main()
    
    # 執行特定功能演示
    demo_specific_functions()
    
    print("\n" + "=" * 50)
    print("🎉 所有測試完成！")
    print("💡 你可以根據需要修改這些範例來符合你的使用情境。")
    print("📖 更多 API 詳細資訊請參考 cwa_api.md")
