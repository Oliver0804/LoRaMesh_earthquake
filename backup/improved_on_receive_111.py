def on_receive(packet, interface):
    """處理收到的 Meshtastic 訊息"""
    try:
        # 數據驗證：檢查封包是否有效
        if not isinstance(packet, dict):
            error_msg = f"接收到無效封包格式: {type(packet)}"
            logging.warning(error_msg)
            print(f"{Fore.YELLOW}{error_msg}{Style.RESET_ALL}")
            return
            
        # 數據驗證：檢查必要欄位
        if 'decoded' not in packet:
            error_msg = "封包缺少 'decoded' 欄位"
            logging.warning(error_msg)
            print(f"{Fore.YELLOW}{error_msg}{Style.RESET_ALL}")
            return
            
        # 調試：記錄原始封包內容
        if debugMode:
            logging.debug(f"原始封包內容: {packet}")
            
        # 從封包中提取訊息內容和發送者資訊
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
                            try:
                                # 將LLM回應發送到原始頻道
                                interface.sendText(f"{llm_response}", channelIndex=channel)
                                print(f"{Fore.GREEN}已發送LLM回應到頻道 {channel}{Style.RESET_ALL}")
                                logging.info(f"Sent LLM response to channel {channel}: {llm_response}")
                            except Exception as send_error:
                                error_msg = f"發送LLM回應失敗: {str(send_error)[:60]}..."
                                print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
                                logging.error(f"Error sending LLM response: {str(send_error)}")
                        else:
                            print(f"{Fore.YELLOW}無法發送LLM回應：Meshtastic介面不可用{Style.RESET_ALL}")
                            logging.warning("Cannot send LLM response: Meshtastic interface unavailable")
                    else:
                        print(f"{Fore.YELLOW}@bashcat後沒有實際查詢內容{Style.RESET_ALL}")
                        if interface is not None:
                            try:
                                interface.sendText("您好，請在@bashcat後輸入您的問題，例如「@bashcat 什麼是地震？」", channelIndex=channel)
                            except Exception as send_error:
                                print(f"{Fore.RED}發送提示訊息失敗: {str(send_error)[:60]}...{Style.RESET_ALL}")
                                logging.error(f"Error sending prompt message: {str(send_error)}")
                except Exception as llm_error:
                    error_msg = f"LLM回應生成失敗: {str(llm_error)[:60]}..."
                    print(f"{Fore.RED}{error_msg}{Style.RESET_ALL}")
                    logging.error(f"LLM response error: {str(llm_error)}")
                    
                    # 即使LLM失敗，也嘗試發送錯誤訊息
                    if interface is not None:
                        try:
                            interface.sendText(f"[錯誤] {error_msg}", channelIndex=channel)
                        except Exception as send_error:
                            print(f"{Fore.RED}發送錯誤訊息失敗: {str(send_error)}{Style.RESET_ALL}")
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
