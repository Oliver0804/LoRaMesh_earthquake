#!/usr/bin/env python3
# filepath: /root/python/earthquake/test_api_python.py
import requests
import json
import os
import time

# 從.key檔案讀取API金鑰
def read_api_key(file_path='.key'):
    try:
        with open(file_path, 'r') as file:
            # 讀取金鑰（去除任何註釋和空白）
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('//'):
                    return line
    except Exception as e:
        print(f"讀取API金鑰時發生錯誤: {e}")
        return None

# 讀取API金鑰
api_key = read_api_key()
print(f"使用的API金鑰: {api_key}\n")

# 設定要測試的模型列表
models_to_test = [
    "qwen/qwen3-8b:free",
    "openai/gpt-4o"
]

for model in models_to_test:
    print(f"\n{'='*60}")
    print(f"測試模型: {model}")
    print(f"{'='*60}")
    
    # 發送的提示
    prompt = "請以不超過66個字符回答以下問題（請務必控制在66字以內）：地震是什麼？"
    
    print(f"發送提示: {prompt}")
    start_time = time.time()
    
    try:
        # 使用requests直接調用API
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
                "max_tokens": 100  # 限制token數量以確保回應簡短
            }),
            timeout=120  # 增加超時時間到120秒
        )
        
        # 計算回應時間
        elapsed_time = time.time() - start_time
        print(f"回應時間: {elapsed_time:.2f} 秒")
        
        # 檢查回應狀態
        response.raise_for_status()
        
        # 打印原始回應
        print("\n原始API回應:")
        print(response.text)
        
        # 解析JSON回應
        result = response.json()
        
        # 提取並打印回應內容
        raw_response = result['choices'][0]['message']['content']
        print(f"\n回應內容 (長度: {len(raw_response)} 字符):")
        print(f"'{raw_response}'")
        
        # 檢查是否有空回應
        if not raw_response.strip():
            print("\n收到空回應，檢查reasoning字段...")
            reasoning = result['choices'][0]['message'].get('reasoning', '')
            if reasoning:
                print("\n模型推理過程:")
                print(reasoning)
            else:
                print("沒有找到推理過程。")
        
        # 檢查token使用情況
        if 'usage' in result:
            usage = result['usage']
            print(f"\nToken使用情況:")
            print(f"提示tokens: {usage.get('prompt_tokens', 'N/A')}")
            print(f"完成tokens: {usage.get('completion_tokens', 'N/A')}")
            print(f"總tokens: {usage.get('total_tokens', 'N/A')}")
    
    except Exception as e:
        print(f"\n發生錯誤: {e}")

print("\n測試完成!")
