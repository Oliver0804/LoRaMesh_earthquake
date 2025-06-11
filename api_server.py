#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import logging
from datetime import datetime
from flask import Flask, request, jsonify
from flask_cors import CORS
import threading
import time
from colorama import Fore, Style
import meshtastic
import meshtastic.serial_interface

app = Flask(__name__)
CORS(app)  # 允許跨域請求

# 設置API專用日誌
api_log_file = f"./logs/api_{datetime.now().strftime('%Y-%m-%d')}.log"
api_logger = logging.getLogger('api_server')
api_handler = logging.FileHandler(api_log_file)
api_handler.setFormatter(logging.Formatter('%(asctime)s %(levelname)s %(message)s'))
api_logger.addHandler(api_handler)
api_logger.setLevel(logging.INFO)

# 全局變數用於存儲從主程式傳遞的Meshtastic接口
_shared_interface = None
_interface_lock = threading.Lock()

def set_meshtastic_interface(interface):
    """由主程式調用來設置共享的Meshtastic接口"""
    global _shared_interface
    with _interface_lock:
        _shared_interface = interface
        api_logger.info(f"Shared Meshtastic interface updated: {interface is not None}")

def get_shared_meshtastic_interface():
    """從共享變數取得Meshtastic接口"""
    global _shared_interface
    with _interface_lock:
        return _shared_interface

def send_meshtastic_message_api(message, channel=2):
    """通過Meshtastic發送訊息（API專用版本）"""
    try:
        # 數據清理
        if not isinstance(message, str):
            message = str(message) if message is not None else ""
            
        # 過濾可能導致解析錯誤的字符
        message = message.replace('\x00', '').replace('\0', '')
        
        # 訊息大小限制檢查
        if len(message.encode('utf-8')) > 200:
            api_logger.warning(f"Message too large ({len(message.encode('utf-8'))} bytes), truncating")
            message = message[:197] + "..."
        
        # 獲取共享的Meshtastic接口
        interface = get_shared_meshtastic_interface()
        if interface is None:
            # 如果沒有共享接口，返回錯誤而不是嘗試創建臨時接口
            error_msg = "Meshtastic接口未可用，請確保main.py正在運行"
            api_logger.error(error_msg)
            return False, error_msg
        
        # 使用共享接口發送訊息
        interface.sendText(message, channelIndex=channel)
        
        api_logger.info(f"API message sent to channel {channel}: {message}")
        print(f"{Fore.GREEN}API服務器：訊息已發送到頻道 {channel}: {message}{Style.RESET_ALL}")
        return True, "訊息發送成功"
        
    except Exception as e:
        error_msg = f"發送訊息時出錯: {str(e)}"
        api_logger.error(error_msg)
        print(f"{Fore.RED}API服務器：{error_msg}{Style.RESET_ALL}")
        return False, error_msg

@app.route('/health', methods=['GET'])
def health_check():
    """健康檢查端點"""
    interface = get_shared_meshtastic_interface()
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'meshtastic_connected': interface is not None
    })

@app.route('/send', methods=['POST'])
def send_message():
    """發送訊息到Meshtastic網絡"""
    try:
        # 檢查請求數據
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': '請求必須是JSON格式'
            }), 400
        
        data = request.get_json()
        
        # 驗證必要欄位
        if 'message' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要欄位: message'
            }), 400
        
        message = data['message']
        channel = data.get('channel', 2)  # 預設頻道2
        
        # 驗證頻道範圍
        if not isinstance(channel, int) or channel < 0 or channel > 7:
            return jsonify({
                'success': False,
                'error': '頻道必須是0-7之間的整數'
            }), 400
        
        # 驗證訊息長度
        if not message or len(message.strip()) == 0:
            return jsonify({
                'success': False,
                'error': '訊息內容不能為空'
            }), 400
        
        # 記錄API請求
        client_ip = request.remote_addr
        api_logger.info(f"API request from {client_ip}: channel={channel}, message='{message}'")
        print(f"{Fore.CYAN}API請求來自 {client_ip}: 頻道={channel}, 訊息='{message}'{Style.RESET_ALL}")
        
        # 發送訊息
        success, result_msg = send_meshtastic_message_api(message, channel)
        
        if success:
            return jsonify({
                'success': True,
                'message': result_msg,
                'data': {
                    'sent_message': message,
                    'channel': channel,
                    'timestamp': datetime.now().isoformat()
                }
            })
        else:
            return jsonify({
                'success': False,
                'error': result_msg
            }), 500
            
    except Exception as e:
        error_msg = f"處理請求時發生錯誤: {str(e)}"
        api_logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/send/broadcast', methods=['POST'])
