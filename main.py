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
import threading
from flask import Flask
# 確保路徑正確以便導入call_llm模組和CWA客戶端
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 導入CWA客戶端
from cwa_client import CWAClient

# 城市名稱到縣市的映射表（用於天氣查詢）
CITY_MAPPING = {
    # 縣市全名
    '宜蘭縣': '001', '臺北市': '061', '新北市': '069', '桃園市': '005',
    '新竹市': '053', '新竹縣': '009', '苗栗縣': '013', '臺中市': '073',
    '彰化縣': '017', '南投縣': '021', '雲林縣': '025', '嘉義市': '057',
    '嘉義縣': '029', '臺南市': '077', '高雄市': '065', '屏東縣': '033',
    '臺東縣': '037', '花蓮縣': '041', '澎湖縣': '045', '基隆市': '049',
    '金門縣': '085', '連江縣': '081',
    # 簡化地名映射
    '宜蘭': '001', '臺北': '061', '台北': '061', '新北': '069', '桃園': '005',
    '新竹': '053', '新竹市': '053', '新竹縣': '009', '苗栗': '013', 
    '臺中': '073', '台中': '073', '彰化': '017', '南投': '021', '雲林': '025',
    '嘉義': '057', '嘉義市': '057', '嘉義縣': '029', '臺南': '077', '台南': '077',
    '高雄': '065', '屏東': '033', '臺東': '037', '台東': '037', '花蓮': '041',
    '澎湖': '045', '基隆': '049', '金門': '085', '連江': '081', '馬祖': '081'
}

# 簡化地名到完整縣市名稱的映射（用於CWA API調用）
CITY_TO_FULL_NAME = {
    '宜蘭': '宜蘭縣', '臺北': '臺北市', '台北': '臺北市', '新北': '新北市', 
    '桃園': '桃園市', '新竹': '新竹縣', '新竹市': '新竹市', '苗栗': '苗栗縣',
    '臺中': '臺中市', '台中': '臺中市', '彰化': '彰化縣', '南投': '南投縣',
    '雲林': '雲林縣', '嘉義': '嘉義縣', '嘉義市': '嘉義市', '臺南': '臺南市',
    '台南': '臺南市', '高雄': '高雄市', '屏東': '屏東縣', '臺東': '臺東縣',
    '台東': '臺東縣', '花蓮': '花蓮縣', '澎湖': '澎湖縣', '基隆': '基隆市',
    '金門': '金門縣', '連江': '連江縣', '馬祖': '連江縣',
    # 已經是完整名稱的直接對應
    '宜蘭縣': '宜蘭縣', '臺北市': '臺北市', '新北市': '新北市', '桃園市': '桃園市',
    '新竹市': '新竹市', '新竹縣': '新竹縣', '苗栗縣': '苗栗縣', '臺中市': '臺中市',
    '彰化縣': '彰化縣', '南投縣': '南投縣', '雲林縣': '雲林縣', '嘉義市': '嘉義市',
    '嘉義縣': '嘉義縣', '臺南市': '臺南市', '高雄市': '高雄市', '屏東縣': '屏東縣',
    '臺東縣': '臺東縣', '花蓮縣': '花蓮縣', '澎湖縣': '澎湖縣', '基隆市': '基隆市',
    '金門縣': '金門縣', '連江縣': '連江縣'
}

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
        # 數據清理：確保訊息格式正確，避免協議解析錯誤
        if not isinstance(tip_msg, str):
            tip_msg = str(tip_msg) if tip_msg is not None else "Alert"
        if not isinstance(report_content, str):
            report_content = str(report_content) if report_content is not None else ""
            
        # 過濾掉可能導致解析錯誤的字符
        tip_msg = tip_msg.replace('\x00', '').replace('\0', '')
        report_content = report_content.replace('\x00', '').replace('\0', '')
            
        # 檢查是否需要創建新的連接
        local_interface = interface
        close_after = False
        
        if local_interface is None:
            try:
                # 使用標準的連接初始化（已移除connectTimeout參數）
                local_interface = meshtastic.serial_interface.SerialInterface()
                close_after = True
                logging.info("Created temporary Meshtastic connection for sending message")
            except Exception as conn_err:
                logging.error(f"Failed to create temporary Meshtastic connection: {str(conn_err)}")
                print(f"{Fore.RED}無法創建臨時連接發送訊息: {str(conn_err)}{Style.RESET_ALL}")
                return False
        
        # 組合訊息
        message = f"[{tip_msg}] {report_content}"
        
        # 訊息大小限制檢查 - Meshtastic協議有大小限制，過大的訊息可能導致錯誤
        if len(message.encode('utf-8')) > 200:  # 設定一個安全值，Meshtastic可能有自己的限制
            logging.warning(f"Message too large ({len(message.encode('utf-8'))} bytes), truncating")
            # 截斷訊息，確保不超過限制
            message = message[:197] + "..."
        
        try:
            # 發送訊息到 channel 2，設置超時處理
            local_interface.sendText(message, channelIndex=2)
        except Exception as send_err:
            logging.error(f"Error sending message: {str(send_err)}")
            print(f"{Fore.RED}發送訊息時出錯: {str(send_err)}{Style.RESET_ALL}")
            
            # 如果是臨時創建的連接，要確保關閉
            if close_after and local_interface:
                try:
                    local_interface.close()
                except Exception as close_err:
                    logging.warning(f"Error closing connection after send error: {str(close_err)}")
            return False
        
        # 如果是臨時創建的連接，則關閉
        if close_after:
            try:
                local_interface.close()
            except Exception as close_err:
                logging.warning(f"Error closing temporary connection: {str(close_err)}")
                print(f"{Fore.YELLOW}關閉臨時連接時出錯: {str(close_err)}{Style.RESET_ALL}")
                # 這不是致命錯誤，訊息已發送成功
        
        logging.info(f"Meshtastic message sent: {tip_msg}")
        print(f"{Fore.GREEN}Meshtastic message sent: {tip_msg}{Style.RESET_ALL}")
        return True
    except Exception as e:
        logging.error(f"Failed to send Meshtastic message: {str(e)}")
        print(f"{Fore.RED}Failed to send Meshtastic message: {str(e)}{Style.RESET_ALL}")
        return False


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

