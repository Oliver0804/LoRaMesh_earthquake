#!/bin/bash
# 簡單的地震查詢 curl 腳本
# 快速取得最新一筆地震資料

# 從 .env 讀取 API Key
if [ -f ".env" ]; then
    export $(cat .env | grep -v '^#' | xargs)
fi

if [ -z "$CWA_KEY" ]; then
    echo "錯誤：請在 .env 檔案中設定 CWA_KEY"
    exit 1
fi

echo "正在取得最新地震資料..."

# curl 取得最新一筆地震 (limit=1)
curl -s "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001?Authorization=$CWA_KEY&format=JSON&limit=1&offset=0" | \
python3 -c "
import json
import sys

try:
    data = json.load(sys.stdin)
    
    if data.get('success') == 'true':
        earthquakes = data['records']['Earthquake']
        if earthquakes:
            eq = earthquakes[0]
            earthquake_info = eq.get('EarthquakeInfo', {})
            epicenter = earthquake_info.get('Epicenter', {})
            magnitude = earthquake_info.get('EarthquakeMagnitude', {})
            
            print('=== 最新地震資訊 ===')
            print(f'地震編號: {eq.get(\"EarthquakeNo\", \"N/A\")}')
            print(f'發生時間: {earthquake_info.get(\"OriginTime\", \"N/A\")}')
            print(f'位置: {epicenter.get(\"Location\", \"N/A\")}')
            print(f'規模: {magnitude.get(\"MagnitudeValue\", \"N/A\")}')
            print(f'深度: {earthquake_info.get(\"FocalDepth\", \"N/A\")} 公里')
            
            # 取得最大震度
            shaking_areas = eq.get('Intensity', {}).get('ShakingArea', [])
            max_intensity = '0級'
            for area in shaking_areas:
                intensity = area.get('AreaIntensity', '0級')
                if '4級' in intensity or '4級' == intensity:
                    max_intensity = '4級'
                    break
                elif '3級' in intensity or '3級' == intensity:
                    max_intensity = '3級'
                elif '2級' in intensity or '2級' == intensity:
                    if max_intensity == '0級' or max_intensity == '1級':
                        max_intensity = '2級'
                elif '1級' in intensity or '1級' == intensity:
                    if max_intensity == '0級':
                        max_intensity = '1級'
            
            print(f'最大震度: {max_intensity}')
            print(f'報告: {eq.get(\"ReportContent\", \"N/A\")}')
        else:
            print('沒有地震資料')
    else:
        print('API 呼叫失敗')
        
except Exception as e:
    print(f'處理資料時發生錯誤: {e}')
"
