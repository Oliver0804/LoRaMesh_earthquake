#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
深入測試LLM模型的原始回覆內容
"""

import json
import requests
from call_llm import read_api_key

def test_raw_llm_response(prompt, model="qwen/qwen3-32b:free"):
    """
    測試LLM模型的原始回覆內容，直接訪問API並獲取完整的原始回應
    
    參數:
        prompt (str): 提示詞
        model (str): 要使用的模型
    """
    api_key = read_api_key()
    if not api_key:
        print("無法讀取API金鑰，請確認.key檔案存在且包含有效的金鑰。")
        return
    
    print(f"=== 測試LLM原始回應 ===")
    print(f"提示詞: {prompt}")
    print(f"模型: {model}")
    print("正在發送請求...")
    
    try:
        # 發送請求到API
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "HTTP-Referer": "https://n8n.bashcat.net", 
                "X-Title": "n8n test",
                "Content-Type": "application/json"
            },
            data=json.dumps({
                "model": model,
                "messages": [
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                "max_tokens": 300
            }),
            timeout=300
        )
        
        # 檢查回應狀態
        response.raise_for_status()
        
        # 獲取原始回應
        raw_text = response.text
        print(f"\n=== 原始回應 ===")
        print(f"回應長度: {len(raw_text)} 字節")
        print(f"原始回應內容:")
        print("-" * 50)
        print(raw_text)
        print("-" * 50)
        
        # 解析JSON
        try:
            result = json.loads(raw_text)
            
            # 分析回應結構
            print("\n=== 回應結構分析 ===")
            
            # 檢查基本結構
            print("1. 基本結構:")
            for key in result:
                print(f"   - {key}: {type(result[key])}")
            
            # 分析choices
            if 'choices' in result and len(result['choices']) > 0:
                print("\n2. choices[0] 結構:")
                for key in result['choices'][0]:
                    print(f"   - {key}: {type(result['choices'][0][key])}")
                
                # 分析message
                if 'message' in result['choices'][0]:
                    print("\n3. message 結構:")
                    for key in result['choices'][0]['message']:
                        value = result['choices'][0]['message'][key]
                        print(f"   - {key}: {type(value)}")
                        
                        # 顯示內容
                        if key == 'content':
                            print("\n4. 消息內容:")
                            print("-" * 50)
                            print(value)
                            print("-" * 50)
                            print(f"內容長度: {len(value)} 字符")
            
            # 檢查是否有額外字段
            print("\n5. 檢查其他有用字段:")
            if 'usage' in result:
                print(f"   Token使用情況: {result['usage']}")
            
            return result
            
        except json.JSONDecodeError as json_err:
            print(f"JSON解析錯誤: {json_err}")
            return None
            
    except Exception as e:
        print(f"發生錯誤: {e}")
        return None

def interactive_test():
    """交互式測試介面"""
    models = [
        "qwen/qwen3-32b:free",
        "meta-llama/llama-3.1-8b:free",
        "google/gemma-7b:free"
    ]
    
    # 選擇一個模型
    print("選擇一個模型進行測試:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    model_choice = input("請輸入模型編號 (預設: 1): ") or "1"
    selected_model = models[int(model_choice) - 1]
    
    # 輸入提示詞
    prompt = input("請輸入提示詞: ")
    
    # 執行測試
    test_raw_llm_response(prompt, selected_model)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 如果有命令列參數，直接使用該參數作為提示詞
        test_raw_llm_response(sys.argv[1])
    else:
        # 否則執行交互式測試
        interactive_test()
