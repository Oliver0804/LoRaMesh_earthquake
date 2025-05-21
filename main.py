import time
import os
import json
from datetime import datetime, timedelta
import requests
import mysql.connector
from mysql.connector import Error
from colorama import Fore, Style
import logging
import requests
from requests.models import PreparedRequest
import meshtastic
import meshtastic.serial_interface
from pubsub import pub
# 確保路徑正確以便導入call_llm模組
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

debugMode = True

# 設置log文件記錄
log_dir = "./logs"
os.makedirs(log_dir, exist_ok=True)
log_file = os.path.join(log_dir, datetime.now().strftime("%Y-%m-%d") + ".log")

# Initialize logging for errors and database interactions only
logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S"
)
def print_earthquake_details(earthquake):
    print(f"{Fore.CYAN}Earthquake Number: {earthquake['EarthquakeNo']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Report Type: {earthquake['ReportType']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Report Color: {earthquake['ReportColor']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Report Content: {earthquake['ReportContent']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Origin Time: {earthquake['EarthquakeInfo']['OriginTime']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Source: {earthquake['EarthquakeInfo']['Source']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Focal Depth: {earthquake['EarthquakeInfo']['FocalDepth']} km{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Epicenter Location: {earthquake['EarthquakeInfo']['Epicenter']['Location']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Epicenter Latitude: {earthquake['EarthquakeInfo']['Epicenter']['EpicenterLatitude']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Epicenter Longitude: {earthquake['EarthquakeInfo']['Epicenter']['EpicenterLongitude']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Magnitude Type: {earthquake['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeType']}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Magnitude Value: {earthquake['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue']}{Style.RESET_ALL}")

def clean_old_logs(log_dir, days=7):
    for filename in os.listdir(log_dir):
        file_path = os.path.join(log_dir, filename)
        if os.path.isfile(file_path):
            file_mtime = datetime.fromtimestamp(os.path.getmtime(file_path))
            if datetime.now() - file_mtime > timedelta(days=days):
                os.remove(file_path)
                logging.info(f"Deleted old log file: {filename}")

def connect_db(config):
    print(f"{Fore.YELLOW}正在嘗試連接到數據庫...{Style.RESET_ALL}")
    try:
        connection = mysql.connector.connect(
            host=config['db_host'],
            user=config['db_user'],
            password=config['db_password'],
            database=config['db_name']
        )
        if connection.is_connected():
            db_info = connection.get_server_info()
            print(f"{Fore.GREEN}成功連接到 MySQL 數據庫，MySQL 服務器版本：{db_info}{Style.RESET_ALL}")
            return connection
    except Error as e:
        print(f"{Fore.RED}數據庫連接失敗：{e}{Style.RESET_ALL}")
        return None

def load_config():
    config_path = './config.json'
    try:
        with open(config_path, 'r') as file:
            config = json.load(file)
            print(f"{Fore.GREEN}成功載入配置文件。{Style.RESET_ALL}")
            return config
    except FileNotFoundError:
        print(f"{Fore.YELLOW}配置文件未找到，使用預設設定。{Style.RESET_ALL}")
        default_config = {
            "Authorization": "Your_Default_Authorization_Key",
            "limit": 1,
            "offset": 0,
            "format": "JSON",
            "magnitude_threshold": 1
        }
        with open(config_path, 'w') as file:
            json.dump(default_config, file)
            print(f"{Fore.GREEN}已創建預設配置文件。{Style.RESET_ALL}")
        return default_config

def save_last_origin_times_db(connection, last_origin_times_small, last_origin_times_all, last_issue_time_weather):
    if connection is not None:
        try:
            cursor = connection.cursor()
            update_query = """
            INSERT INTO origin_times (type, last_origin_time, last_checked_time)
            VALUES (%s, %s, %s) ON DUPLICATE KEY UPDATE 
            last_origin_time = VALUES(last_origin_time), 
            last_checked_time = VALUES(last_checked_time);
            """
            current_time = datetime.now()
            cursor.execute(update_query, ('small', last_origin_times_small, current_time))
            cursor.execute(update_query, ('all', last_origin_times_all, current_time))
            cursor.execute(update_query, ('weather', last_issue_time_weather, current_time))
            connection.commit()
            logging.info("Origin times updated in SQL.")
        except Error as e:
            logging.error(f"Failed to update origin times in SQL: {e}")
        finally:
            cursor.close()
    else:
        print(f"{Fore.RED}No database connection available.{Style.RESET_ALL}")

