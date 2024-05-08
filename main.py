
import time
import os
import json
from datetime import datetime

import requests
import mysql.connector
from mysql.connector import Error
        

def connect_db():
    try:
        print("正在嘗試連接到數據庫...")
        connection = mysql.connector.connect(
            host="127.0.0.1",
            user="oliver",
            password="tzsr0804",
            database="earthquake_data"
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

def load_last_origin_times():
    try:
        with open('./.lastData.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {"small": None, "all": None}

def save_last_origin_times(origin_times):
    with open('./.lastData.json', 'w') as file:
        json.dump(origin_times, file)



def save_last_origin_times_db(connection, last_origin_times_small,last_origin_times_all):
    print(" 保存起源时间到数据库...")
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

            # 更新 small 类型的时间
            cursor.execute(update_query, ('small', last_origin_times_small, current_time))
            # 更新 all 类型的时间
            cursor.execute(update_query, ('all', last_origin_times_all, current_time))

            connection.commit()
            print("Origin times updated in SQL.")
        except Error as e:
            print(f"Failed to update origin times in SQL: {e}")
        finally:
            cursor.close()
    else:
        print("No database connection available.")

def read_last_origin_time_db(connection):
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
    # 建立数据库连接（注：connect_db应当返回连接实例以供后续使用，这里假设它存储在全局或传递给需要它的函数）
    db_connection = connect_db()

    try:
        while True:
            # 每次迭代开始时加载最新的起源时间
            #origin_times = load_last_origin_times()

            origin_times = read_last_origin_time_db(db_connection)
            if origin_times is not None:
                # 分别取出 'small' 和 'all' 的时间数据
                last_small_time = origin_times.get('small')
                last_all_time = origin_times.get('all')

            #轉換成字串類別
            last_small_time = str(last_small_time)
            last_all_time = str(last_all_time)

            small_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001"
            all_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"
            

            #取得最近一次的發生時間
            new_origin_time_small, earthquake_small = fetch_earthquake_data(small_url, last_small_time, config)
            new_origin_time_all, earthquake_all = fetch_earthquake_data(all_url, last_all_time, config)
            
            #save_last_origin_times_db(db_connection, origin_times)

            updated = False
            print("===============================")
            print(f"db_small_time: {last_small_time}")
            print(f"db_all_time: {last_all_time}")
            print(f"new_origin_time_small:{new_origin_time_small}")
            print(f"new_origin_time_all:{new_origin_time_all}")
            print("===============================")

            if new_origin_time_small != last_small_time:
                print("發現變化small_time")
                last_small_time = new_origin_time_small
                updated = True
                if earthquake_small and earthquake_small['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                    print("Small Region", earthquake_small['ReportContent'])
                    #send_meshtastic_message("Small Region", earthquake_small['ReportContent'])
            
            if new_origin_time_all != last_all_time:
                print("發現變化all_time")
                last_all_time = new_origin_time_all
                updated = True
                if earthquake_all and earthquake_all['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                    print("All Regions", earthquake_all['ReportContent'])
                    #send_meshtastic_message("All Regions", earthquake_all['ReportContent'])
            
            if updated:
                # 将时间更新保存到数据库
                #save_last_origin_times(origin_times)
                save_last_origin_times_db(db_connection,last_small_time ,last_all_time)

            else:
                print(f"Small Region last origin time: {origin_times['small']}")
                print(f"All Regions last origin time: {origin_times['all']}")
            
            time.sleep(2)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        if db_connection:
            db_connection.close()  # 确保在程序结束前关闭数据库连接
        
if __name__ == "__main__":
    main()