def get_weather_info_for_llm(query, cwa_client):
    """
    從用戶查詢中提取地名並獲取天氣資訊
    返回格式化的天氣資訊字串，用於LLM處理
    現在使用 get_detailed_weather_for_llm 獲取更完整的天氣資訊
    """
    try:
        # 尋找查詢中的城市名稱（優先匹配較長的名稱）
        detected_city = None
        detected_full_name = None
        
        # 按長度排序，優先匹配較長的城市名稱
        sorted_cities = sorted(CITY_TO_FULL_NAME.keys(), key=len, reverse=True)
        
        for city_name in sorted_cities:
            if city_name in query:
                detected_city = city_name
                detected_full_name = CITY_TO_FULL_NAME[city_name]
                break
        
        if not detected_city:
            return "無法識別您查詢的城市，請提供具體的縣市名稱，例如：臺北、高雄、花蓮等。"
        
        print(f"{Fore.CYAN}檢測到城市: {detected_city} -> {detected_full_name}{Style.RESET_ALL}")
        
        # 使用 get_detailed_weather_for_llm 獲取詳細天氣資訊
        detailed_weather = cwa_client.get_detailed_weather_for_llm(detected_full_name)
        
        return detailed_weather
        
    except Exception as e:
        logging.error(f"Error getting weather info for LLM: {str(e)}")
        return f"獲取天氣資訊時發生錯誤：{str(e)}"

