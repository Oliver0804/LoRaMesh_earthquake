#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
中央氣象署開放資料平臺 API 客戶端
Central Weather Administration (CWA) Open Data API Client

提供以下功能：
- 天氣預報 (一般天氣預報、鄉鎮天氣預報)
- 觀測資料 (氣象、雨量、海象等)
- 地震海嘯資訊
- 天氣警特報
- 氣候資料
- 天文資料
"""

import os
import requests
import json
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Union
from dotenv import load_dotenv

# 載入環境變數
load_dotenv()

class CWAClient:
    """中央氣象署 API 客戶端"""
    
    BASE_URL = "https://opendata.cwa.gov.tw/api"
    
    def __init__(self, api_key: Optional[str] = None):
        """
        初始化 CWA API 客戶端
        
        Args:
            api_key: API 金鑰，如果未提供會從環境變數 CWA_KEY 讀取
        """
        self.api_key = api_key or os.getenv('CWA_KEY')
        if not self.api_key:
            raise ValueError("請提供 API 金鑰或在 .env 檔案中設定 CWA_KEY")
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict:
        """
        發送 API 請求
        
        Args:
            endpoint: API 端點
            params: 查詢參數
            
        Returns:
            API 響應的 JSON 資料
        """
        url = f"{self.BASE_URL}{endpoint}"
        
        # 設定預設參數
        default_params = {
            'Authorization': self.api_key,
            'format': 'JSON'
        }
        
        if params:
            default_params.update(params)
        
        try:
            response = requests.get(url, params=default_params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            raise Exception(f"API 請求失敗: {e}")
    
    # ===========================================
    # 天氣預報相關 API
    # ===========================================
    
    def get_general_forecast(self, location_name: Optional[str] = None, 
                           element_name: Optional[str] = None,
                           start_time: Optional[str] = None,
                           time_from: Optional[str] = None,
                           time_to: Optional[str] = None) -> Dict:
        """
        取得一般天氣預報-今明 36 小時天氣預報
        
        Args:
            location_name: 地區名稱
            element_name: 氣象要素名稱
            start_time: 起始時間
            time_from: 起始時間 (格式: YYYY-MM-DDTHH:MM:SS)
            time_to: 結束時間 (格式: YYYY-MM-DDTHH:MM:SS)
            
        Returns:
            天氣預報資料
        """
        params = {}
        if location_name:
            params['locationName'] = location_name
        if element_name:
            params['elementName'] = element_name
        if start_time:
            params['startTime'] = start_time
        if time_from:
            params['timeFrom'] = time_from
        if time_to:
            params['timeTo'] = time_to
            
        return self._make_request('/v1/rest/datastore/F-C0032-001', params)
    
    def get_township_forecast_3days(self, county_code: str, 
                                   location_name: Optional[str] = None,
                                   element_name: Optional[str] = None) -> Dict:
        """
        取得鄉鎮未來3天天氣預報
        
        Args:
            county_code: 縣市代碼 (如: '001'=宜蘭縣, '061'=臺北市, '065'=高雄市等)
            location_name: 鄉鎮名稱
            element_name: 氣象要素名稱
            
        Returns:
            鄉鎮天氣預報資料
        """
        endpoint = f'/v1/rest/datastore/F-D0047-{county_code}'
        params = {}
        if location_name:
            params['LocationName'] = location_name
        if element_name:
            params['ElementName'] = element_name
            
        return self._make_request(endpoint, params)
    
    def get_township_forecast_week(self, county_code: str,
                                  location_name: Optional[str] = None,
                                  element_name: Optional[str] = None) -> Dict:
        """
        取得鄉鎮未來1週天氣預報
        
        Args:
            county_code: 縣市代碼 (如: '003'=宜蘭縣1週, '063'=臺北市1週等)
            location_name: 鄉鎮名稱
            element_name: 氣象要素名稱
            
        Returns:
            鄉鎮天氣預報資料
        """
        endpoint = f'/v1/rest/datastore/F-D0047-{county_code}'
        params = {}
        if location_name:
            params['LocationName'] = location_name
        if element_name:
            params['ElementName'] = element_name
            
        return self._make_request(endpoint, params)
    
    def get_all_taiwan_forecast_3days(self) -> Dict:
        """取得全臺灣未來3天天氣預報"""
        return self._make_request('/v1/rest/datastore/F-D0047-089')
    
    def get_all_taiwan_forecast_week(self) -> Dict:
        """取得全臺灣未來1週天氣預報"""
        return self._make_request('/v1/rest/datastore/F-D0047-091')
    
    def get_cross_county_forecast(self, location_names: List[str]) -> Dict:
        """
        取得跨縣市鄉鎮預報資料 (最多5個，最少1個)
        
        Args:
            location_names: 鄉鎮名稱列表
            
        Returns:
            跨縣市鄉鎮預報資料
        """
        if len(location_names) > 5 or len(location_names) < 1:
            raise ValueError("鄉鎮數量必須在1-5個之間")
            
        params = {'LocationName': ','.join(location_names)}
        return self._make_request('/v1/rest/datastore/F-D0047-093', params)
    
    # ===========================================
    # 觀測資料相關 API
    # ===========================================
    
    def get_weather_station_data(self) -> Dict:
        """取得自動氣象站-氣象觀測資料"""
        return self._make_request('/v1/rest/datastore/O-A0001-001')
    
    def get_rainfall_station_data(self) -> Dict:
        """取得自動雨量站-雨量觀測資料"""
        return self._make_request('/v1/rest/datastore/O-A0002-001')
    
    def get_current_weather_report(self) -> Dict:
        """取得現在天氣觀測報告"""
        return self._make_request('/v1/rest/datastore/O-A0003-001')
    
    def get_uv_index(self) -> Dict:
        """取得紫外線指數-每日紫外線指數最大值"""
        return self._make_request('/v1/rest/datastore/O-A0005-001')
    
    def get_ozone_data(self) -> Dict:
        """取得臭氧總量觀測資料-台北站"""
        return self._make_request('/v1/rest/datastore/O-A0006-002')
    
    def get_marine_data_48h(self) -> Dict:
        """取得海象監測資料-48小時浮標站與潮位站海況監測資料"""
        return self._make_request('/v1/rest/datastore/O-B0075-001')
    
    def get_marine_data_30d(self) -> Dict:
        """取得海象監測資料-30天浮標站與潮位站海況監測資料"""
        return self._make_request('/v1/rest/datastore/O-B0075-002')
    
    # ===========================================
    # 地震海嘯相關 API
    # ===========================================
    
    def get_tsunami_info(self) -> Dict:
        """取得海嘯資訊資料"""
        return self._make_request('/v1/rest/datastore/E-A0014-001')
    
    def get_significant_earthquake_report(self, language: str = 'zh', limit: int = 5, offset: int = 0) -> Dict:
        """
        取得顯著有感地震報告
        
        Args:
            language: 語言 ('zh' 中文, 'en' 英文)
            limit: 限制回傳筆數 (預設 5 筆)
            offset: 偏移量 (預設 0)
            
        Returns:
            顯著有感地震報告資料
        """
        endpoint = '/v1/rest/datastore/E-A0015-001' if language == 'zh' else '/v1/rest/datastore/E-A0015-002'
        params = {
            'limit': limit,
            'offset': offset
        }
        return self._make_request(endpoint, params)
    
    def get_local_earthquake_report(self, language: str = 'zh', limit: int = 5, offset: int = 0) -> Dict:
        """
        取得小區域有感地震報告
        
        Args:
            language: 語言 ('zh' 中文, 'en' 英文)
            limit: 限制回傳筆數 (預設 5 筆)
            offset: 偏移量 (預設 0)
            
        Returns:
            小區域有感地震報告資料
        """
        endpoint = '/v1/rest/datastore/E-A0016-001' if language == 'zh' else '/v1/rest/datastore/E-A0016-002'
        params = {
            'limit': limit,
            'offset': offset
        }
        return self._make_request(endpoint, params)
    
    # ===========================================
    # 天氣警特報相關 API
    # ===========================================
    
    def get_weather_warning_by_county(self) -> Dict:
        """取得天氣特報-各別縣市地區目前之天氣警特報情形"""
        return self._make_request('/v1/rest/datastore/W-C0033-001')
    
    def get_weather_warning_content(self) -> Dict:
        """取得天氣特報-各別天氣警特報之內容及所影響之區域"""
        return self._make_request('/v1/rest/datastore/W-C0033-002')
    
    def get_typhoon_info(self) -> Dict:
        """取得颱風消息與警報-熱帶氣旋路徑"""
        return self._make_request('/v1/rest/datastore/W-C0034-005')
    
    # ===========================================
    # 氣候資料相關 API
    # ===========================================
    
    def get_daily_rainfall(self) -> Dict:
        """取得每日雨量-地面測站每日雨量資料"""
        return self._make_request('/v1/rest/datastore/C-B0025-001')
    
    def get_monthly_average(self) -> Dict:
        """取得月平均-地面測站資料"""
        return self._make_request('/v1/rest/datastore/C-B0027-001')
    
    def get_manned_station_info(self) -> Dict:
        """取得氣象測站基本資料-有人氣象測站基本資料"""
        return self._make_request('/v1/rest/datastore/C-B0074-001')
    
    def get_automatic_station_info(self) -> Dict:
        """取得氣象測站基本資料-無人氣象測站基本資料"""
        return self._make_request('/v1/rest/datastore/C-B0074-002')
    
    # ===========================================
    # 健康氣象相關 API
    # ===========================================
    
    def get_cold_injury_index_5day(self) -> Dict:
        """取得健康氣象冷傷害指數及警示全臺各鄉鎮五日預報"""
        return self._make_request('/v1/rest/datastore/F-A0085-002')
    
    def get_cold_injury_index_72h(self) -> Dict:
        """取得健康氣象冷傷害指數及警示全臺各鄉鎮未來72小時逐3小時預報"""
        return self._make_request('/v1/rest/datastore/F-A0085-003')
    
    def get_temperature_diff_index_5day(self) -> Dict:
        """取得健康氣象溫差提醒指數及警示全臺各鄉鎮五日預報"""
        return self._make_request('/v1/rest/datastore/F-A0085-004')
    
    def get_temperature_diff_index_72h(self) -> Dict:
        """取得健康氣象溫差提醒指數及警示全臺各鄉鎮未來72小時逐3小時預報"""
        return self._make_request('/v1/rest/datastore/F-A0085-005')
    
    def get_heat_injury_index(self) -> Dict:
        """取得健康氣象-熱傷害指數及警示全台各鄉鎮五日逐三小時預報"""
        return self._make_request('/v1/rest/datastore/M-A0085-001')
    
    # ===========================================
    # 天文資料相關 API
    # ===========================================
    
    def get_sunrise_sunset(self) -> Dict:
        """取得日出日沒時刻-全臺各縣市年度逐日日出日沒時刻資料"""
        return self._make_request('/v1/rest/datastore/A-B0062-001')
    
    def get_moonrise_moonset(self) -> Dict:
        """取得月出月沒時刻-全臺各縣市年度逐日月出月沒時刻資料"""
        return self._make_request('/v1/rest/datastore/A-B0063-001')
    
    def get_tide_forecast(self) -> Dict:
        """取得潮汐預報-未來 1 個月潮汐預報"""
        return self._make_request('/v1/rest/datastore/F-A0021-001')
    
    # ===========================================
    # 便利方法
    # ===========================================
    
    def get_city_weather(self, city_name: str) -> Dict:
        """
        取得指定城市的天氣預報 (便利方法)
        
        Args:
            city_name: 城市名稱 (如: '臺北市', '高雄市', '臺中市' 等)
            
        Returns:
            該城市的天氣預報資料
        """
        return self.get_general_forecast(location_name=city_name)
    
    def get_latest_earthquake(self, count: int = 1) -> Dict:
        """取得最新地震資訊 (便利方法)"""
        return self.get_significant_earthquake_report(limit=count, offset=0)
    
    def save_data_to_file(self, data: Dict, filename: str) -> None:
        """
        將資料儲存到 JSON 檔案
        
        Args:
            data: 要儲存的資料
            filename: 檔案名稱
        """
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"資料已儲存到 {filename}")


# ===========================================
# 縣市代碼對照表
# ===========================================

COUNTY_CODES = {
    # 3天預報代碼
    '宜蘭縣_3天': '001',
    '桃園市_3天': '005',
    '新竹縣_3天': '009',
    '苗栗縣_3天': '013',
    '彰化縣_3天': '017',
    '南投縣_3天': '021',
    '雲林縣_3天': '025',
    '嘉義縣_3天': '029',
    '屏東縣_3天': '033',
    '臺東縣_3天': '037',
    '花蓮縣_3天': '041',
    '澎湖縣_3天': '045',
    '基隆市_3天': '049',
    '新竹市_3天': '053',
    '嘉義市_3天': '057',
    '臺北市_3天': '061',
    '高雄市_3天': '065',
    '新北市_3天': '069',
    '臺中市_3天': '073',
    '臺南市_3天': '077',
    '連江縣_3天': '081',
    '金門縣_3天': '085',
    
    # 1週預報代碼
    '宜蘭縣_1週': '003',
    '桃園市_1週': '007',
    '新竹縣_1週': '011',
    '苗栗縣_1週': '015',
    '彰化縣_1週': '019',
    '南投縣_1週': '023',
    '雲林縣_1週': '027',
    '嘉義縣_1週': '031',
    '屏東縣_1週': '035',
    '臺東縣_1週': '039',
    '花蓮縣_1週': '043',
    '澎湖縣_1週': '047',
    '基隆市_1週': '051',
    '新竹市_1週': '055',
    '嘉義市_1週': '059',
    '臺北市_1週': '063',
    '高雄市_1週': '067',
    '新北市_1週': '071',
    '臺中市_1週': '075',
    '臺南市_1週': '079',
    '連江縣_1週': '083',
    '金門縣_1週': '087',
}


if __name__ == "__main__":
    # 使用範例
    try:
        # 建立 CWA 客戶端
        client = CWAClient()
        
        print("=== 中央氣象署 API 客戶端測試 ===\n")
        
        # 測試一般天氣預報
        print("1. 取得臺北市天氣預報...")
        taipei_weather = client.get_city_weather('臺北市')
        print(f"取得 {len(taipei_weather.get('records', {}).get('location', []))} 個地區的資料")
        
        # 測試地震資訊
        print("\n2. 取得最新地震資訊...")
        earthquake_data = client.get_latest_earthquake()
        earthquakes = earthquake_data.get('records', {}).get('Earthquake', [])
        print(f"取得 {len(earthquakes)} 筆地震資料")
        if earthquakes:
            eq = earthquakes[0]
            eq_info = eq.get('EarthquakeInfo', {})
            print(f"最新地震: {eq_info.get('OriginTime')} | {eq_info.get('Epicenter', {}).get('Location')} | M{eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue')}")
        
        # 測試觀測資料
        print("\n3. 取得氣象觀測資料...")
        weather_station_data = client.get_weather_station_data()
        print(f"取得 {len(weather_station_data.get('records', {}).get('location', []))} 個氣象站資料")
        
        # 測試天氣警特報
        print("\n4. 取得天氣警特報...")
        warning_data = client.get_weather_warning_by_county()
        print("天氣警特報資料取得完成")
        
        print("\n=== 測試完成 ===")
        
    except Exception as e:
        print(f"錯誤: {e}")
