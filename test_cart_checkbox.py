#!/usr/bin/env python3
"""
測試購物車勾選功能
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_cart_checkbox():
    """測試購物車勾選功能"""
    
    print("=== 測試購物車勾選功能 ===\n")
    
    # 創建會話來保持登入狀態
    session = requests.Session()
    
    try:
        # 1. 登入測試用戶
        print("1. 登入測試用戶...")
        login_data = {
            'email': 'test@example.com',
            'password': 'testpass'
        }
        response = session.post(f"{BASE_URL}/login", data=login_data)
        if response.status_code == 200:
            print("✓ 登入成功")
        else:
            print(f"✗ 登入失敗: {response.status_code}")
            return
        
        # 2. 檢查購物車頁面
        print("\n2. 檢查購物車頁面...")
        response = session.get(f"{BASE_URL}/cart")
        if response.status_code == 200:
            print("✓ 購物車頁面載入成功")
            # 檢查是否包含勾選框
            if 'select-all' in response.text:
                print("✓ 找到全選勾選框")
            if 'item-checkbox' in response.text:
                print("✓ 找到商品勾選框")
        else:
            print(f"✗ 購物車頁面載入失敗: {response.status_code}")
            return
        
        # 3. 測試API端點
        print("\n3. 測試選中商品API...")
        # 先獲取購物車中的商品
        response = session.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            data = response.json()
            products = data.get('products', [])
            if products:
                # 添加商品到購物車
                product = products[0]
                cart_data = {
                    'product_id': product['id'],
                    'quantity': 2
                }
                response = session.post(f"{BASE_URL}/cart/add", data=cart_data)
                if response.status_code == 200:
                    print("✓ 成功添加商品到購物車")
                    
                    # 測試選中商品API
                    selected_data = {
                        'item_ids': [1]  # 假設第一個商品ID為1
                    }
                    response = session.post(f"{BASE_URL}/api/cart/selected", 
                                          json=selected_data)
                    if response.status_code == 200:
                        data = response.json()
                        if data.get('success'):
                            print("✓ 選中商品API正常工作")
                            items = data.get('items', [])
                            print(f"  找到 {len(items)} 個選中商品")
                        else:
                            print(f"✗ API返回錯誤: {data.get('message')}")
                    else:
                        print(f"✗ 選中商品API請求失敗: {response.status_code}")
                else:
                    print("✗ 添加商品到購物車失敗")
            else:
                print("⚠️ 沒有找到商品")
        else:
            print(f"✗ 獲取商品列表失敗: {response.status_code}")
        
        print("\n=== 測試完成 ===")
        print("請在瀏覽器中訪問購物車頁面，確認:")
        print("1. 每個商品前都有勾選框")
        print("2. 表頭有全選/取消全選功能")
        print("3. 勾選商品後總計會動態更新")
        print("4. 只有選中商品時結帳按鈕才可用")
        print("5. 結帳頁面只顯示選中的商品")
        
    except Exception as e:
        print(f"✗ 測試過程中發生錯誤: {e}")

if __name__ == '__main__':
    test_cart_checkbox() 