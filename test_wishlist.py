#!/usr/bin/env python3
"""
測試願望清單功能
"""

import requests
import json

BASE_URL = 'http://localhost:5000'

def test_wishlist_functionality():
    """測試願望清單功能"""
    
    # 1. 測試未登入用戶無法訪問願望清單
    print("1. 測試未登入用戶訪問願望清單...")
    response = requests.get(f'{BASE_URL}/wishlist')
    if response.status_code == 302:  # 重定向到登入頁面
        print("✓ 未登入用戶被重定向到登入頁面")
    else:
        print(f"✗ 未登入用戶訪問願望清單失敗: {response.status_code}")
    
    # 2. 測試登入
    print("\n2. 測試登入...")
    login_data = {
        'email': 'test@example.com',
        'password': 'password123'
    }
    session = requests.Session()
    response = session.post(f'{BASE_URL}/login', data=login_data)
    if response.status_code == 200:
        print("✓ 登入成功")
    else:
        print(f"✗ 登入失敗: {response.status_code}")
        return
    
    # 3. 測試添加產品到願望清單
    print("\n3. 測試添加產品到願望清單...")
    add_data = {'product_id': 1}
    response = session.post(f'{BASE_URL}/api/wishlist/add', data=add_data)
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✓ 成功添加產品到願望清單")
        else:
            print(f"✗ 添加失敗: {result.get('message')}")
    else:
        print(f"✗ 添加請求失敗: {response.status_code}")
    
    # 4. 測試檢查願望清單狀態
    print("\n4. 測試檢查願望清單狀態...")
    response = session.get(f'{BASE_URL}/api/wishlist/check/1')
    if response.status_code == 200:
        result = response.json()
        if result.get('in_wishlist'):
            print("✓ 產品確實在願望清單中")
        else:
            print("✗ 產品不在願望清單中")
    else:
        print(f"✗ 檢查請求失敗: {response.status_code}")
    
    # 5. 測試訪問願望清單頁面
    print("\n5. 測試訪問願望清單頁面...")
    response = session.get(f'{BASE_URL}/wishlist')
    if response.status_code == 200:
        print("✓ 成功訪問願望清單頁面")
        if 'HAVIT HV-G92 Gamepad' in response.text:
            print("✓ 願望清單頁面顯示正確的產品")
        else:
            print("✗ 願望清單頁面未顯示產品")
    else:
        print(f"✗ 訪問願望清單頁面失敗: {response.status_code}")
    
    # 6. 測試從願望清單移除產品
    print("\n6. 測試從願望清單移除產品...")
    remove_data = {'product_id': 1}
    response = session.post(f'{BASE_URL}/api/wishlist/remove', data=remove_data)
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print("✓ 成功從願望清單移除產品")
        else:
            print(f"✗ 移除失敗: {result.get('message')}")
    else:
        print(f"✗ 移除請求失敗: {response.status_code}")
    
    # 7. 再次檢查願望清單狀態
    print("\n7. 再次檢查願望清單狀態...")
    response = session.get(f'{BASE_URL}/api/wishlist/check/1')
    if response.status_code == 200:
        result = response.json()
        if not result.get('in_wishlist'):
            print("✓ 產品已從願望清單中移除")
        else:
            print("✗ 產品仍在願望清單中")
    else:
        print(f"✗ 檢查請求失敗: {response.status_code}")

if __name__ == '__main__':
    print("開始測試願望清單功能...")
    test_wishlist_functionality()
    print("\n測試完成！") 