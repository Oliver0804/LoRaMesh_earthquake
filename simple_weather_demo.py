#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中央氣象署 API 客戶端簡單使用範例
Simple CWA API Client Usage Examples
"""

from cwa_client import CWAClient
import json

def simple_weather_demo():
    """簡單的天氣查詢演示"""
    print("🌤️  中央氣象署天氣資訊查詢")
    print("=" * 40)
    
    try:
        # 建立客戶端
        client = CWAClient()
        
        # 1. 查詢臺北市天氣
        print("\n📍 查詢臺北市天氣預報...")
        taipei_weather = client.get_city_weather('臺北市')
        
        if taipei_weather.get('success') == 'true':
            print("✅ 天氣資料取得成功")
            
            # 解析天氣資料
            locations = taipei_weather.get('records', {}).get('location', [])
            if locations:
                location = locations[0]
                print(f"地區: {location.get('locationName')}")
                
                weather_elements = location.get('weatherElement', [])
                for element in weather_elements:
                    element_name = element.get('elementName')
                    if element_name == 'Wx':  # 天氣現象
                        print(f"\n🌈 天氣現象:")
                        times = element.get('time', [])
                        for i, time_data in enumerate(times[:3]):  # 顯示前3個時段
                            start_time = time_data.get('startTime')
                            end_time = time_data.get('endTime')
                            weather = time_data.get('parameter', {}).get('parameterName')
                            print(f"  {i+1}. {start_time} ~ {end_time}: {weather}")
                    
                    elif element_name == 'T':  # 溫度
                        print(f"\n🌡️  溫度:")
                        times = element.get('time', [])
                        for i, time_data in enumerate(times[:3]):
                            start_time = time_data.get('startTime')
                            temp = time_data.get('parameter', {}).get('parameterName')
                            unit = time_data.get('parameter', {}).get('parameterUnit')
                            print(f"  {i+1}. {start_time}: {temp} {unit}")
                    
                    elif element_name == 'PoP':  # 降雨機率
                        print(f"\n☔ 降雨機率:")
                        times = element.get('time', [])
                        for i, time_data in enumerate(times[:3]):
                            start_time = time_data.get('startTime')
                            pop = time_data.get('parameter', {}).get('parameterName')
                            unit = time_data.get('parameter', {}).get('parameterUnit')
                            print(f"  {i+1}. {start_time}: {pop}{unit}")
        else:
            print("❌ 天氣資料取得失敗")
        
        # 2. 查詢地震資訊
        print("\n\n🌏 查詢最新地震資訊...")
        earthquake_data = client.get_latest_earthquake()
        
        if earthquake_data.get('success') == 'true':
            earthquakes = earthquake_data.get('records', {}).get('Earthquake', [])
            if earthquakes:
                print("✅ 地震資料取得成功")
                
                # 顯示最新地震資料
                eq = earthquakes[0]
                eq_info = eq.get('EarthquakeInfo', {})
                origin_time = eq_info.get('OriginTime')
                magnitude = eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue')
                location = eq_info.get('Epicenter', {}).get('Location')
                depth = eq_info.get('FocalDepth')
                report_content = eq.get('ReportContent')
                
                print(f"\n📍 最新地震資訊:")
                print(f"  時間: {origin_time}")
                print(f"  位置: {location}")
                print(f"  規模: M{magnitude}")
                print(f"  深度: {depth} 公里")
                print(f"  說明: {report_content}")
                
                # 顯示震度資訊
                intensity = eq.get('Intensity', {})
                shaking_areas = intensity.get('ShakingArea', [])
                if shaking_areas:
                    max_intensity_area = None
                    max_intensity_value = 0
                    
                    for area in shaking_areas:
                        area_intensity = area.get('AreaIntensity', '0級')
                        try:
                            intensity_num = int(area_intensity.replace('級', ''))
                            if intensity_num > max_intensity_value:
                                max_intensity_value = intensity_num
                                max_intensity_area = area
                        except:
                            pass
                    
                    if max_intensity_area:
                        county = max_intensity_area.get('CountyName', '未知')
                        max_intensity = max_intensity_area.get('AreaIntensity', '未知')
                        print(f"  最大震度: {county} {max_intensity}")
                
                # 顯示更多地震資料
                print(f"\n🔗 詳細資訊: {eq.get('Web', '無')}")
                print(f"🖼️  地震報告圖: {eq.get('ReportImageURI', '無')}")
            else:
                print("ℹ️  目前無地震資料")
        else:
            print("❌ 地震資料取得失敗")
        
        # 3. 查詢氣象觀測
        print("\n\n🌡️  查詢氣象觀測資料...")
        weather_stations = client.get_weather_station_data()
        
        if weather_stations.get('success') == 'true':
            stations = weather_stations.get('records', {}).get('location', [])
            if stations:
                print(f"✅ 取得 {len(stations)} 個氣象站觀測資料")
                
                # 顯示前3個氣象站的重要資料
                for i, station in enumerate(stations[:3]):
                    station_name = station.get('locationName')
                    station_id = station.get('stationId')
                    print(f"\n🏠 氣象站 {i+1}: {station_name} ({station_id})")
                    
                    elements = station.get('weatherElement', [])
                    for element in elements:
                        element_name = element.get('elementName')
                        element_value = element.get('elementValue')
                        
                        # 只顯示重要的觀測項目
                        if element_name == 'TEMP':  # 溫度
                            print(f"  🌡️  溫度: {element_value}°C")
                        elif element_name == 'HUMD':  # 濕度
                            print(f"  💧 濕度: {element_value}%")
                        elif element_name == 'PRES':  # 氣壓
                            print(f"  📏 氣壓: {element_value} hPa")
                        elif element_name == 'WDIR':  # 風向
                            print(f"  🧭 風向: {element_value}°")
                        elif element_name == 'WDSD':  # 風速
                            print(f"  💨 風速: {element_value} m/s")
            else:
                print("ℹ️  目前無氣象觀測資料")
        else:
            print("❌ 氣象觀測資料取得失敗")
        
        # 4. 查詢天氣警特報
        print("\n\n⚠️  查詢天氣警特報...")
        try:
            warnings = client.get_weather_warning_by_county()
            
            if warnings.get('success') == 'true':
                warning_locations = warnings.get('records', {}).get('location', [])
                if warning_locations:
                    # 計算有警特報的縣市
                    active_warnings = []
                    for location in warning_locations:
                        hazards = location.get('hazardConditions', {}).get('hazards', [])
                        if hazards:  # 如果有危險條件
                            active_warnings.append(location)
                    
                    if active_warnings:
                        print(f"⚠️  目前有天氣警特報 (共 {len(active_warnings)} 個縣市)")
                        for i, location in enumerate(active_warnings[:5]):  # 顯示前5項
                            location_name = location.get('locationName', '未知縣市')
                            print(f"\n📋 {location_name}:")
                            hazards = location.get('hazardConditions', {}).get('hazards', [])
                            for j, hazard in enumerate(hazards[:3]):  # 顯示前3個警報
                                info = hazard.get('info', {})
                                valid_time = hazard.get('validTime', {})
                                
                                phenomena = info.get('phenomena', '未知現象')
                                significance = info.get('significance', '未知')
                                start_time = valid_time.get('startTime', '未知時間')
                                end_time = valid_time.get('endTime', '未知時間')
                                
                                print(f"  {j+1}. {phenomena}{significance}")
                                print(f"     有效時間: {start_time} ~ {end_time}")
                    else:
                        print("✅ 目前沒有天氣警特報")
                else:
                    print("✅ 目前沒有天氣警特報")
            else:
                print("✅ 目前沒有天氣警特報")
        except Exception as warning_e:
            print(f"⚠️  警特報查詢發生錯誤: {warning_e}")
        
    except Exception as e:
        print(f"❌ 程式執行錯誤: {e}")

def save_weather_data():
    """儲存天氣資料到檔案"""
    print("\n\n💾 儲存天氣資料到檔案...")
    
    try:
        client = CWAClient()
        
        # 取得臺北市天氣資料
        taipei_weather = client.get_city_weather('臺北市')
        
        if taipei_weather.get('success') == 'true':
            # 儲存到 JSON 檔案
            from datetime import datetime
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"taipei_weather_{timestamp}.json"
            
            client.save_data_to_file(taipei_weather, filename)
            print(f"✅ 天氣資料已儲存到 {filename}")
        else:
            print("❌ 無法取得天氣資料")
            
    except Exception as e:
        print(f"❌ 儲存資料時發生錯誤: {e}")

def main():
    """主程式"""
    # 執行簡單的天氣查詢演示
    simple_weather_demo()
    
    # 儲存天氣資料
    save_weather_data()
    
    print("\n" + "=" * 40)
    print("🎉 查詢完成！")
    print("💡 更多功能請參考 cwa_client.py 和 cwa_examples.py")

if __name__ == "__main__":
    main()
