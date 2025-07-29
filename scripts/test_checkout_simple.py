#!/usr/bin/env python3
"""
簡單的結帳功能測試腳本
"""

import requests
import re
import json

def test_checkout_simple():
    """簡單的結帳功能測試"""
    print("🔧 開始簡單的結帳功能測試...")
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # 1. 登入
    print("\n1. 登入...")
    response = session.get(f"{base_url}/login")
    content = response.text
    
    csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', content)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f"   ✅ 獲取 CSRF token: {csrf_token[:10]}...")
    else:
        print("   ❌ 無法獲取 CSRF token")
        return False
    
    login_data = {
        'email': 'simple@test.com',
        'password': '123456',
        'csrf_token': csrf_token
    }
    
    response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
    print(f"   登入響應狀態碼: {response.status_code}")
    print(f"   登入響應頭: {dict(response.headers)}")
    print(f"   登入響應內容: {response.text[:500]}...")
    
    if response.status_code in [200, 302]:
        print("   ✅ 登入成功")
        # 如果有重定向，跟隨重定向
        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            if redirect_url:
                print(f"   跟隨重定向到: {redirect_url}")
                response = session.get(f"{base_url}{redirect_url}")
    else:
        print(f"   ❌ 登入失敗: {response.status_code}")
        print(f"   響應內容: {response.text}")
        return False
    
    # 2. 訪問結帳頁面
    print("\n2. 訪問結帳頁面...")
    response = session.get(f"{base_url}/checkout")
    content = response.text
    
    if 'csrf_token' in content:
        print("   ✅ 結帳頁面包含 CSRF token")
    else:
        print("   ❌ 結帳頁面缺少 CSRF token")
        return False
    
    # 3. 測試 /api/cart/selected API
    print("\n3. 測試 /api/cart/selected API...")
    
    # 獲取結帳頁面的 CSRF token
    csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', content)
    if csrf_match:
        checkout_csrf_token = csrf_match.group(1)
        print(f"   ✅ 獲取結帳頁面 CSRF token: {checkout_csrf_token[:10]}...")
    else:
        print("   ❌ 無法獲取結帳頁面 CSRF token")
        return False
    
    # 測試 API 調用（使用實際存在的購物車項目ID）
    api_data = {
        'item_ids': [13, 14],  # 新創建的購物車項目ID
        'csrf_token': checkout_csrf_token
    }
    
    headers = {
        'Content-Type': 'application/json',
        'X-CSRFToken': checkout_csrf_token
    }
    
    print(f"   發送請求到 /api/cart/selected...")
    print(f"   請求數據: {api_data}")
    print(f"   請求頭: {headers}")
    
    response = session.post(f"{base_url}/api/cart/selected", 
                           json=api_data, 
                           headers=headers)
    
    print(f"   響應狀態碼: {response.status_code}")
    print(f"   響應內容: {response.text[:200]}...")
    
    if response.status_code == 200:
        data = response.json()
        if data.get('success'):
            print("   ✅ API 調用成功")
            items = data.get('items', [])
            print(f"   返回 {len(items)} 個商品")
            for item in items:
                print(f"   - {item.get('name')}: ${item.get('price')} x {item.get('quantity')}")
        else:
            print(f"   ❌ API 返回錯誤: {data.get('message')}")
            return False
    else:
        print(f"   ❌ API 調用失敗: {response.status_code}")
        print(f"   完整響應: {response.text}")
        return False
    
    print(f"\n✅ 結帳功能測試完成！")
    return True

if __name__ == "__main__":
    try:
        test_checkout_simple()
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc() 