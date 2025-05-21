# 修改的Meshtastic連接管理代碼段
# 在main函數中，替換現有的連接檢查代碼

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
                        if meshtastic_interface:
                            meshtastic_interface.close()
                        # 增加連接超時設置為30秒
                        meshtastic_interface = meshtastic.serial_interface.SerialInterface(connectTimeout=30)
                        print(f"{Fore.GREEN}已重新連接到 Meshtastic 裝置{Style.RESET_ALL}")
                        logging.info("Reconnected to Meshtastic device")
                        
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
                # 增加連接超時設置為30秒
                meshtastic_interface = meshtastic.serial_interface.SerialInterface(connectTimeout=30)
                print(f"{Fore.GREEN}已連接到 Meshtastic 裝置{Style.RESET_ALL}")
                logging.info("Connected to Meshtastic device")
                
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
