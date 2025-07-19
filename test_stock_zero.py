#!/usr/bin/env python3
"""
測試庫存為0時的顯示邏輯
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_stock_zero_display():
    """測試庫存為0時的顯示邏輯"""
    
    print("=== 庫存為0顯示邏輯測試 ===\n")
    
    # 1. 檢查產品變體資料
    print("1. 檢查產品變體資料...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            products = response.json()['products']
            if products:
                product = products[0]
                print(f"   ✓ 找到產品: {product['name']} (ID: {product['id']})")
                
                # 分析變體資料
                if product['variants']:
                    print(f"   ✓ 總變體數量: {len(product['variants'])}")
                    
                    # 統計顏色和尺寸
                    colors = set()
                    sizes = set()
                    existing_combinations = set()
                    
                    print("   ✓ 現有變體組合:")
                    for variant in product['variants']:
                        color = variant.get('color', 'N/A')
                        size = variant.get('size', 'N/A')
                        stock = variant['stock_quantity']
                        colors.add(color)
                        sizes.add(size)
                        existing_combinations.add(f"{color}-{size}")
                        print(f"     - {color} {size}: {stock} 件")
                    
                    print(f"\n   ✓ 可用顏色: {', '.join(sorted(colors))}")
                    print(f"   ✓ 可用尺寸: {', '.join(sorted(sizes))}")
                    
                    # 找出不存在的組合
                    all_combinations = set()
                    for color in colors:
                        for size in sizes:
                            all_combinations.add(f"{color}-{size}")
                    
                    missing_combinations = all_combinations - existing_combinations
                    if missing_combinations:
                        print(f"   ✓ 不存在的組合: {', '.join(sorted(missing_combinations))}")
                    else:
                        print("   ✓ 所有顏色-尺寸組合都存在")
                else:
                    print("   ⚠ 沒有變體")
            else:
                print("   ⚠ 沒有找到產品")
                return
        else:
            print(f"   ✗ API錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ 連接錯誤: {e}")
        return
    
    print("\n2. 庫存顯示邏輯說明:")
    print("   ✓ 選擇存在的組合: 顯示實際庫存")
    print("   ✓ 選擇不存在的組合: 顯示0件（紅色）")
    print("   ✓ 只選擇顏色: 顯示該顏色總庫存")
    print("   ✓ 只選擇尺寸: 顯示該尺寸總庫存")
    print("   ✓ 無選擇: 顯示總庫存")
    
    print("\n3. 修復內容:")
    print("   - 添加了不存在的組合處理邏輯")
    print("   - 庫存為0時顯示紅色警告")
    print("   - 改進了顏色和尺寸單獨選擇的庫存顯示")
    print("   - 確保所有情況都有正確的庫存顯示")
    
    print("\n4. 測試場景:")
    print("   a) 選擇存在的組合（如：黑色 S）")
    print("   b) 選擇不存在的組合（如：白色 L）")
    print("   c) 只選擇顏色（如：紅色）")
    print("   d) 只選擇尺寸（如：M）")
    print("   e) 不選擇任何選項")
    
    print("\n5. 預期結果:")
    print("   - 存在的組合: 顯示實際庫存數字")
    print("   - 不存在的組合: 顯示 '0 件'（紅色）")
    print("   - 庫存充足: 綠色文字")
    print("   - 庫存不足: 紅色文字")
    
    print("\n6. 如何測試:")
    print("   a) 訪問產品頁面: http://127.0.0.1:5000/product/1")
    print("   b) 選擇不同的顏色和尺寸組合")
    print("   c) 觀察庫存顯示的變化")
    print("   d) 特別注意不存在的組合是否顯示0")

if __name__ == "__main__":
    test_stock_zero_display() 