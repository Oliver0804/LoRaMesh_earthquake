# 中央氣象署 API 客戶端使用說明

## 📋 檔案說明

- **`cwa_client.py`** - 主要的 API 客戶端類別，提供所有 CWA API 功能
- **`cwa_examples.py`** - 完整的使用範例程式
- **`simple_weather_demo.py`** - 簡單易用的天氣查詢演示
- **`.env`** - 存放 API 金鑰的環境變數檔案

## 🚀 快速開始

### 1. 確認 API 金鑰

你的 API 金鑰已經設定在 `.env` 檔案中：
```
CWA_API_KEY=你的_API_金鑰
```

### 2. 安裝依賴套件

```bash
pip install requests python-dotenv
```

### 3. 基本使用

```python
from cwa_client import CWAClient

# 建立客戶端 (會自動從 .env 讀取 API 金鑰)
client = CWAClient()

# 取得臺北市天氣預報
weather_data = client.get_city_weather('臺北市')
print(weather_data)
```

## 📚 主要功能

### 🌤️ 天氣預報

```python
# 一般天氣預報 (36小時)
weather = client.get_general_forecast(location_name='臺北市')

# 鄉鎮天氣預報 (3天)
township_3day = client.get_township_forecast_3days('061', location_name='信義區')

# 鄉鎮天氣預報 (1週)
township_week = client.get_township_forecast_week('063', location_name='信義區')

# 全臺灣天氣預報
taiwan_weather = client.get_all_taiwan_forecast_3days()
```

### 🌏 地震資訊

```python
# 最新地震報告 (中文)
earthquake_zh = client.get_significant_earthquake_report('zh')

# 最新地震報告 (英文)  
earthquake_en = client.get_significant_earthquake_report('en')

# 小區域地震報告
local_earthquake = client.get_local_earthquake_report()

# 海嘯資訊
tsunami = client.get_tsunami_info()
```

### 🌡️ 觀測資料

```python
# 氣象觀測資料
weather_stations = client.get_weather_station_data()

# 雨量觀測資料
rainfall = client.get_rainfall_station_data()

# 現在天氣觀測報告
current_weather = client.get_current_weather_report()

# 紫外線指數
uv_index = client.get_uv_index()
```

### ⚠️ 天氣警特報

```python
# 各縣市天氣警特報
warnings_by_county = client.get_weather_warning_by_county()

# 天氣警特報內容
warning_content = client.get_weather_warning_content()

# 颱風資訊
typhoon_info = client.get_typhoon_info()
```

### 🌊 海象資料

```python
# 48小時海象監測
marine_48h = client.get_marine_data_48h()

# 30天海象監測
marine_30d = client.get_marine_data_30d()
```

### 🩺 健康氣象

```python
# 熱傷害指數
heat_injury = client.get_heat_injury_index()

# 冷傷害指數 (5天)
cold_injury_5d = client.get_cold_injury_index_5day()

# 溫差提醒指數
temp_diff = client.get_temperature_diff_index_5day()
```

### 🌅 天文資料

```python
# 日出日沒時刻
sunrise_sunset = client.get_sunrise_sunset()

# 月出月沒時刻
moonrise_moonset = client.get_moonrise_moonset()

# 潮汐預報
tide_forecast = client.get_tide_forecast()
```

## 🗺️ 縣市代碼對照

### 3天預報代碼
- 宜蘭縣: `001`
- 臺北市: `061`
- 新北市: `069`
- 桃園市: `005`
- 新竹市: `053`
- 新竹縣: `009`
- 苗栗縣: `013`
- 臺中市: `073`
- 彰化縣: `017`
- 南投縣: `021`
- 雲林縣: `025`
- 嘉義市: `057`
- 嘉義縣: `029`
- 臺南市: `077`
- 高雄市: `065`
- 屏東縣: `033`
- 臺東縣: `037`
- 花蓮縣: `041`
- 澎湖縣: `045`
- 基隆市: `049`
- 金門縣: `085`
- 連江縣: `081`

### 1週預報代碼
在3天預報代碼基礎上 +2，例如：
- 臺北市1週: `063`
- 高雄市1週: `067`

也可以使用 `COUNTY_CODES` 字典：
```python
from cwa_client import COUNTY_CODES

# 取得臺北市3天預報
code_3day = COUNTY_CODES['臺北市_3天']  # '061'

# 取得臺北市1週預報  
code_1week = COUNTY_CODES['臺北市_1週']  # '063'
```

## 💾 資料儲存

```python
# 儲存資料到 JSON 檔案
client.save_data_to_file(weather_data, 'weather_report.json')
```

## 🔧 進階使用

### 自訂參數查詢

```python
# 指定時間範圍的天氣預報
weather = client.get_general_forecast(
    location_name='臺北市',
    element_name='Wx,T,PoP',  # 天氣現象、溫度、降雨機率
    time_from='2025-06-24T00:00:00',
    time_to='2025-06-26T23:59:59'
)
```

### 跨縣市查詢

```python
# 同時查詢多個鄉鎮 (最多5個)
cross_county = client.get_cross_county_forecast([
    '中正區', '信義區', '大安區'
])
```

### 錯誤處理

```python
try:
    weather_data = client.get_city_weather('臺北市')
    if weather_data.get('success') == 'true':
        print("資料取得成功")
        # 處理資料
    else:
        print("API 回傳失敗")
except Exception as e:
    print(f"發生錯誤: {e}")
```

## 🚦 使用範例

### 執行基本測試
```bash
python3 cwa_client.py
```

### 執行完整範例
```bash
python3 cwa_examples.py
```

### 執行簡單演示
```bash
python3 simple_weather_demo.py
```

## 📈 API 回應格式

大部分 API 回應都包含以下結構：

```json
{
  "success": "true",
  "result": {
    "resource_id": "...",
    "fields": [...]
  },
  "records": {
    "datasetDescription": "...",
    "location": [...],  // 或其他資料結構
    ...
  }
}
```

## ⚡ 效能提示

1. **快取機制**: 考慮實作資料快取以減少 API 呼叫次數
2. **錯誤重試**: 實作自動重試機制處理網路暫時問題
3. **異步處理**: 對於大量資料查詢，可考慮使用 `asyncio` 和 `aiohttp`

## 🔗 相關資源

- [中央氣象署開放資料平臺](https://opendata.cwa.gov.tw/)
- [API 文件](https://opendata.cwa.gov.tw/dist/opendata-swagger.html)
- [資料使用說明](https://opendata.cwa.gov.tw/opendatadoc)

## 🐛 常見問題

### Q: API 金鑰無效？
A: 請確認 `.env` 檔案中的 `CWA_KEY` 是否正確，並確保金鑰未過期。

### Q: 某些 API 沒有資料？
A: 部分 API 在特定時間可能沒有資料，例如地震資料在無地震時會回傳空陣列。

### Q: 如何取得更多氣象要素？
A: 在查詢時使用 `element_name` 參數指定需要的氣象要素，以逗號分隔多個要素。

---

🎉 現在你已經可以使用這個 CWA API 客戶端來獲取各種氣象資訊了！
