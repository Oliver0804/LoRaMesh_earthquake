import requests
import time
import os
import json
from datetime import datetime

def load_config():
    config_path = './config.json'
    default_config = {
        "Authorization": "Your_Default_Authorization_Key",
        "limit": 1,
        "offset": 0,
        "format": "JSON",
        "magnitude_threshold": 1
    }
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            print("成功載入配置文件。")
            return config
    except FileNotFoundError:
        print("配置文件未找到，使用預設設定。")
        # Create the default config file if it doesn't exist
        with open(config_path, 'w') as file:
            json.dump(default_config, file)
            print("已創建預設配置文件。")
        return default_config

def load_last_origin_times():
    try:
        with open('./.lastData.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"small": None, "all": None}

def save_last_origin_times(origin_times):
    with open('./.lastData.json', 'w') as file:
        json.dump(origin_times, file)

def fetch_earthquake_data(url, last_origin_time, config):
    params = {
        'Authorization': config['Authorization'],
        'limit': config['limit'],
        'offset': config['offset'],
        'format': config['format']
    }
    headers = {'accept': 'application/json'}

    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        if data['success']:
            earthquake = data['records']['Earthquake'][0]
            current_origin_time = earthquake['EarthquakeInfo']['OriginTime']
            if current_origin_time != last_origin_time:
                print_earthquake_details(earthquake)
                return current_origin_time, earthquake
            else:
                print(f"{url}最近一次獲取時間:", datetime.now())
        else:
            print("Failed to retrieve data:", data['message'])
    else:
        print("HTTP Error:", response.status_code)
    return last_origin_time, None

def print_earthquake_details(earthquake):
    print("Earthquake Number:", earthquake['EarthquakeNo'])
    print("Report Type:", earthquake['ReportType'])
    print("Report Color:", earthquake['ReportColor'])
    print("Report Content:", earthquake['ReportContent'])
    print("Origin Time:", earthquake['EarthquakeInfo']['OriginTime'])
    print("Source:", earthquake['EarthquakeInfo']['Source'])
    print("Focal Depth:", earthquake['EarthquakeInfo']['FocalDepth'], "km")
    print("Epicenter Location:", earthquake['EarthquakeInfo']['Epicenter']['Location'])
    print("Epicenter Latitude:", earthquake['EarthquakeInfo']['Epicenter']['EpicenterLatitude'])
    print("Epicenter Longitude:", earthquake['EarthquakeInfo']['Epicenter']['EpicenterLongitude'])
    print("Magnitude Type:", earthquake['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeType'])
    print("Magnitude Value:", earthquake['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'])
def send_meshtastic_message(tip_msg, report_content):
    command = f'meshtastic --sendtext "[{tip_msg}] {report_content}" --ch-index 2'
    os.system(command)
    print(f"Meshtastic message sent: {tip_msg}")
def main():
    config = load_config()
    try:
        while True:
            # Load the latest origin times at the beginning of each iteration
            origin_times = load_last_origin_times()

            small_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001"
            all_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"
            
            new_origin_time_small, earthquake_small = fetch_earthquake_data(small_url, origin_times["small"], config)
            new_origin_time_all, earthquake_all = fetch_earthquake_data(all_url, origin_times["all"], config)
            
            updated = False
            if new_origin_time_small != origin_times["small"]:
                origin_times["small"] = new_origin_time_small
                updated = True
                if earthquake_small and earthquake_small['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                    send_meshtastic_message("Small Region", earthquake_small['ReportContent'])
            
            if new_origin_time_all != origin_times["all"]:
                origin_times["all"] = new_origin_time_all
                updated = True
                if earthquake_all and earthquake_all['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                    send_meshtastic_message("All Regions", earthquake_all['ReportContent'])
            
            if updated:
                save_last_origin_times(origin_times)
            else:
                #print(f"No new data updates. Last known origin times:")
                print(f"Small Region last origin time: {origin_times['small']}")
                print(f"All Regions last origin time: {origin_times['all']}")
            
            time.sleep(1)
    except KeyboardInterrupt:
        print("Program terminated by user.")
        
if __name__ == "__main__":
    main()