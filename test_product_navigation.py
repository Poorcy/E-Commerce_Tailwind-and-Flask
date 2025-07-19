#!/usr/bin/env python3
"""
測試商品導航功能
"""

import requests
import json
from urllib.parse import quote

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_product_navigation():
    """測試商品導航功能"""
    
    print("=== 商品導航功能測試 ===\n")
    
    # 1. 檢查資料庫中的商品
    print("1. 檢查資料庫中的商品...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            products = response.json()['products']
            print(f"   ✓ 找到 {len(products)} 個商品:")
            
            for product in products:
                print(f"     - ID: {product['id']}")
                print(f"       名稱: {product['name']}")
                print(f"       價格: ${product['price']}")
                print()
        else:
            print(f"   ✗ API錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ 連接錯誤: {e}")
        return
    
    # 2. 測試商品導航
    print("2. 測試商品導航...")
    
    # 測試存在的商品
    existing_products = [
        "HAVIT HV G-92 Gamepad",
        "AK-900 Wired Keyboard"
    ]
    
    for product_name in existing_products:
        print(f"   測試商品: {product_name}")
        
        # 編碼商品名稱用於URL
        encoded_name = quote(product_name)
        url = f"{BASE_URL}/product?name={encoded_name}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"     ✓ 成功導航到商品頁面")
                # 檢查頁面內容是否包含商品名稱
                if product_name in response.text:
                    print(f"     ✓ 頁面包含正確的商品名稱")
                else:
                    print(f"     ⚠ 頁面可能不包含商品名稱")
            else:
                print(f"     ✗ 導航失敗，狀態碼: {response.status_code}")
        except Exception as e:
            print(f"     ✗ 請求失敗: {e}")
        print()
    
    # 3. 測試不存在的商品
    print("3. 測試不存在的商品...")
    non_existing_products = [
        "不存在的商品",
        "Fake Product Name",
        "Test Product 123"
    ]
    
    for product_name in non_existing_products:
        print(f"   測試商品: {product_name}")
        
        encoded_name = quote(product_name)
        url = f"{BASE_URL}/product?name={encoded_name}"
        
        try:
            response = requests.get(url)
            if response.status_code == 404:
                print(f"     ✓ 正確返回404錯誤頁面")
            else:
                print(f"     ⚠ 未返回404錯誤，狀態碼: {response.status_code}")
        except Exception as e:
            print(f"     ✗ 請求失敗: {e}")
        print()
    
    # 4. 功能說明
    print("4. 功能說明:")
    print("   ✓ 從主頁點擊精選商品會導航到對應的商品頁面")
    print("   ✓ 如果商品存在，顯示該商品的詳細資訊")
    print("   ✓ 如果商品不存在，顯示404錯誤頁面")
    print("   ✓ 支持通過商品名稱查詢商品")
    
    print("\n5. 修改內容:")
    print("   - 修改了商品路由，支持通過查詢參數傳遞商品名稱")
    print("   - 更新了主頁精選商品的連結")
    print("   - 添加了商品不存在時的404處理")
    print("   - 改進了用戶體驗和導航邏輯")
    
    print("\n6. 測試URL範例:")
    print("   - 存在的商品: /product?name=HAVIT HV G-92 Gamepad")
    print("   - 存在的商品: /product?name=AK-900 Wired Keyboard")
    print("   - 不存在的商品: /product?name=不存在的商品")
    
    print("\n7. 如何測試:")
    print("   a) 訪問主頁: http://127.0.0.1:5000/")
    print("   b) 點擊精選商品中的任意商品")
    print("   c) 確認導航到正確的商品頁面")
    print("   d) 檢查商品資訊是否正確顯示")
    print("   e) 測試不存在的商品是否顯示404頁面")

if __name__ == "__main__":
    test_product_navigation() 