def broadcast_message():
    """廣播訊息到多個頻道"""
    try:
        if not request.is_json:
            return jsonify({
                'success': False,
                'error': '請求必須是JSON格式'
            }), 400
        
        data = request.get_json()
        
        if 'message' not in data:
            return jsonify({
                'success': False,
                'error': '缺少必要欄位: message'
            }), 400
        
        message = data['message']
        channels = data.get('channels', [1, 2, 3])  # 預設廣播到頻道1, 2, 3
        
        # 驗證頻道列表
        if not isinstance(channels, list) or len(channels) == 0:
            return jsonify({
                'success': False,
                'error': '頻道必須是非空列表'
            }), 400
        
        # 驗證每個頻道
        for channel in channels:
            if not isinstance(channel, int) or channel < 0 or channel > 7:
                return jsonify({
                    'success': False,
                    'error': f'無效頻道: {channel}，頻道必須是0-7之間的整數'
                }), 400
        
        # 記錄廣播請求
        client_ip = request.remote_addr
        api_logger.info(f"Broadcast request from {client_ip}: channels={channels}, message='{message}'")
        print(f"{Fore.CYAN}廣播請求來自 {client_ip}: 頻道={channels}, 訊息='{message}'{Style.RESET_ALL}")
        
        # 發送到每個頻道
        results = []
        for channel in channels:
            success, result_msg = send_meshtastic_message_api(message, channel)
            results.append({
                'channel': channel,
                'success': success,
                'message': result_msg
            })
            # 在頻道間稍作延遲，避免過快發送
            time.sleep(0.5)
        
        # 檢查是否有任何成功的發送
        successful_sends = [r for r in results if r['success']]
        
        return jsonify({
            'success': len(successful_sends) > 0,
            'message': f'成功發送到 {len(successful_sends)}/{len(channels)} 個頻道',
            'data': {
                'sent_message': message,
                'results': results,
                'timestamp': datetime.now().isoformat()
            }
        })
        
    except Exception as e:
        error_msg = f"處理廣播請求時發生錯誤: {str(e)}"
        api_logger.error(error_msg)
        return jsonify({
            'success': False,
            'error': error_msg
        }), 500

@app.route('/status', methods=['GET'])
def get_status():
    """獲取系統狀態"""
    try:
        interface = get_shared_meshtastic_interface()
        meshtastic_status = "已連接" if interface is not None else "未連接"
        
        return jsonify({
            'success': True,
            'data': {
                'api_server': '運行中',
                'meshtastic_connection': meshtastic_status,
                'timestamp': datetime.now().isoformat(),
                'uptime': time.time() - start_time if 'start_time' in globals() else 0
            }
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': f"獲取狀態時發生錯誤: {str(e)}"
        }), 500

@app.errorhandler(404)
def not_found(error):
    return jsonify({
        'success': False,
        'error': '找不到請求的端點'
    }), 404

@app.errorhandler(500)
def internal_error(error):
    return jsonify({
        'success': False,
        'error': '服務器內部錯誤'
    }), 500

def run_api_server(host='0.0.0.0', port=5000):
    """運行API服務器"""
    global start_time
    start_time = time.time()
    
    print(f"{Fore.GREEN}啟動API服務器...{Style.RESET_ALL}")
    print(f"{Fore.GREEN}API端點：{Style.RESET_ALL}")
    print(f"  - GET  http://{host}:{port}/health     - 健康檢查")
    print(f"  - GET  http://{host}:{port}/status     - 系統狀態")
    print(f"  - POST http://{host}:{port}/send       - 發送訊息")
    print(f"  - POST http://{host}:{port}/send/broadcast - 廣播訊息")
    
    api_logger.info(f"API server starting on {host}:{port}")
    
    try:
        app.run(host=host, port=port, debug=False, threaded=True)
    except Exception as e:
        print(f"{Fore.RED}API服務器啟動失敗: {str(e)}{Style.RESET_ALL}")
        api_logger.error(f"Failed to start API server: {str(e)}")

if __name__ == '__main__':
    run_api_server()
