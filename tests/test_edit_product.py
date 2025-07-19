#!/usr/bin/env python3
"""
測試產品編輯功能
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_edit_product():
    """測試編輯產品功能"""
    
    print("=== 產品編輯功能測試 ===\n")
    
    # 1. 首先獲取所有產品
    print("1. 獲取所有產品...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            products = response.json()['products']
            if products:
                product = products[0]  # 使用第一個產品進行測試
                print(f"   找到產品: {product['name']} (ID: {product['id']})")
                print(f"   當前價格: ${product['price']}")
                print(f"   變體數量: {len(product['variants'])}")
                
                # 顯示現有變體
                if product['variants']:
                    print("   現有變體:")
                    for variant in product['variants']:
                        print(f"     - 顏色: {variant['color']}, 尺寸: {variant['size']}, 庫存: {variant['stock_quantity']}")
            else:
                print("   沒有找到產品，請先新增產品")
                return
        else:
            print(f"   錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"   連接錯誤: {e}")
        return
    
    print("\n2. 編輯產品步驟說明:")
    print("   a) 訪問產品管理頁面: http://127.0.0.1:5000/admin/products")
    print("   b) 在產品列表中找到要編輯的產品")
    print("   c) 點擊該產品行的「編輯」按鈕")
    print("   d) 在編輯頁面修改以下內容:")
    print("      - 產品名稱")
    print("      - 產品描述")
    print("      - 基本價格")
    print("      - 類別")
    print("      - 圖片網址")
    print("   e) 修改產品變體:")
    print("      - 顏色")
    print("      - 尺寸")
    print("      - 庫存數量")
    print("   f) 可以新增或移除變體")
    print("   g) 點擊「更新產品」儲存變更")
    
    print("\n3. 編輯頁面功能:")
    print("   - 產品基本資訊區塊：修改名稱、價格、描述等")
    print("   - 產品變體區塊：管理顏色、尺寸、庫存")
    print("   - 新增變體：點擊「新增變體」按鈕")
    print("   - 移除變體：點擊變體行右側的「移除」按鈕")
    print("   - 儲存：點擊「更新產品」按鈕")
    print("   - 取消：點擊「取消」按鈕返回")
    
    print("\n4. 注意事項:")
    print("   - 產品名稱和價格為必填欄位")
    print("   - 庫存數量必須為非負整數")
    print("   - 至少需要保留一個產品變體")
    print("   - 編輯完成後會自動跳轉到產品詳情頁面")
    print("   - 成功編輯會顯示綠色成功訊息")

if __name__ == "__main__":
    test_edit_product() 