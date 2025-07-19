#!/usr/bin/env python3
"""
測試產品頁面的圖片顯示
"""

import requests
from bs4 import BeautifulSoup

def test_product_page_images():
    """測試產品頁面的圖片顯示"""
    
    base_url = "http://localhost:5000"
    
    print("=== 產品頁面圖片測試 ===")
    
    # 測試產品列表
    try:
        response = requests.get(f"{base_url}/admin/products")
        if response.status_code == 200:
            print("✓ 產品管理頁面可訪問")
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找產品圖片
            product_images = soup.find_all('img', class_='h-10 w-10 rounded-full object-cover')
            print(f"找到 {len(product_images)} 個產品圖片")
            
            for img in product_images:
                src = img.get('src')
                alt = img.get('alt', '無名稱')
                print(f"  - {alt}: {src}")
        else:
            print(f"✗ 產品管理頁面無法訪問 (狀態碼: {response.status_code})")
    except Exception as e:
        print(f"✗ 產品管理頁面訪問錯誤: {e}")
    
    # 測試具體產品頁面
    print("\n=== 具體產品頁面測試 ===")
    
    # 測試第一個產品
    try:
        response = requests.get(f"{base_url}/product/1")
        if response.status_code == 200:
            print("✓ 產品頁面1可訪問")
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找主圖片
            main_image = soup.find('img', class_='rounded-xl shadow-lg w-full h-80 object-cover')
            if main_image and hasattr(main_image, 'get'):
                src = main_image.get('src')
                alt = main_image.get('alt', '無名稱')
                print(f"  主圖片: {alt} - {src}")
            else:
                print("  ✗ 未找到主圖片")
            
            # 查找縮略圖
            thumbnails = soup.find_all('img', class_='rounded-lg w-24 h-20 object-cover')
            print(f"  找到 {len(thumbnails)} 個縮略圖")
            
            for i, img in enumerate(thumbnails, 1):
                if hasattr(img, 'get'):
                    src = img.get('src')
                    alt = img.get('alt', '無名稱')
                    print(f"    縮略圖{i}: {alt} - {src}")
        else:
            print(f"✗ 產品頁面1無法訪問 (狀態碼: {response.status_code})")
    except Exception as e:
        print(f"✗ 產品頁面1訪問錯誤: {e}")
    
    # 測試第二個產品
    try:
        response = requests.get(f"{base_url}/product/2")
        if response.status_code == 200:
            print("✓ 產品頁面2可訪問")
            
            # 解析HTML
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 查找主圖片
            main_image = soup.find('img', class_='rounded-xl shadow-lg w-full h-80 object-cover')
            if main_image and hasattr(main_image, 'get'):
                src = main_image.get('src')
                alt = main_image.get('alt', '無名稱')
                print(f"  主圖片: {alt} - {src}")
            else:
                print("  ✗ 未找到主圖片")
        else:
            print(f"✗ 產品頁面2無法訪問 (狀態碼: {response.status_code})")
    except Exception as e:
        print(f"✗ 產品頁面2訪問錯誤: {e}")

if __name__ == '__main__':
    test_product_page_images() 