def get_earthquake_info_for_llm(cwa_client, max_display: int = 5):
    """
    獲取最新地震資訊，返回格式化的地震資訊字串，用於LLM處理
    現在會獲取最近10筆地震資料，並顯示前幾筆的詳細資訊
    
    Args:
        cwa_client: CWA API 客戶端
        max_display: 最多顯示幾筆地震的詳細資訊 (預設5筆)
    """
    try:
        earthquake_data = cwa_client.get_latest_earthquake()  # 現在預設獲取10筆
        
        if earthquake_data.get('success') != 'true':
            return "無法獲取最新地震資料，請稍後再試。"
        
        earthquakes = earthquake_data.get('records', {}).get('Earthquake', [])
        if not earthquakes:
            return "目前沒有地震資料。"
        
        # 格式化地震資訊
        earthquake_summary = f"🌍 最新地震資訊（共{len(earthquakes)}筆資料）：\n\n"
        
        # 顯示前 max_display 筆地震的詳細資訊
        display_count = min(max_display, len(earthquakes))
        
        for i, eq in enumerate(earthquakes[:display_count]):
            eq_info = eq.get('EarthquakeInfo', {})
            
            # 提取地震資訊
            origin_time = eq_info.get('OriginTime', '未知時間')
            magnitude = eq_info.get('EarthquakeMagnitude', {}).get('MagnitudeValue', '未知')
            location = eq_info.get('Epicenter', {}).get('Location', '未知位置')
            depth = eq_info.get('FocalDepth', '未知')
            report_content = eq.get('ReportContent', '無詳細報告')
            
            # 找出最大震度
            max_intensity = '未知'
            shaking_areas = eq.get('Intensity', {}).get('ShakingArea', [])
            if shaking_areas:
                max_intensity_value = 0
                for area in shaking_areas:
                    area_intensity = area.get('AreaIntensity', '0級')
                    try:
                        intensity_num = int(area_intensity.replace('級', ''))
                        if intensity_num > max_intensity_value:
                            max_intensity_value = intensity_num
                            max_intensity = area_intensity
                    except:
                        pass
            
            # 格式化單筆地震資訊
            if i == 0:
                earthquake_summary += f"📍 第{i+1}筆（最新）：\n"
            else:
                earthquake_summary += f"� 第{i+1}筆：\n"
            
            earthquake_summary += f"  �📅 發生時間：{origin_time}\n"
            earthquake_summary += f"  📍 震央位置：{location}\n"
            earthquake_summary += f"  📊 地震規模：M{magnitude}\n"
            earthquake_summary += f"  📏 震源深度：{depth}公里\n"
            earthquake_summary += f"  🎯 最大震度：{max_intensity}\n"
            earthquake_summary += f"  📝 說明：{report_content}\n\n"
        
        # 如果還有更多地震資料未顯示
        if len(earthquakes) > display_count:
            earthquake_summary += f"... 還有{len(earthquakes) - display_count}筆地震資料\n\n"
        
        # 提供整體統計
        earthquake_summary += f"📈 整體統計（最近{len(earthquakes)}筆）：\n"
        
        magnitude_4_plus = 0
        magnitude_5_plus = 0
        magnitude_6_plus = 0
        
        for eq in earthquakes:
            eq_mag = eq.get('EarthquakeInfo', {}).get('EarthquakeMagnitude', {}).get('MagnitudeValue', '0')
            try:
                mag_value = float(eq_mag)
                if mag_value >= 4.0:
                    magnitude_4_plus += 1
                if mag_value >= 5.0:
                    magnitude_5_plus += 1
                if mag_value >= 6.0:
                    magnitude_6_plus += 1
            except:
                pass
        
        earthquake_summary += f"• 規模4.0以上：{magnitude_4_plus}次\n"
        if magnitude_5_plus > 0:
            earthquake_summary += f"• 規模5.0以上：{magnitude_5_plus}次\n"
        if magnitude_6_plus > 0:
            earthquake_summary += f"• 規模6.0以上：{magnitude_6_plus}次\n"
        
        return earthquake_summary.strip()
        
    except Exception as e:
        logging.error(f"Error getting earthquake info for LLM: {str(e)}")
        return f"獲取地震資訊時發生錯誤：{str(e)}"

