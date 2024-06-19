
import time
import os
import json
from datetime import datetime


import requests
import mysql.connector
from mysql.connector import Error
        
debugMode = True

def connect_db(config):
    try:
        print("正在嘗試連接到數據庫...")
        connection = mysql.connector.connect(
            host=config['db_host'],
            user=config['db_user'],
            password=config['db_password'],
            database=config['db_name']
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"成功連接到 MySQL 數據庫，MySQL 服務器版本：{db_info}")
            return connection
    except Error as e:
        print(f"數據庫連接失敗：{e}")
        return None
        

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



def save_last_origin_times_db(connection, last_origin_times_small, last_origin_times_all, last_issue_time_weather):
    if debugMode:
        print("保存起源时间到数据库...")
    if connection is not None:
        try:
            cursor = connection.cursor()
            update_query = """
            INSERT INTO origin_times (type, last_origin_time, last_checked_time)
            VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE 
            last_origin_time = VALUES(last_origin_time), 
            last_checked_time = VALUES(last_checked_time);
            """
            current_time = datetime.now()  # 获取当前时间

            # 更新 small 类型的地震时间
            cursor.execute(update_query, ('small', last_origin_times_small, current_time))
            # 更新 all 类型的地震时间
            cursor.execute(update_query, ('all', last_origin_times_all, current_time))
            # 更新天气时间
            cursor.execute(update_query, ('weather', last_issue_time_weather, current_time))

            connection.commit()
            print("Origin times updated in SQL.")
        except Error as e:
            print(f"Failed to update origin times in SQL: {e}")
        finally:
            cursor.close()
    else:
        print("No database always available.")


def read_last_origin_time_db(connection):
    if debugMode:
        print(" 从数据库读取起源时间...")
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT type, last_origin_time FROM origin_times;"  # 只选择需要的字段
            cursor.execute(select_query)
            origin_times = {}
            for (type, last_origin_time) in cursor:  # 在这里只解包两个字段
                origin_times[type] = last_origin_time
            print("Origin times read from SQL.")
            print(origin_times)
            return origin_times
        except Error as e:
            print(f"Failed to read origin times from SQL: {e}")
        finally:
            cursor.close()
            connection.commit()  # 提交事务
    else:
        print("No database connection available.")
        return None

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
                if debugMode:
                    print_earthquake_details(earthquake)
                return current_origin_time, earthquake
            else:
                if debugMode:
                    print(f"{url}最近一次獲取時間:", datetime.now())
        else:
            print("Failed to retrieve data:", data['message'])
    else:
        print("HTTP Error:", response.status_code)
    return last_origin_time, None


# def fetch_weather_data(url, last_issue_time, config):
#     params = {
#         'Authorization': config['Authorization'],
#         'limit': config['limit'],
#         'offset': config['offset'],
#         'format': config['format']
#     }
#     headers = {'accept': 'application/json'}
#     print("===========")
#     print(params)
#     print("===========")

#     response = requests.get(url, headers=headers, params=params)
#     if response.status_code == 200:
#         data = response.json()
#         if data['success']:
#             record = data['records']['record'][0]  # 取出第一条记录
#             current_issue_time = record['datasetInfo']['issueTime']
#             if current_issue_time != last_issue_time:
#                 content_text = record['contents']['content']['contentText'].strip().replace('\n', ' ')
#                 if debugMode:
#                     print_weather_details(record)
#                 return current_issue_time, content_text  # Correct variable name here
#             else:
#                 if debugMode:
#                     print(f"{url} 最近一次获取时间:", datetime.now())
#         else:
#             print("Failed to retrieve weather data:", data['message'])
#     else:
#         print("HTTP Error:", response.status_code)
#     return last_issue_time, None

def fetch_weather_data(url, retries=3):
    while retries > 0:
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') == 'true':
                return data['records']  # 返回解析好的记录部分
            else:
                print("Failed to retrieve data:", data.get('message'))
        else:
            print("HTTP Error:", response.status_code)
        retries -= 1
        print(f"Retrying... {retries} attempts left.")
    return None  # 如果尝试用完仍然失败，返回 None

# def parse_weather_data(records):
#     """Parses the weather data to extract and structure forecast information."""
#     forecast_summary = []
#     for location in records['location']:
#         location_name = location['locationName']
#         for element in location['weatherElement']:
#             element_name = element['elementName']  # 修正了此处的键名
#             for period in element['time']:
#                 start_time = period['startTime']
#                 end_time = period['endTime']
#                 parameter = period.get('parameter', {})
#                 forecast_summary.append({
#                     'location': location_name,
#                     'element': element_name,
#                     'start_time': start_time,
#                     'end_time': end_time,
#                     'parameter_name': parameter.get('parameterName', ''),
#                     'parameter_value': parameter.get('parameterValue', '')
#                 })
#     return forecast_summary
def parse_weather_data(records):
    """Parses the weather data to extract structured forecast information."""
    forecast_summary = {}
    for location in records['location']:
        location_name = location['locationName']
        forecast_summary[location_name] = {
            'MaxT': None,
            'MinT': None,
            'PoP': None,
            'CI': None
        }
        # 循环通过天气要素来寻找最高温、最低温、降雨机率和舒适度
        for element in location['weatherElement']:
            element_name = element['elementName']
            if element_name in ['MaxT', 'MinT', 'PoP', 'CI']:
                # 取每个要素的最后一个时间段的参数值
                last_period = element['time'][-1]  # 取最后一段时间
                parameter = last_period['parameter']
                forecast_summary[location_name][element_name] = parameter.get('parameterValue', parameter.get('parameterName', ''))
    
    return forecast_summary

