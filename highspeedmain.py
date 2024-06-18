
import time
import os
import json
from datetime import datetime

import requests
import mysql.connector
from mysql.connector import Error
        
debugMode = False
def load_config():
    config_path = './config.json'
    default_config = {
        "Authorization": "Your_Default_Authorization_Key",
        "limit": 1,
        "offset": 0,
        "format": "JSON",
        "magnitude_threshold": 1,
        "db_host": "127.0.0.1",
        "db_port": 3306,
        "db_name": "earthquake_data",
        "table_name": "origin_times",
        "db_user": "username",
        "db_password": "password"
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
        
        
def fetch_speed_data(connection):
    cursor = None  # Initialize cursor to None
    if connection is not None:
        try:
            cursor = connection.cursor()
            query = "SELECT last_origin_time FROM origin_times WHERE type = %s ORDER BY last_checked_time DESC LIMIT 1;"
            cursor.execute(query, ('speed',))
            result = cursor.fetchone()
            if result:
                return result[0]
            else:
                return None
        except Exception as e:
            print(f"Failed to fetch speed data: {e}")
            return None
        finally:
            if cursor:  # Check if cursor was successfully created before trying to close it
                cursor.close()
    else:
        print("No database connection available.")
        return None


def save_last_origin_time_db(connection, new_speed_time):
    if debugMode:
        print("Saving the latest speed time to the database...")
    if connection is not None:
        try:
            cursor = connection.cursor()
            update_query = """
            INSERT INTO origin_times (type, last_origin_time, last_checked_time)
            VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE 
            last_origin_time = VALUES(last_checked_time), 
            last_checked_time = VALUES(last_checked_time);
            """
            current_time = datetime.now()  # 获取当前时间

            # Update the 'speed' type time
            cursor.execute(update_query, ('speed', new_speed_time, current_time))

            connection.commit()
            print("Speed time updated in SQL.")
        except Exception as e:
            print(f"Failed to update speed time in SQL: {e}")
        finally:
            if cursor:
                cursor.close()
    else:
        print("No database connection available.")



def save_last_origin_times_db(connection, last_origin_times_small,last_origin_times_all):
    if debugMode:
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
    db_connection = connect_db(config)

    try:
        while True:
            # 从数据库加载最新的起源时间
            origin_times = read_last_origin_time_db(db_connection)
            current_speed_time = origin_times.get('speed') if origin_times else None

            # 转换成字符串类别
            current_speed_time = str(current_speed_time)
            print("Current speed time:", current_speed_time)

            # 获取最新的速度测试数据
            new_speed_time = fetch_speed_data(db_connection)  # Assuming you have this function

            if debugMode:
                print("===============================")
                print(f"DB speed time: {current_speed_time}")
                print(f"New speed time: {new_speed_time}")
                print("===============================")

            # 检查速度时间是否有变化
            if new_speed_time != current_speed_time:
                if debugMode:
                    print("Speed test detected a change.")
                print("MESHTASTIC: Speed test detected a change.")
                #send_meshtastic_message("speed測試", "偵測中...")
                # 更新数据库中的时间记录
                save_last_origin_time_db(db_connection, new_speed_time)
            else:
                if debugMode:
                    print("No change in speed test time.")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print("Program terminated by user.")
    finally:
        if db_connection:
            db_connection.close()  # 确保在程序结束前关闭数据库连接

if __name__ == "__main__":
    main()
