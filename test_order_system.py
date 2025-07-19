#!/usr/bin/env python3
"""
測試訂單系統功能
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_order_system():
    """測試訂單系統功能"""
    
    print("=== 測試訂單系統功能 ===\n")
    
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
        
        # 2. 檢查訂單查詢頁面
        print("\n2. 檢查訂單查詢頁面...")
        response = session.get(f"{BASE_URL}/orders")
        if response.status_code == 200:
            print("✓ 訂單查詢頁面載入成功")
            if '訂單查詢' in response.text:
                print("✓ 頁面標題正確")
            if '您還沒有訂單' in response.text:
                print("✓ 空訂單狀態顯示正確")
        else:
            print(f"✗ 訂單查詢頁面載入失敗: {response.status_code}")
            return
        
        # 3. 檢查結帳頁面
        print("\n3. 檢查結帳頁面...")
        response = session.get(f"{BASE_URL}/checkout")
        if response.status_code == 200:
            print("✓ 結帳頁面載入成功")
            if '結帳' in response.text:
                print("✓ 頁面標題正確")
        else:
            print(f"✗ 結帳頁面載入失敗: {response.status_code}")
            return
        
        # 4. 測試訂單提交API（模擬）
        print("\n4. 測試訂單提交API...")
        # 注意：這裡只是測試API端點是否存在，實際提交需要購物車中有商品
        test_data = {
            'name': '測試用戶',
            'phone': '0912345678',
            'address': '測試地址',
            'payment': 'credit',
            'selected_items': '[]'
        }
        response = session.post(f"{BASE_URL}/checkout/submit", data=test_data)
        if response.status_code == 200:
            data = response.json()
            if not data.get('success'):
                print("✓ API端點正常工作（返回預期的錯誤信息）")
            else:
                print("⚠️ API返回成功，但這可能不是預期的")
        else:
            print(f"⚠️ API請求失敗: {response.status_code}")
        
        print("\n=== 測試完成 ===")
        print("請在瀏覽器中測試以下功能:")
        print("1. 訪問購物車頁面並選擇商品")
        print("2. 點擊結帳按鈕進入結帳頁面")
        print("3. 填寫收件信息並提交訂單")
        print("4. 查看訂單查詢頁面確認訂單已創建")
        print("5. 確認預計抵達日期為7天後")
        
    except Exception as e:
        print(f"✗ 測試過程中發生錯誤: {e}")

if __name__ == '__main__':
    test_order_system() 