def format_forecast(forecast_summary):
    """Formats the extracted forecast information into a specified string format."""
    formatted_forecasts = []
    for location, data in forecast_summary.items():
        formatted_forecast = f"近三日天氣預報{location}溫度{data['MinT']}~{data['MaxT']}度,降雨機率{data['PoP']}%：{data['CI']}"
        formatted_forecasts.append(formatted_forecast)
    return formatted_forecasts

def print_forecast(forecast):
    for item in forecast:
        print(f"{item['location']}: {item['element']} from {item['start_time']} to {item['end_time']}, {item['parameter_name']} {item['parameter_value']}")


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


def print_weather_details(record):
    print("Issue Time:", record['datasetInfo']['issueTime'])
    print("Start Time:", record['datasetInfo']['validTime']['startTime'])
    print("End Time:", record['datasetInfo']['validTime']['endTime'])
    print("Content Text:", record['contents']['content']['contentText'].strip().replace('\n', ' '))

def send_meshtastic_message(tip_msg, report_content):
    command = f'meshtastic --sendtext "[{tip_msg}] {report_content}" --ch-index 2'
    os.system(command)
    print(f"Meshtastic message sent: {tip_msg}")

def main():
    config = load_config()
    db_connection = connect_db(config)
    last_run_day = None  # 用于跟踪上次运行更新的日期

    try:
        while True:
            current_time = datetime.now()
            today_date = current_time.date()
            if db_connection is None or not db_connection.is_connected():
                print("数据库连接丢失，尝试重新连接...")
                db_connection = connect_db(config)
                if db_connection is None or not db_connection.is_connected():
                    print("重新连接失败，稍后再试...")
                    time.sleep(10)  # 等待10秒后再次尝试
                    continue
            
            origin_times = read_last_origin_time_db(db_connection)
            if origin_times is not None:
                last_small_time = str(origin_times.get('small', ''))
                last_all_time = str(origin_times.get('all', ''))
                last_weather_time = str(origin_times.get('weather', ''))  # Ensure this matches the database key

            small_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001"
            all_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"
            #weather_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/W-C0033-002"

            new_origin_time_small, earthquake_small = fetch_earthquake_data(small_url, last_small_time, config)
            new_origin_time_all, earthquake_all = fetch_earthquake_data(all_url, last_all_time, config)
            #new_weather_time, weather_content = fetch_weather_data(weather_url, last_weather_time, config)  # Correct function call


            updated = False
            if new_origin_time_small != last_small_time:
                print("Small Region Update Detected")
                last_small_time = new_origin_time_small
                updated = True
                if earthquake_small and earthquake_small['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                    print("Small Region", earthquake_small['ReportContent'])
                    send_meshtastic_message("Small Region", earthquake_small['ReportContent'])

            if new_origin_time_all != last_all_time:
                print("All Regions Update Detected")
                last_all_time = new_origin_time_all
                updated = True
                if earthquake_all and earthquake_all['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                    print("All Regions", earthquake_all['ReportContent'])
                    send_meshtastic_message("All Regions", earthquake_all['ReportContent'])

            # if new_weather_time != last_weather_time:
            #     print("Weather Update Detected")
            #     last_weather_time = new_weather_time
            #     updated = True
            #     #send_meshtastic_message("Weather Alert", weather_content)

            if current_time.hour == 8 and (last_run_day is None or last_run_day != today_date):
                # 仅在每天的8点执行一次
                url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001?Authorization=CWA-608053CD-525F-4018-ACD8-DF7F8C5C380E&format=JSON&locationName=花蓮縣,澎湖縣,臺北市,臺中市,高雄市"
                weather_data = fetch_weather_data(url)
                if weather_data:
                    parsed_data = parse_weather_data(weather_data)
                    formatted_forecasts = format_forecast(parsed_data)
                    for forecast in formatted_forecasts:
                        print(forecast)
                        send_meshtastic_message("0800天氣預報", forecast)

                last_run_day = today_date  # 更新最后运行日期

            if updated:
                save_last_origin_times_db(db_connection, last_small_time, last_all_time, last_weather_time)
            else:
                if debugMode:
                    print(f"Checked data: Small: {last_small_time}, All: {last_all_time}, Weather: {last_weather_time}")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        if db_connection:
            db_connection.close()  # 确保在程序结束前关闭数据库连接

        
if __name__ == "__main__":
    main()
