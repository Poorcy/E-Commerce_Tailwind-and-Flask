#!/usr/bin/env python3
"""
測試登入功能的腳本
"""

import requests
import re

def test_login():
    """測試登入功能"""
    print("🔧 開始測試登入功能...")
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # 1. 獲取登入頁面
    print("\n1. 獲取登入頁面...")
    response = session.get(f"{base_url}/login")
    content = response.text
    
    csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', content)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f"   ✅ 獲取 CSRF token: {csrf_token[:10]}...")
    else:
        print("   ❌ 無法獲取 CSRF token")
        return False
    
    # 2. 測試不同的用戶名和密碼組合
    test_users = [
        ('simple@test.com', '123456'),
        ('test@example.com', 'testpass'),
        ('admin@example.com', 'admin123'),
        ('user1@example.com', 'password'),
        ('user2@example.com', 'password'),
    ]
    
    for username, password in test_users:
        print(f"\n2. 測試用戶: {username} / {password}")
        
        login_data = {
            'email': username,  # 使用 email 字段
            'password': password,
            'csrf_token': csrf_token
        }
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"   響應狀態碼: {response.status_code}")
        print(f"   重定向到: {response.headers.get('Location', 'None')}")
        print(f"   響應內容: {response.text[:200]}...")
        
        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            if redirect_url == '/':
                print(f"   ✅ 登入成功！用戶: {username}")
                return username, password
            else:
                print(f"   ❌ 登入失敗，重定向到: {redirect_url}")
        else:
            print(f"   ❌ 登入失敗，狀態碼: {response.status_code}")
    
    print("\n❌ 所有用戶登入都失敗")
    return False

if __name__ == "__main__":
    try:
        result = test_login()
        if result:
            username, password = result
            print(f"\n✅ 找到可用的用戶: {username} / {password}")
        else:
            print(f"\n❌ 沒有找到可用的用戶")
    except Exception as e:
        print(f"❌ 測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc() 