#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
測試LLM模型調用的回覆內容
"""

from call_llm import generate_response

def test_llm_with_prompt(prompt, max_length=120, model="qwen/qwen3-32b:free"):
    """
    使用指定的提示測試LLM模型回覆
    
    參數:
        prompt (str): 提示詞
        max_length (int): 回覆最大長度
        model (str): 要使用的模型
    """
    print(f"=== 測試LLM回覆 ===")
    print(f"提示詞: {prompt}")
    print(f"模型: {model}")
    print(f"最大長度: {max_length}")
    print("正在發送請求...")
    
    # 調用generate_response函數
    response = generate_response(prompt, max_length, model)
    
    print("\n=== 測試結果 ===")
    print(f"回覆內容: {response}")
    print(f"回覆長度: {len(response)} 字符")
    print("=" * 50)
    
    return response

def run_multiple_tests():
    """執行多個不同的測試案例"""
    test_prompts = [
        "什麼是地震?",
        "地震預警系統如何運作?",
        "如何準備地震應急包?",
        "Tell me about earthquakes in Taiwan",  # 測試英文提示
        "地震" # 測試極短提示
    ]
    
    models = [
        "qwen/qwen3-32b:free",
        "meta-llama/llama-3.1-8b:free",
        "google/gemma-7b:free"
    ]
    
    # 選擇一個模型和一個提示詞進行測試
    print("選擇一個模型進行測試:")
    for i, model in enumerate(models, 1):
        print(f"{i}. {model}")
    
    model_choice = input("請輸入模型編號 (預設: 1): ") or "1"
    selected_model = models[int(model_choice) - 1]
    
    print("\n選擇一個提示詞或輸入自訂提示詞:")
    for i, prompt in enumerate(test_prompts, 1):
        print(f"{i}. {prompt}")
    print(f"{len(test_prompts) + 1}. 自訂提示詞")
    
    prompt_choice = input("請輸入提示詞編號 (預設: 1): ") or "1"
    
    if int(prompt_choice) <= len(test_prompts):
        selected_prompt = test_prompts[int(prompt_choice) - 1]
    else:
        selected_prompt = input("請輸入自訂提示詞: ")
    
    max_length = input("請輸入最大回覆長度 (預設: 120): ") or "120"
    
    # 執行測試
    test_llm_with_prompt(selected_prompt, int(max_length), selected_model)

if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1:
        # 如果有命令列參數，直接使用該參數作為提示詞
        test_llm_with_prompt(sys.argv[1])
    else:
        # 否則執行交互式測試
        run_multiple_tests()
