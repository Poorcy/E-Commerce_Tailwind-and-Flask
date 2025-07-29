#!/usr/bin/env python3
"""
調試登入頁面的腳本
"""

import requests
import re

def debug_login_page():
    """調試登入頁面"""
    print("🔧 調試登入頁面...")
    
    base_url = "http://localhost:5000"
    session = requests.Session()
    
    # 1. 獲取登入頁面
    print("\n1. 獲取登入頁面...")
    response = session.get(f"{base_url}/login")
    content = response.text
    
    print(f"   響應狀態碼: {response.status_code}")
    print(f"   頁面長度: {len(content)}")
    
    # 檢查是否有錯誤信息
    if 'error' in content.lower() or 'invalid' in content.lower():
        print("   ⚠️ 頁面包含錯誤信息")
    
    # 檢查 CSRF token
    csrf_match = re.search(r'name="csrf_token" value="([^"]+)"', content)
    if csrf_match:
        csrf_token = csrf_match.group(1)
        print(f"   ✅ 找到 CSRF token: {csrf_token[:10]}...")
    else:
        print("   ❌ 沒有找到 CSRF token")
    
    # 檢查表單
    if 'form' in content.lower():
        print("   ✅ 頁面包含表單")
    else:
        print("   ❌ 頁面不包含表單")
    
    # 2. 嘗試登入並檢查響應
    print("\n2. 嘗試登入...")
    
    if csrf_match:
        csrf_token = csrf_match.group(1)
        
        login_data = {
            'username': 'simple',
            'password': '123456',
            'csrf_token': csrf_token
        }
        
        response = session.post(f"{base_url}/login", data=login_data, allow_redirects=False)
        print(f"   登入響應狀態碼: {response.status_code}")
        print(f"   登入響應頭: {dict(response.headers)}")
        
        # 如果有重定向，跟隨重定向
        if response.status_code == 302:
            redirect_url = response.headers.get('Location')
            print(f"   重定向到: {redirect_url}")
            
            if redirect_url:
                response = session.get(f"{base_url}{redirect_url}")
                print(f"   重定向後狀態碼: {response.status_code}")
                print(f"   重定向後內容: {response.text[:500]}...")
                
                # 檢查重定向後的頁面是否有錯誤信息
                if 'error' in response.text.lower() or 'invalid' in response.text.lower():
                    print("   ⚠️ 重定向後頁面包含錯誤信息")
                    
                    # 查找具體的錯誤信息
                    error_patterns = [
                        r'<div[^>]*class="[^"]*error[^"]*"[^>]*>(.*?)</div>',
                        r'<span[^>]*class="[^"]*error[^"]*"[^>]*>(.*?)</span>',
                        r'<p[^>]*class="[^"]*error[^"]*"[^>]*>(.*?)</p>',
                    ]
                    
                    for pattern in error_patterns:
                        matches = re.findall(pattern, response.text, re.IGNORECASE | re.DOTALL)
                        for match in matches:
                            print(f"   錯誤信息: {match.strip()}")
    
    print(f"\n✅ 登入頁面調試完成！")

if __name__ == "__main__":
    try:
        debug_login_page()
    except Exception as e:
        print(f"❌ 調試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc() 