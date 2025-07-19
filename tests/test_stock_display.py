#!/usr/bin/env python3
"""
測試庫存顯示功能
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_stock_display():
    """測試庫存顯示功能"""
    
    print("=== 庫存顯示功能測試 ===\n")
    
    # 1. 檢查產品API
    print("1. 檢查產品庫存資料...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            products = response.json()['products']
            if products:
                product = products[0]
                print(f"   ✓ 找到產品: {product['name']} (ID: {product['id']})")
                
                # 計算總庫存
                total_stock = sum(variant['stock_quantity'] for variant in product['variants'])
                print(f"   ✓ 總庫存數量: {total_stock} 件")
                
                # 顯示各變體庫存
                if product['variants']:
                    print("   ✓ 各變體庫存:")
                    for variant in product['variants']:
                        color = variant.get('color', 'N/A')
                        size = variant.get('size', 'N/A')
                        stock = variant['stock_quantity']
                        print(f"     - 顏色: {color}, 尺寸: {size}, 庫存: {stock} 件")
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
    
    print("\n2. 庫存顯示功能說明:")
    print("   ✓ 初始狀態顯示總庫存數量")
    print("   ✓ 選擇顏色後顯示該顏色變體的庫存")
    print("   ✓ 選擇尺寸後顯示該尺寸變體的庫存")
    print("   ✓ 庫存為0時顯示紅色警告")
    print("   ✓ 庫存充足時顯示綠色")
    
    print("\n3. 功能特點:")
    print("   - 動態更新庫存顯示")
    print("   - 顏色和尺寸選擇影響庫存顯示")
    print("   - 視覺化庫存狀態（綠色/紅色）")
    print("   - 支援重置選擇回到總庫存")
    
    print("\n4. 如何測試:")
    print("   a) 訪問產品頁面: http://127.0.0.1:5000/product/1")
    print("   b) 查看初始庫存顯示（總庫存）")
    print("   c) 點擊不同顏色按鈕，觀察庫存變化")
    print("   d) 點擊不同尺寸按鈕，觀察庫存變化")
    print("   e) 測試庫存為0的情況")
    
    print("\n5. 預期效果:")
    print("   - 頁面載入時顯示總庫存")
    print("   - 選擇變體後顯示對應庫存")
    print("   - 庫存狀態有顏色區分")
    print("   - 選擇狀態與庫存顯示同步")

if __name__ == "__main__":
    test_stock_display() 