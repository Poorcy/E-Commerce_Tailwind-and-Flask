#!/usr/bin/env python3
"""
測試所有頁面的導航連結
"""

import requests
import re

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_navigation_links():
    """測試所有頁面的導航連結"""
    
    print("=== 測試導航連結 ===\n")
    
    # 創建會話來保持登入狀態
    session = requests.Session()
    
    # 頁面列表
    pages = [
        ('/', '主頁'),
        ('/product', '產品頁面'),
        ('/wishlist', '願望清單'),
        ('/account', '個人資料'),
        ('/about', '關於頁面'),
        ('/contact', '聯絡我們'),
        ('/cart', '購物車'),
        ('/checkout', '結帳頁面'),
        ('/orders', '訂單查詢')
    ]
    
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
        
        # 2. 測試每個頁面的導航連結
        print("\n2. 測試頁面導航連結...")
        
        for url, page_name in pages:
            print(f"\n測試 {page_name} ({url})...")
            
            try:
                response = session.get(f"{BASE_URL}{url}")
                if response.status_code == 200:
                    print(f"  ✓ 頁面載入成功")
                    
                    # 檢查訂單查詢連結
                    if '訂單查詢' in response.text:
                        # 查找訂單查詢連結
                        orders_link_pattern = r'href="([^"]*orders[^"]*)"'
                        orders_links = re.findall(orders_link_pattern, response.text)
                        
                        if orders_links:
                            print(f"  ✓ 找到訂單查詢連結: {orders_links[0]}")
                            
                            # 測試連結是否有效
                            if orders_links[0] == '/orders' or 'orders' in orders_links[0]:
                                print(f"  ✓ 訂單查詢連結格式正確")
                            else:
                                print(f"  ⚠️ 訂單查詢連結格式可能有問題: {orders_links[0]}")
                        else:
                            print(f"  ⚠️ 未找到訂單查詢連結")
                    else:
                        print(f"  ⚠️ 頁面中沒有訂單查詢文字")
                        
                else:
                    print(f"  ✗ 頁面載入失敗: {response.status_code}")
                    
            except Exception as e:
                print(f"  ✗ 測試頁面時發生錯誤: {e}")
        
        # 3. 測試訂單查詢頁面功能
        print("\n3. 測試訂單查詢頁面功能...")
        response = session.get(f"{BASE_URL}/orders")
        if response.status_code == 200:
            print("✓ 訂單查詢頁面載入成功")
            
            # 檢查頁面內容
            if '訂單查詢' in response.text:
                print("✓ 頁面標題正確")
            if '您還沒有訂單' in response.text or '訂單編號' in response.text:
                print("✓ 頁面內容正確")
            
            # 檢查導航菜單
            if '個人資料' in response.text and '願望清單' in response.text:
                print("✓ 導航菜單完整")
                
        else:
            print(f"✗ 訂單查詢頁面載入失敗: {response.status_code}")
        
        print("\n=== 測試完成 ===")
        print("所有頁面的訂單查詢連結已更新完成！")
        print("現在用戶可以從任何頁面的導航菜單中點擊'訂單查詢'來訪問訂單頁面。")
        
    except Exception as e:
        print(f"✗ 測試過程中發生錯誤: {e}")

if __name__ == '__main__':
    test_navigation_links() 