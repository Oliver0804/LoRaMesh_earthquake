#!/bin/bash
# CWA 地震 API curl 測試腳本
# 取得最新一筆地震資料

# 讀取 API Key
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
else
    echo "錯誤：找不到 .env 檔案"
    exit 1
fi

if [ -z "$CWA_KEY" ]; then
    echo "錯誤：.env 檔案中未設定 CWA_KEY"
    exit 1
fi

echo "=== 使用 curl 取得最新地震資料 ==="
echo "API URL: https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"
echo "參數: limit=1, offset=0"
echo ""

# 使用 curl 取得最新一筆地震資料
echo "正在查詢..."
response=$(curl -s "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=$CWA_KEY&format=JSON&limit=1&offset=0")

# 檢查是否成功
if [ $? -eq 0 ]; then
    echo "✓ API 呼叫成功"
    echo ""
    
    # 儲存完整回應到檔案
    timestamp=$(date +"%Y%m%d_%H%M%S")
    output_file="earthquake_curl_${timestamp}.json"
    echo "$response" > "$output_file"
    echo "✓ 完整回應已儲存到: $output_file"
    echo ""
    
    # 解析並顯示重要資訊
    echo "=== 最新地震資訊 ==="
    
    # 使用 Python 來解析 JSON 檔案並顯示重要資訊
    python3 -c "
import json

try:
    with open('$output_file', 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    if data.get('success') == 'true':
        earthquakes = data['records']['Earthquake']
        if earthquakes:
            eq = earthquakes[0]
            print(f'地震編號: {eq.get(\"EarthquakeNo\", \"N/A\")}')
            print(f'報告類型: {eq.get(\"ReportType\", \"N/A\")}')
            print(f'發生時間: {eq.get(\"EarthquakeInfo\", {}).get(\"OriginTime\", \"N/A\")}')
            print(f'位置: {eq.get(\"EarthquakeInfo\", {}).get(\"Epicenter\", {}).get(\"Location\", \"N/A\")}')
            print(f'規模: {eq.get(\"EarthquakeInfo\", {}).get(\"EarthquakeMagnitude\", {}).get(\"MagnitudeValue\", \"N/A\")}')
            print(f'深度: {eq.get(\"EarthquakeInfo\", {}).get(\"FocalDepth\", \"N/A\")} 公里')
            
            # 找出最大震度
            max_intensity = '0級'
            shaking_areas = eq.get('Intensity', {}).get('ShakingArea', [])
            for area in shaking_areas:
                intensity = area.get('AreaIntensity', '0級')
                if '4級' in intensity:
                    max_intensity = '4級'
                elif '3級' in intensity and '4級' not in max_intensity:
                    max_intensity = '3級'
                elif '2級' in intensity and '3級' not in max_intensity and '4級' not in max_intensity:
                    max_intensity = '2級'
                elif '1級' in intensity and '2級' not in max_intensity and '3級' not in max_intensity and '4級' not in max_intensity:
                    max_intensity = '1級'
            
            print(f'最大震度: {max_intensity}')
            print(f'報告內容: {eq.get(\"ReportContent\", \"N/A\")}')
            print(f'詳細資訊: {eq.get(\"Web\", \"N/A\")}')
            print('')
            
            # 顯示受影響地區
            print('=== 受影響地區 ===')
            for area in shaking_areas[:5]:  # 只顯示前5個地區
                print(f'{area.get(\"CountyName\", \"未知縣市\")}: {area.get(\"AreaIntensity\", \"未知\")}')
            
            if len(shaking_areas) > 5:
                print(f'...等共 {len(shaking_areas)} 個地區')
                
        else:
            print('沒有地震資料')
    else:
        print('API 呼叫失敗')
        print(f'錯誤訊息: {data}')
        
except Exception as e:
    print(f'解析 JSON 時發生錯誤: {e}')
"
    
else
    echo "✗ API 呼叫失敗"
    echo "請檢查網路連線和 API Key"
fi

echo ""
echo "=== 其他可用的 curl 指令 ==="
echo "取得最新 5 筆地震:"
echo "curl -s \"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=\$CWA_KEY&format=JSON&limit=5&offset=0\""
echo ""
echo "取得小區域地震報告:"
echo "curl -s \"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001?Authorization=\$CWA_KEY&format=JSON&limit=1\""
echo ""
echo "取得英文地震報告:"
echo "curl -s \"https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-002?Authorization=\$CWA_KEY&format=JSON&limit=1\""
