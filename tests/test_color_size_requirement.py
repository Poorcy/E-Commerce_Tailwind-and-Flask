#!/usr/bin/env python3
"""
測試顏色和尺寸選擇要求功能
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_color_size_requirement():
    """測試顏色和尺寸選擇要求"""
    
    print("=== 測試顏色和尺寸選擇要求功能 ===\n")
    
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
            print("請確保測試用戶存在，或先創建測試用戶")
            return
        
        # 2. 檢查產品頁面是否正常載入
        print("\n2. 檢查產品頁面載入...")
        response = session.get(f"{BASE_URL}/product/1")
        if response.status_code == 200:
            print("✓ 產品頁面載入成功")
        else:
            print(f"✗ 產品頁面載入失敗: {response.status_code}")
            return
        
        # 3. 檢查API變體數據
        print("\n3. 檢查產品變體數據...")
        response = session.get(f"{BASE_URL}/api/products/1/variants")
        if response.status_code == 200:
            data = response.json()
            variants = data.get('variants', [])
            print(f"✓ 找到 {len(variants)} 個變體")
            
            if variants:
                print("變體詳情:")
                for variant in variants:
                    print(f"  - 顏色: {variant.get('color', 'N/A')}, 尺寸: {variant.get('size', 'N/A')}, 庫存: {variant.get('stock_quantity', 0)}")
            else:
                print("⚠️ 沒有找到變體數據")
        else:
            print(f"✗ API請求失敗: {response.status_code}")
        
        # 4. 測試未選擇顏色和尺寸時加入購物車
        print("\n4. 測試未選擇顏色和尺寸時加入購物車...")
        cart_data = {
            'product_id': 1,
            'quantity': 1
        }
        response = session.post(f"{BASE_URL}/cart/add", data=cart_data)
        if response.status_code == 200:
            data = response.json()
            if not data.get('success'):
                print("✓ 正確阻止了未選擇顏色和尺寸的加入購物車操作")
                print(f"  錯誤訊息: {data.get('message', '未知錯誤')}")
            else:
                print("⚠️ 意外允許了未選擇顏色和尺寸的加入購物車操作")
        else:
            print(f"✗ 加入購物車請求失敗: {response.status_code}")
        
        # 5. 測試選擇顏色和尺寸後加入購物車
        print("\n5. 測試選擇顏色和尺寸後加入購物車...")
        # 找到第一個有庫存的變體
        if variants:
            first_variant = variants[0]
            cart_data = {
                'product_id': 1,
                'quantity': 1,
                'variant_id': first_variant['id']
            }
            response = session.post(f"{BASE_URL}/cart/add", data=cart_data)
            if response.status_code == 200:
                data = response.json()
                if data.get('success'):
                    print("✓ 成功加入購物車（使用變體ID）")
                else:
                    print(f"✗ 加入購物車失敗: {data.get('message', '未知錯誤')}")
            else:
                print(f"✗ 加入購物車請求失敗: {response.status_code}")
        
        print("\n=== 測試完成 ===")
        print("請在瀏覽器中訪問產品頁面，確認:")
        print("1. 顏色和尺寸選擇按鈕正常顯示")
        print("2. 未選擇顏色和尺寸時，加入購物車按鈕被禁用")
        print("3. 顯示提示文字：'請選擇顏色和尺寸後才能加入購物車'")
        print("4. 選擇顏色和尺寸後，加入購物車按鈕變為可用")
        
    except Exception as e:
        print(f"✗ 測試過程中發生錯誤: {e}")

if __name__ == '__main__':
    test_color_size_requirement() 