# 定義接收訊息的回調函數
def on_receive(packet, interface):
    """處理收到的 Meshtastic 訊息"""
    try:
        # 協議錯誤處理：初始化協議錯誤計數器（如果尚未初始化）
        if not hasattr(main, 'protocol_errors'):
            main.protocol_errors = 0
            
        # 數據驗證：檢查封包是否有效
        if not isinstance(packet, dict):
            error_msg = f"接收到無效封包格式: {type(packet)}"
            logging.warning(error_msg)
            print(f"{Fore.YELLOW}{error_msg}{Style.RESET_ALL}")
            
            # 增加協議錯誤計數
            main.protocol_errors += 1
            print(f"{Fore.YELLOW}協議錯誤計數: {main.protocol_errors}/5{Style.RESET_ALL}")
            return
            
        # 數據驗證：檢查必要欄位
        if 'decoded' not in packet:
            error_msg = "封包缺少 'decoded' 欄位"
            logging.warning(error_msg)
            print(f"{Fore.YELLOW}{error_msg}{Style.RESET_ALL}")
            
            # 增加協議錯誤計數
            main.protocol_errors += 1
            print(f"{Fore.YELLOW}協議錯誤計數: {main.protocol_errors}/5{Style.RESET_ALL}")
            return
            
        # 從封包中提取訊息內容和發送者資訊
        try:
            decoded = packet.get('decoded', {})
            message = decoded.get('text', '')
            if not isinstance(message, str):
                error_msg = f"訊息內容格式無效: {type(message)}"
                logging.warning(error_msg)
                print(f"{Fore.YELLOW}{error_msg}{Style.RESET_ALL}")
                message = str(message) if message is not None else ""
                
            sender = packet.get('fromId', 'Unknown')
            channel = packet.get('channel', 0)
            
            # 數據驗證：檢查頻道值
            if not isinstance(channel, int):
                error_msg = f"頻道格式無效: {type(channel)}"
                logging.warning(error_msg)
                print(f"{Fore.YELLOW}{error_msg}{Style.RESET_ALL}")
                try:
                    channel = int(channel) if channel is not None else 0
                except (ValueError, TypeError):
                    channel = 0
        except Exception as decode_error:
            # 特別處理解碼錯誤
            error_msg = f"訊息解碼錯誤: {str(decode_error)}"
            logging.warning(error_msg)
            print(f"{Fore.YELLOW}{error_msg}{Style.RESET_ALL}")
            
            # 增加協議錯誤計數
            main.protocol_errors += 1
            print(f"{Fore.YELLOW}協議錯誤計數: {main.protocol_errors}/5{Style.RESET_ALL}")
            return
                
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
            
            # 記錄收到的訊息
            logging.info(f"Meshtastic message received - From: {sender}, Channel: {channel}, Message: {message}")
            
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
                        
                        # 檢查是否包含天氣或地震關鍵詞
                        enhanced_prompt = actual_query
                        
                        # 初始化CWA客戶端（用於獲取天氣和地震資料）
                        try:
                            cwa_client = CWAClient()
                        except Exception as cwa_error:
                            print(f"{Fore.YELLOW}無法初始化CWA客戶端: {str(cwa_error)}{Style.RESET_ALL}")
                            cwa_client = None
                        
                        # 檢查天氣查詢
                        if '天氣' in actual_query and cwa_client:
                            print(f"{Fore.CYAN}檢測到天氣查詢，正在獲取天氣資料...{Style.RESET_ALL}")
                            weather_info = get_weather_info_for_llm(actual_query, cwa_client)
                            enhanced_prompt = f"用戶查詢：{actual_query}\n\n相關天氣資料：\n{weather_info}\n\n請根據以上天氣資料回答用戶的問題。"
                            print(f"{Fore.CYAN}已獲取天氣資料，準備LLM處理{Style.RESET_ALL}")
                        
                        # 檢查地震查詢
                        elif '地震' in actual_query and cwa_client:
                            print(f"{Fore.CYAN}檢測到地震查詢，正在獲取地震資料...{Style.RESET_ALL}")
                            earthquake_info = get_earthquake_info_for_llm(cwa_client)
                            enhanced_prompt = f"用戶查詢：{actual_query}\n\n最新地震資料：\n{earthquake_info}\n\n請根據以上地震資料回答用戶的問題。"
                            print(f"{Fore.CYAN}已獲取地震資料，準備LLM處理{Style.RESET_ALL}")
                        
                        # 生成LLM回應，限制在66字以內
                        llm_response = generate_response(enhanced_prompt, max_length=66)
                        print(f"{Fore.CYAN}LLM回應: {llm_response}{Style.RESET_ALL}")
                        
                        # 發送LLM回應
                        if interface is not None:
                            try:
                                # 將LLM回應發送到原始頻道
                                interface.sendText(f"{llm_response}", channelIndex=channel)
                                print(f"{Fore.GREEN}已發送LLM回應到頻道 {channel}{Style.RESET_ALL}")
                                logging.info(f"Sent LLM response to channel {channel}: {llm_response}")
                            except Exception as send_error:
                                error_msg = f"發送LLM回應時出錯: {str(send_error)}"
                                print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
                                logging.error(f"Error sending LLM response: {str(send_error)}")
                        else:
                            error_msg = "無法發送LLM回應: Meshtastic接口未連接"
                            print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
                            logging.error("Cannot send LLM response: Meshtastic interface not connected")
                    else:
                        print(f"{Fore.YELLOW}@bashcat後沒有實際內容，跳過LLM處理{Style.RESET_ALL}")
                        if interface is not None:
                            interface.sendText("您好，請在@bashcat後輸入您的問題，例如「@bashcat 臺北天氣如何？」或「@bashcat 最近有地震嗎？」", channelIndex=channel)
                except Exception as query_error:
                    error_msg = f"處理@bashcat查詢時出錯: {str(query_error)}"
                    print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
                    logging.error(f"Error processing @bashcat query: {str(query_error)}")
            else:
                print(f"{Fore.YELLOW}訊息不含@bashcat標記，不調用LLM{Style.RESET_ALL}")
                
            # 收到正常訊息，重置協議錯誤計數
            if hasattr(main, 'protocol_errors') and main.protocol_errors > 0:
                print(f"{Fore.GREEN}成功處理訊息，重置協議錯誤計數{Style.RESET_ALL}")
                main.protocol_errors = 0
                
    except Exception as e:
        # 處理所有其他錯誤，包括可能的protobuf解析錯誤
        error_msg = f"處理收到的訊息時出錯: {str(e)}"
        print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
        logging.error(f"Error processing received message: {str(e)}")
        
        # 檢查是否為解析錯誤(DecodeError或其他解析相關錯誤)
        error_str = str(e).lower()
        if "decode" in error_str or "parse" in error_str or "protobuf" in error_str:
            # 這是一個協議解析錯誤，增加計數
            if hasattr(main, 'protocol_errors'):
                main.protocol_errors += 1
            else:
                main.protocol_errors = 1
                
            print(f"{Fore.RED}檢測到協議解析錯誤，當前計數: {main.protocol_errors}/5{Style.RESET_ALL}")
            logging.warning(f"Protocol parse error detected, count: {main.protocol_errors}/5")
            
            # 實現指數退避策略 - 連續錯誤時增加更長的等待時間
            if main.protocol_errors > 3:
                wait_time = min(2 ** (main.protocol_errors - 3), 10)  # 最多等待10秒
                print(f"{Fore.YELLOW}連續多次協議錯誤，等待{wait_time}秒以穩定連接...{Style.RESET_ALL}")
                time.sleep(wait_time)