def read_last_origin_time_db(connection):
    if connection is not None:
        try:
            cursor = connection.cursor()
            select_query = "SELECT type, last_origin_time FROM origin_times;"
            cursor.execute(select_query)
            origin_times = {}
            for (type, last_origin_time) in cursor:
                origin_times[type] = last_origin_time
            print(f"{Fore.GREEN}Origin times read from SQL.{Style.RESET_ALL}")
            return origin_times
        except Error as e:
            print(f"{Fore.RED}Failed to read origin times from SQL: {e}{Style.RESET_ALL}")
        finally:
            cursor.close()
            connection.commit()
    else:
        print(f"{Fore.RED}No database connection available.{Style.RESET_ALL}")
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
                print(f"{Fore.CYAN}{url} 最近一次獲取時間: {datetime.now()}{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Failed to retrieve data: {data['message']}{Style.RESET_ALL}")
    else:
        print(f"{Fore.RED}HTTP Error: {response.status_code}{Style.RESET_ALL}")
    return last_origin_time, None

def send_meshtastic_message(tip_msg, report_content, interface=None):
    try:
        # 檢查是否需要創建新的連接
        local_interface = interface
        close_after = False
        
        if local_interface is None:
            local_interface = meshtastic.serial_interface.SerialInterface()
            close_after = True
        
        # 組合訊息
        message = f"[{tip_msg}] {report_content}"
        
        # 發送訊息到 channel 2
        local_interface.sendText(message, channelIndex=2)
        
        # 如果是臨時創建的連接，則關閉
        if close_after:
            local_interface.close()
        
        logging.info(f"Meshtastic message sent: {tip_msg}")
        print(f"{Fore.GREEN}Meshtastic message sent: {tip_msg}{Style.RESET_ALL}")
    except Exception as e:
        logging.error(f"Failed to send Meshtastic message: {str(e)}")
        print(f"{Fore.RED}Failed to send Meshtastic message: {str(e)}{Style.RESET_ALL}")


def format_forecast(forecast_summary):
    """Formats the extracted forecast information into a specified string format."""
    # 獲取今天的日期和三天後的日期
    today_date = datetime.now().date()
    three_days_later = today_date + timedelta(days=3)

    formatted_forecasts = []
    for location, data in forecast_summary.items():
        # 格式化日期範圍
        date_range = f"{today_date.strftime('%m/%d')}～{three_days_later.strftime('%m/%d')}"
        formatted_forecast = f"{date_range} 天氣預報{location}溫度{data['MinT']}~{data['MaxT']}度,降雨機率{data['PoP']}%：{data['CI']}"
        formatted_forecasts.append(formatted_forecast)
    return formatted_forecasts

def print_request_details(url, headers, params):
    """Utility function to print the full URL and headers of a request."""
    req = PreparedRequest()
    req.prepare_url(url, params)
    req.prepare_headers(headers)

    print("Request URL:", req.url)
    print("Request Headers:", req.headers)
    print("Request Params:", params)


