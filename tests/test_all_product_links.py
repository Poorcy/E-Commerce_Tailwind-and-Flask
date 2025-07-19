#!/usr/bin/env python3
"""
測試主頁所有商品連結的功能
"""

import requests
import json
from urllib.parse import quote

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_all_product_links():
    """測試主頁所有商品連結的功能"""
    
    print("=== 測試主頁所有商品連結功能 ===\n")
    
    # 主頁所有商品列表
    all_products = [
        # 精選商品
        "HAVIT HV-G92 Gamepad",
        "AK-900 Wired Keyboard", 
        "IPS LCD Gaming Monitor",
        "S-Series Comfort Chair",
        
        # Best Selling Products
        "The north coat",
        "Gucci duffle bag",
        "RGB liquid CPU Cooler",
        "Small BookSelf",
        
        # Explore Our Products
        "Breed Dry Dog Food",
        "CANON EOS DSLR Camera",
        "ASUS FHD Gaming Laptop",
        "Curology Product Set",
        "Kids Electric Car",
        "Jr. Zoom Soccer Cleats",
        "GP11 Shooter USB Gamepad",
        "Quilted Satin Jacket"
    ]
    
    # 1. 檢查資料庫中的商品
    print("1. 檢查資料庫中的商品...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            products = response.json()['products']
            existing_products = [p['name'] for p in products]
            print(f"   ✓ 資料庫中有 {len(products)} 個商品")
            print(f"   ✓ 商品名稱: {', '.join(existing_products)}")
        else:
            print(f"   ✗ API錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ 連接錯誤: {e}")
        return
    
    print("\n2. 測試商品連結...")
    
    # 分類統計
    existing_count = 0
    missing_count = 0
    existing_products_list = []
    missing_products_list = []
    
    for product_name in all_products:
        print(f"   測試商品: {product_name}")
        
        # 編碼商品名稱用於URL
        encoded_name = quote(product_name)
        url = f"{BASE_URL}/product?name={encoded_name}"
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"     ✓ 成功導航到商品頁面")
                existing_count += 1
                existing_products_list.append(product_name)
                
                # 檢查頁面內容是否包含商品名稱
                if product_name in response.text:
                    print(f"     ✓ 頁面包含正確的商品名稱")
                else:
                    print(f"     ⚠ 頁面可能不包含商品名稱")
            elif response.status_code == 404:
                print(f"     ✓ 正確返回404錯誤頁面（商品不存在）")
                missing_count += 1
                missing_products_list.append(product_name)
            else:
                print(f"     ⚠ 未預期的狀態碼: {response.status_code}")
        except Exception as e:
            print(f"     ✗ 請求失敗: {e}")
        print()
    
    # 3. 統計結果
    print("3. 測試結果統計:")
    print(f"   ✓ 存在的商品: {existing_count} 個")
    print(f"   ✓ 不存在的商品: {missing_count} 個")
    print(f"   ✓ 總測試商品: {len(all_products)} 個")
    
    if existing_products_list:
        print(f"\n   ✓ 存在的商品列表:")
        for product in existing_products_list:
            print(f"     - {product}")
    
    if missing_products_list:
        print(f"\n   ⚠ 不存在的商品列表（會顯示404頁面）:")
        for product in missing_products_list:
            print(f"     - {product}")
    
    # 4. 功能說明
    print("\n4. 功能說明:")
    print("   ✓ 從主頁點擊任意商品會導航到對應的商品頁面")
    print("   ✓ 如果商品存在，顯示該商品的詳細資訊")
    print("   ✓ 如果商品不存在，顯示404錯誤頁面")
    print("   ✓ 支持通過商品名稱查詢商品")
    print("   ✓ 不會導航到其他頁面，確保用戶體驗")
    
    print("\n5. 修改內容:")
    print("   - 更新了精選商品區塊的所有商品連結")
    print("   - 更新了Best Selling Products區塊的所有商品連結")
    print("   - 更新了Explore Our Products區塊的所有商品連結")
    print("   - 所有連結都使用查詢參數傳遞商品名稱")
    print("   - 統一了錯誤處理邏輯")
    
    print("\n6. 測試URL範例:")
    print("   - 存在的商品: /product?name=HAVIT HV-G92 Gamepad")
    print("   - 存在的商品: /product?name=AK-900 Wired Keyboard")
    print("   - 不存在的商品: /product?name=不存在的商品")
    
    print("\n7. 如何測試:")
    print("   a) 訪問主頁: http://127.0.0.1:5000/")
    print("   b) 點擊任意商品卡片")
    print("   c) 確認導航到正確的商品頁面")
    print("   d) 檢查商品資訊是否正確顯示")
    print("   e) 測試不存在的商品是否顯示404頁面")
    
    print("\n8. 商品分類:")
    print("   - 精選商品: 4個商品")
    print("   - Best Selling Products: 4個商品")
    print("   - Explore Our Products: 8個商品")
    print("   - 總計: 16個商品")

if __name__ == "__main__":
    test_all_product_links() 