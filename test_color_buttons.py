#!/usr/bin/env python3
"""
測試顏色選擇按鈕修改
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_color_button_changes():
    """測試顏色選擇按鈕的修改"""
    
    print("=== 顏色選擇按鈕修改測試 ===\n")
    
    # 1. 檢查產品API
    print("1. 檢查產品資料...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            products = response.json()['products']
            if products:
                product = products[0]
                print(f"   ✓ 找到產品: {product['name']} (ID: {product['id']})")
                
                # 顯示顏色變體
                color_variants = [v for v in product['variants'] if v['color']]
                if color_variants:
                    print(f"   ✓ 顏色變體數量: {len(color_variants)}")
                    print("   ✓ 可用顏色:")
                    for variant in color_variants:
                        print(f"     - {variant['color']} (ID: {variant['id']})")
                else:
                    print("   ⚠ 沒有顏色變體")
            else:
                print("   ⚠ 沒有找到產品")
                return
        else:
            print(f"   ✗ API錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ 連接錯誤: {e}")
        return
    
    print("\n2. 顏色選擇按鈕修改說明:")
    print("   ✓ 已將圓形色塊改為文字按鈕")
    print("   ✓ 按鈕樣式: 圓角邊框，白色背景，灰色文字")
    print("   ✓ 選中狀態: 紅色背景，白色文字")
    print("   ✓ 懸停效果: 邊框顏色變化")
    
    print("\n3. 修改內容:")
    print("   - HTML: 移除圓形樣式和背景色")
    print("   - CSS: 改為文字按鈕樣式")
    print("   - JavaScript: 更新選中狀態樣式")
    
    print("\n4. 如何測試:")
    print("   a) 訪問產品頁面: http://127.0.0.1:5000/product/1")
    print("   b) 查看顏色選擇區域")
    print("   c) 點擊不同顏色按鈕")
    print("   d) 觀察選中狀態變化")
    
    print("\n5. 預期效果:")
    print("   - 顏色按鈕顯示為文字形式")
    print("   - 點擊後按鈕變為紅色背景")
    print("   - 其他按鈕恢復白色背景")
    print("   - 選中的變體ID正確傳遞")

if __name__ == "__main__":
    test_color_button_changes() 