def fetch_weather_data(config):
    """Fetches weather data from the specified URL with retries for handling request failures."""
    base_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
    params = {
        'Authorization': config['Authorization'],
        'limit': 5,
        'offset': config['offset'],
        'format': 'JSON',
        'locationName': '花蓮縣,澎湖縣,臺北市,臺中市,高雄市'
    }
    headers = {'accept': 'application/json'}

    # Print the request details before sending
    print_request_details(base_url, headers, params)

    retries = 3
    while retries > 0:
        response = requests.get(base_url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            if data.get('success') == 'true':
                return data['records']
            else:
                print(f"Failed to retrieve data: {data.get('message')}")
        else:
            print(f"HTTP Error: {response.status_code}")

        retries -= 1
        print(f"Retrying... {retries} attempts left.")
        time.sleep(5)

    print("Failed to retrieve data after multiple attempts.")
    return None


def parse_weather_data(records):
    """Parses the weather data from API response and provides detailed insights.
    
    Args:
        records (dict): The 'records' part of the JSON response containing weather data.

    Returns:
        dict: A dictionary with location names as keys and their weather details as values.
    """
    forecast_summary = {}
    total_locations = len(records['location'])
    print(f"Total locations processed: {total_locations}")

    # Loop through each location to extract weather details
    for location in records['location']:
        location_name = location['locationName']
        forecast_summary[location_name] = {
            'MaxT': None,
            'MinT': None,
            'PoP': None,
            'CI': None
        }
        print(f"\nProcessing weather data for {location_name}:")
        
        # Extract and display each relevant weather element
        for element in location['weatherElement']:
            element_name = element['elementName']
            if element_name in ['MaxT', 'MinT', 'PoP', 'CI']:
                last_period = element['time'][-1]
                parameter = last_period['parameter']
                value = parameter.get('parameterValue', parameter.get('parameterName', ''))
                forecast_summary[location_name][element_name] = value
                
                # Display detailed weather information for the current element
                print(f"  {element_name}: {value}")

    print(f"\nTotal data entries processed: {len(forecast_summary)}")
    return forecast_summary

# 定義接收訊息的回調函數
def on_receive(packet, interface):
    """處理收到的 Meshtastic 訊息"""
    try:
        # 從封包中提取訊息內容和發送者資訊
        message = packet.get('decoded', {}).get('text', '')
        sender = packet.get('fromId', 'Unknown')
        channel = packet.get('channel', 0)
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        
        # 只處理頻道1、2、3的訊息
        if channel in [1, 2, 3]:
            # 格式化並顯示訊息內容
            print(f"\n{Fore.MAGENTA}===== 收到 Meshtastic 訊息 ====={Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}時間: {timestamp}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}發送者: {sender}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}頻道: {channel}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}內容: {message}{Style.RESET_ALL}")
            print(f"{Fore.MAGENTA}==========================={Style.RESET_ALL}\n")
            
            # 檢查訊息是否包含"@bashcat"
            if "@bashcat" in message:
                print(f"{Fore.CYAN}偵測到@bashcat提及，正在準備LLM回應...{Style.RESET_ALL}")
                
                # 提取@bashcat後的實際內容
                try:
                    # 尋找@bashcat在訊息中的位置
                    tag_position = message.find("@bashcat")
                    # 提取@bashcat後的訊息作為真正要處理的內容
                    actual_query = message[tag_position + 8:].strip()
                    
                    if actual_query:
                        # 導入call_llm模組
                        from call_llm import generate_response
                        
                        print(f"{Fore.CYAN}處理查詢: '{actual_query}'{Style.RESET_ALL}")
                        
                        # 生成LLM回應，限制在66字以內
                        llm_response = generate_response(actual_query, max_length=66)
                        print(f"{Fore.CYAN}LLM回應: {llm_response}{Style.RESET_ALL}")
                        
                        # 發送LLM回應
                        if interface is not None:
                            # 將LLM回應發送到原始頻道
                            interface.sendText(f"{llm_response}", channelIndex=channel)
                            print(f"{Fore.GREEN}已發送LLM回應到頻道 {channel}{Style.RESET_ALL}")
                            logging.info(f"Sent LLM response to channel {channel}: {llm_response}")
                        else:
                            print(f"{Fore.YELLOW}無法發送LLM回應：Meshtastic介面不可用{Style.RESET_ALL}")
                            logging.warning("Cannot send LLM response: Meshtastic interface unavailable")
                    else:
                        print(f"{Fore.YELLOW}@bashcat後沒有實際查詢內容{Style.RESET_ALL}")
                        if interface is not None:
                            interface.sendText("您好，請在@bashcat後輸入您的問題，例如「@bashcat 什麼是地震？」", channelIndex=channel)
                except Exception as llm_error:
                    error_msg = f"LLM回應生成失敗: {str(llm_error)[:60]}..."
                    print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
                    logging.error(f"LLM response error: {str(llm_error)}")
                    
                    # 即使LLM失敗，也發送錯誤訊息
                    if interface is not None:
                        interface.sendText(f"[錯誤] {error_msg}", channelIndex=channel)
            else:
                print(f"{Fore.YELLOW}訊息不含@bashcat標記，不調用LLM{Style.RESET_ALL}")
            
            # 記錄到日誌
            logging.info(f"Meshtastic message received - From: {sender}, Channel: {channel}, Message: {message}")
        else:
            # 只記錄但不顯示其他頻道的訊息
            logging.debug(f"Ignored message from channel {channel} - From: {sender}, Message: {message}")
    except Exception as e:
        logging.error(f"Error processing received message: {str(e)}")
        print(f"{Fore.RED}處理收到的訊息時發生錯誤: {str(e)}{Style.RESET_ALL}")

def main():
    clean_old_logs(log_dir)
    config = load_config()
    db_connection = connect_db(config)
    last_run_day = None
    meshtastic_interface = None
    
    # 嘗試連接 Meshtastic 裝置
    try:
        meshtastic_interface = meshtastic.serial_interface.SerialInterface()
        print(f"{Fore.GREEN}成功連接到 Meshtastic 裝置{Style.RESET_ALL}")
        logging.info("Connected to Meshtastic device")
        
        # 訂閱訊息接收事件
        pub.subscribe(on_receive, "meshtastic.receive")
        print(f"{Fore.GREEN}已訂閱 Meshtastic 訊息接收事件{Style.RESET_ALL}")
        logging.info("Subscribed to Meshtastic message events")
    except Exception as e:
        print(f"{Fore.RED}無法連接 Meshtastic 裝置: {str(e)}{Style.RESET_ALL}")
        logging.error(f"Cannot connect to Meshtastic device: {str(e)}")
        meshtastic_interface = None
        
    # 記錄系統啟動
    logging.info("System started.")
    try:
        while True:
            current_time = datetime.now()
            today_date = current_time.date()
            if db_connection is None or not db_connection.is_connected():
                print(f"{Fore.YELLOW}数据库连接丢失，尝试重新连接...{Style.RESET_ALL}")
                logging.warning("Database connection lost, attempting to reconnect...")
                db_connection = connect_db(config)
                if db_connection is None or not db_connection.is_connected():
                    print(f"{Fore.RED}重新连接失败，稍后再试...{Style.RESET_ALL}")
                    logging.error("Reconnection failed, retrying in 10 seconds...")
                    time.sleep(10)
                    continue

            origin_times = read_last_origin_time_db(db_connection)
            if origin_times is not None:
                last_small_time = str(origin_times.get('small', ''))
                last_all_time = str(origin_times.get('all', ''))
                last_weather_time = str(origin_times.get('weather', ''))

            small_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0016-001"
            all_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/E-A0015-001"

            new_origin_time_small, earthquake_small = fetch_earthquake_data(small_url, last_small_time, config)
            new_origin_time_all, earthquake_all = fetch_earthquake_data(all_url, last_all_time, config)

            updated = False
            if new_origin_time_small != last_small_time:
                print(f"{Fore.GREEN}Small Region Update Detected{Style.RESET_ALL}")
                last_small_time = new_origin_time_small
                updated = True
                if earthquake_small and earthquake_small['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                    print(f"{Fore.GREEN}Small Region: {earthquake_small['ReportContent']}{Style.RESET_ALL}")
                    send_meshtastic_message("Small Region", earthquake_small['ReportContent'], meshtastic_interface)

            if new_origin_time_all != last_all_time:
                print(f"{Fore.GREEN}All Regions Update Detected{Style.RESET_ALL}")
                last_all_time = new_origin_time_all
                updated = True
                if earthquake_all and earthquake_all['EarthquakeInfo']['EarthquakeMagnitude']['MagnitudeValue'] > config['magnitude_threshold']:
                    print(f"{Fore.GREEN}All Regions: {earthquake_all['ReportContent']}{Style.RESET_ALL}")
                    send_meshtastic_message("All Regions", earthquake_all['ReportContent'], meshtastic_interface)

            if current_time.hour == 8 and (last_run_day is None or last_run_day != today_date):
                weather_url = "https://opendata.cwa.gov.tw/api/v1/rest/datastore/F-C0032-001"
                weather_data = fetch_weather_data(config)
                if weather_data:
                    parsed_data = parse_weather_data(weather_data)
                    formatted_forecasts = format_forecast(parsed_data)
                    for forecast in formatted_forecasts:
                        print(forecast)
                        send_meshtastic_message("0800天氣預報", forecast, meshtastic_interface)

                last_run_day = today_date
                logging.info(f"Last run day: {last_run_day}")
            if updated:
                save_last_origin_times_db(db_connection, last_small_time, last_all_time, last_weather_time)
            #print adn log last_run_day 
            print(f"Last run day: {last_run_day}")
            
            # 每 20 次迴圈顯示一次 Meshtastic 連線狀態 (約每 10 秒)
            if hasattr(main, 'loop_counter'):
                main.loop_counter += 1
            else:
                main.loop_counter = 0
                
            if main.loop_counter % 20 == 0:
                if meshtastic_interface is not None:
                    try:
                        # 取得裝置資訊來檢查連線狀態
                        node_info = meshtastic_interface.myInfo
                        print(f"{Fore.GREEN}Meshtastic 連線中 - 節點: {node_info.get('user', {}).get('longName', 'Unknown')}{Style.RESET_ALL}")
                    except Exception as e:
                        print(f"{Fore.RED}Meshtastic 連線中斷: {str(e)}{Style.RESET_ALL}")
                        # 嘗試重新連接
                        try:
                            if meshtastic_interface:
                                meshtastic_interface.close()
                            meshtastic_interface = meshtastic.serial_interface.SerialInterface()
                            print(f"{Fore.GREEN}已重新連接到 Meshtastic 裝置{Style.RESET_ALL}")
                            logging.info("Reconnected to Meshtastic device")
                            
                            # 重新訂閱訊息接收事件
                            pub.subscribe(on_receive, "meshtastic.receive")
                            print(f"{Fore.GREEN}已重新訂閱 Meshtastic 訊息接收事件{Style.RESET_ALL}")
                            logging.info("Resubscribed to Meshtastic message events")
                        except Exception as reconnect_error:
                            print(f"{Fore.RED}無法重新連接 Meshtastic: {str(reconnect_error)}{Style.RESET_ALL}")
                            logging.error(f"Failed to reconnect to Meshtastic: {str(reconnect_error)}")
                            meshtastic_interface = None
                else:
                    print(f"{Fore.YELLOW}Meshtastic 未連接{Style.RESET_ALL}")
                    # 嘗試連接
                    try:
                        meshtastic_interface = meshtastic.serial_interface.SerialInterface()
                        print(f"{Fore.GREEN}已連接到 Meshtastic 裝置{Style.RESET_ALL}")
                        logging.info("Connected to Meshtastic device")
                        
                        # 訂閱訊息接收事件
                        pub.subscribe(on_receive, "meshtastic.receive")
                        print(f"{Fore.GREEN}已訂閱 Meshtastic 訊息接收事件{Style.RESET_ALL}")
                        logging.info("Subscribed to Meshtastic message events")
                    except Exception as e:
                        print(f"{Fore.RED}無法連接 Meshtastic: {str(e)}{Style.RESET_ALL}")
                        logging.error(f"Cannot connect to Meshtastic device: {str(e)}")

            time.sleep(0.5)
    except KeyboardInterrupt:
        print(f"{Fore.YELLOW}Program terminated by user.{Style.RESET_ALL}")
        logging.info("Program terminated by user.")
    finally:
        if db_connection:
            db_connection.close()
        if meshtastic_interface:
            meshtastic_interface.close()
            print(f"{Fore.YELLOW}Meshtastic connection closed.{Style.RESET_ALL}")
            logging.info("Meshtastic connection closed.")

if __name__ == "__main__":
    main()

