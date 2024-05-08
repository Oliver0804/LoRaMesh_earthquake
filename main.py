import requests
import time
import os
import json

from datetime import datetime
def load_config():
    try:
        with open('./config.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print("Config file not found, using default settings.")
        return {
            "Authorization": "Your_Default_Authorization_Key",
            "limit": 1,
            "offset": 0,
            "format": "JSON",
            "magnitude_threshold": 1
        }

def fetch_earthquake_data(last_origin_time, config):
    url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"
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
        try:
            if data['success']:
                earthquake = data['records']['Earthquake'][0]
                current_origin_time = earthquake['EarthquakeInfo']['OriginTime']
                if current_origin_time != last_origin_time:
                    print_earthquake_details(earthquake)
                    if earthquake['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                        send_meshtastic_message(earthquake['ReportContent'])
                    return current_origin_time
                else:
                    print("No new earthquake data. Current system time:", datetime.now())
                    return last_origin_time
            else:
                print("Failed to retrieve data:", data['message'])
                return last_origin_time
        except KeyError as e:
            print(f"Key Error: {e}")
            print("Data received:", data)
            return last_origin_time
    else:
        print("HTTP Error:", response.status_code)
        return last_origin_time

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

def send_meshtastic_message(report_content):
    command = f'meshtastic --sendtext "[測試中] {report_content}" --ch-index 2'
    os.system(command)
    print("Meshtastic message sent due to significant earthquake.")

def save_last_origin_time(last_origin_time):
    with open("./.lastData.txt", "w") as file:
        file.write(last_origin_time)

def load_last_origin_time():
    try:
        with open("./.lastData.txt", "r") as file:
            return file.read().strip()
    except FileNotFoundError:
        return None

def main():
    config = load_config()
    last_origin_time = load_last_origin_time()
    try:
        while True:
            last_origin_time = load_last_origin_time()  # Load the last origin time before each fetch
            print(f"Loaded last origin time: {last_origin_time}")
            new_origin_time = fetch_earthquake_data(last_origin_time, config)

            if new_origin_time != last_origin_time:
                save_last_origin_time(new_origin_time)  # Save the new origin time if it's different
                print(f"Saved new origin time: {new_origin_time}")
            time.sleep(15)
    except KeyboardInterrupt:
        print("Program terminated by user.")

if __name__ == "__main__":
    main()