# 全局變數用於在主程式和API之間共享Meshtastic接口
shared_meshtastic_interface = None
interface_lock = threading.Lock()

def set_shared_meshtastic_interface(interface):
    """設置共享的Meshtastic接口"""
    global shared_meshtastic_interface
    with interface_lock:
        shared_meshtastic_interface = interface

def get_shared_meshtastic_interface():
    """獲取共享的Meshtastic接口"""
    global shared_meshtastic_interface
    with interface_lock:
        return shared_meshtastic_interface

def start_api_server():
    """在背景線程中啟動API服務器"""
    from api_server import run_api_server
    try:
        print(f"{Fore.GREEN}在背景啟動API服務器...{Style.RESET_ALL}")
        run_api_server(host='0.0.0.0', port=5000)
    except Exception as e:
        print(f"{Fore.RED}API服務器啟動失敗: {str(e)}{Style.RESET_ALL}")
        logging.error(f"Failed to start API server: {str(e)}")

def main():
    clean_old_logs(log_dir)
    config = load_config()
    db_connection = connect_db(config)
    last_run_day = None
    meshtastic_interface = None
    
    # 啟動API服務器線程
    api_thread = threading.Thread(target=start_api_server, daemon=True)
    api_thread.start()
    print(f"{Fore.GREEN}API服務器線程已啟動{Style.RESET_ALL}")
    
    # 嘗試連接 Meshtastic 裝置
    try:
        # 連接到Meshtastic裝置
        meshtastic_interface = meshtastic.serial_interface.SerialInterface()
        print(f"{Fore.GREEN}成功連接到 Meshtastic 裝置{Style.RESET_ALL}")
        logging.info("Connected to Meshtastic device")
        
        # 設置共享接口
        set_shared_meshtastic_interface(meshtastic_interface)
        
        # 同時也設置API服務器的接口
        try:
            import api_server
            api_server.set_meshtastic_interface(meshtastic_interface)
            print(f"{Fore.GREEN}API服務器接口已更新{Style.RESET_ALL}")
        except Exception as api_error:
            print(f"{Fore.YELLOW}無法更新API服務器接口: {str(api_error)}{Style.RESET_ALL}")
            logging.warning(f"Could not update API server interface: {str(api_error)}")
        
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
            
            # 連接管理和檢查邏輯
            # 降低連接檢查頻率，從20次迴圈改為100次迴圈（約50秒）
            if hasattr(main, 'loop_counter'):
                main.loop_counter += 1
            else:
                main.loop_counter = 0
                
            # 添加一個重新連接計數器，避免頻繁重連
            if not hasattr(main, 'reconnect_attempts'):
                main.reconnect_attempts = 0
                
            # 添加上次連接成功的時間戳，用於實現冷卻期
            if not hasattr(main, 'last_successful_connection'):
                main.last_successful_connection = time.time()
                
            # 添加協議錯誤計數器
            if not hasattr(main, 'protocol_errors'):
                main.protocol_errors = 0
                
            # 持續的協議錯誤應該觸發連接重置
            if hasattr(main, 'protocol_errors') and main.protocol_errors > 5:
                print(f"{Fore.RED}檢測到多次協議錯誤 ({main.protocol_errors}/5)，強制重置連接...{Style.RESET_ALL}")
                logging.warning(f"Multiple protocol errors detected ({main.protocol_errors}/5), forcing connection reset")
                
                try:
                    if meshtastic_interface:
                        try:
                            meshtastic_interface.close()
                        except Exception as close_error:
                            logging.warning(f"Error during connection close in reset: {str(close_error)}")
                            
                    meshtastic_interface = None
                    
                    # 重置計數器
                    main.protocol_errors = 0
                    main.reconnect_attempts = 0
                    
                    # 設置冷卻期
                    main.last_connection_attempt = time.time()
                    
                    # 強制等待5秒讓系統穩定
                    time.sleep(5)
                    
                    print(f"{Fore.YELLOW}連接已重置，等待下一次連接嘗試{Style.RESET_ALL}")
                    logging.info("Connection has been reset due to protocol errors, waiting for next connection attempt")
                except Exception as reset_error:
                    logging.error(f"Error during forced reset: {str(reset_error)}")
                    print(f"{Fore.RED}重置連接時發生錯誤: {str(reset_error)}{Style.RESET_ALL}")
                
            # 每100次迴圈檢查一次連接狀態
            if main.loop_counter % 100 == 0:
                if meshtastic_interface is not None:
                    try:
                        # 使用一個更簡單的方法檢查連接狀態，避免複雜操作
                        is_connected = hasattr(meshtastic_interface, 'localNode') and meshtastic_interface.localNode is not None
                        
                        if is_connected:
                            print(f"{Fore.GREEN}Meshtastic 連線中 - 保持連線狀態{Style.RESET_ALL}")
                            main.reconnect_attempts = 0  # 重置重連計數器
                            main.last_successful_connection = time.time()  # 更新上次成功連接時間
                        else:
                            raise Exception("連接不完整")
                            
                    except Exception as e:
                        print(f"{Fore.YELLOW}Meshtastic 連線檢查失敗: {str(e)}{Style.RESET_ALL}")
                        
                        # 檢查距離上次成功連接是否已經過了至少60秒（冷卻期）
                        current_time = time.time()
                        if current_time - main.last_successful_connection > 60:
                            # 檢查重連嘗試次數，避免無限重連
                            if main.reconnect_attempts < 3:
                                print(f"{Fore.YELLOW}嘗試重新連接 Meshtastic (嘗試 #{main.reconnect_attempts + 1}){Style.RESET_ALL}")
                                # 嘗試重新連接
                                try:
                                    # 安全關閉現有連接
                                    if meshtastic_interface:
                                        try:
                                            meshtastic_interface.close()
                                        except Exception as close_error:
                                            logging.warning(f"Error during connection close: {str(close_error)}")
                                    
                                    # 預防性延遲，確保Serial端口已被釋放
                                    time.sleep(2)
                                    
                                    # 重新連接
                                    meshtastic_interface = meshtastic.serial_interface.SerialInterface()
                                    print(f"{Fore.GREEN}已重新連接到 Meshtastic 裝置{Style.RESET_ALL}")
                                    logging.info("Reconnected to Meshtastic device")
                                    
                                    # 更新共享接口
                                    set_shared_meshtastic_interface(meshtastic_interface)
                                    
                                    # 同時也更新API服務器的接口
                                    try:
                                        import api_server
                                        api_server.set_meshtastic_interface(meshtastic_interface)
                                        print(f"{Fore.GREEN}API服務器接口已更新（重連）{Style.RESET_ALL}")
                                    except Exception as api_error:
                                        print(f"{Fore.YELLOW}無法更新API服務器接口（重連）: {str(api_error)}{Style.RESET_ALL}")
                                        logging.warning(f"Could not update API server interface (reconnect): {str(api_error)}")
                                    
                                    # 重新訂閱訊息接收事件
                                    pub.subscribe(on_receive, "meshtastic.receive")
                                    print(f"{Fore.GREEN}已重新訂閱 Meshtastic 訊息接收事件{Style.RESET_ALL}")
                                    logging.info("Resubscribed to Meshtastic message events")
                                    
                                    # 更新成功連接時間和計數器
                                    main.last_successful_connection = time.time()
                                    main.reconnect_attempts += 1
                                except Exception as reconnect_error:
                                    print(f"{Fore.RED}無法重新連接 Meshtastic: {str(reconnect_error)}{Style.RESET_ALL}")
                                    logging.error(f"Failed to reconnect to Meshtastic: {str(reconnect_error)}")
                                    main.reconnect_attempts += 1
                                    meshtastic_interface = None
                            else:
                                print(f"{Fore.RED}達到最大重連嘗試次數 (3)，暫停重連嘗試{Style.RESET_ALL}")
                                # 每30分鐘重置重連計數器，允許再次嘗試
                                if current_time - main.last_successful_connection > 1800:  # 30分鐘
                                    main.reconnect_attempts = 0
                                    print(f"{Fore.YELLOW}重置重連計數器，允許新的重連嘗試{Style.RESET_ALL}")
                        else:
                            print(f"{Fore.YELLOW}連接失敗，但處於冷卻期，跳過重連{Style.RESET_ALL}")
                else:
                    # Meshtastic接口為空，嘗試初始連接
                    print(f"{Fore.YELLOW}Meshtastic 未連接{Style.RESET_ALL}")
                    
                    # 檢查冷卻期
                    current_time = time.time()
                    if not hasattr(main, 'last_connection_attempt') or current_time - main.last_connection_attempt > 60:
                        # 嘗試連接
                        try:
                            # 連接到Meshtastic裝置
                            meshtastic_interface = meshtastic.serial_interface.SerialInterface()
                            print(f"{Fore.GREEN}已連接到 Meshtastic 裝置{Style.RESET_ALL}")
                            logging.info("Connected to Meshtastic device")
                            
                            # 設置共享接口
                            set_shared_meshtastic_interface(meshtastic_interface)
                            
                            # 同時也更新API服務器的接口
                            try:
                                import api_server
                                api_server.set_meshtastic_interface(meshtastic_interface)
                                print(f"{Fore.GREEN}API服務器接口已更新（初始連接）{Style.RESET_ALL}")
                            except Exception as api_error:
                                print(f"{Fore.YELLOW}無法更新API服務器接口（初始連接）: {str(api_error)}{Style.RESET_ALL}")
                                logging.warning(f"Could not update API server interface (initial): {str(api_error)}")
                            
                            # 訂閱訊息接收事件
                            pub.subscribe(on_receive, "meshtastic.receive")
                            print(f"{Fore.GREEN}已訂閱 Meshtastic 訊息接收事件{Style.RESET_ALL}")
                            logging.info("Subscribed to Meshtastic message events")
                            
                            # 更新成功連接時間
                            main.last_successful_connection = time.time()
                            main.last_connection_attempt = time.time()
                            main.reconnect_attempts = 0
                        except Exception as e:
                            print(f"{Fore.RED}無法連接 Meshtastic: {str(e)}{Style.RESET_ALL}")
                            logging.error(f"Cannot connect to Meshtastic device: {str(e)}")
                            main.last_connection_attempt = time.time()
                    else:
                        print(f"{Fore.YELLOW}上次連接嘗試太近，等待冷卻期結束{Style.RESET_ALL}")

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

