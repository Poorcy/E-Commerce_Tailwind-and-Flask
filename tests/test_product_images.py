#!/usr/bin/env python3
"""
測試產品圖片功能
"""

import requests
from app import app, db, Product

def test_product_images():
    """測試產品圖片功能"""
    
    with app.app_context():
        # 獲取所有產品
        products = Product.query.all()
        
        print("=== 產品圖片測試 ===")
        print(f"總共有 {len(products)} 個產品")
        
        for product in products:
            print(f"\n產品: {product.name}")
            print(f"圖片路徑: {product.image_url}")
            
            if product.image_url:
                # 檢查圖片是否存在
                try:
                    with app.test_client() as client:
                        response = client.get(f'/static/{product.image_url}')
                        if response.status_code == 200:
                            print(f"✓ 圖片存在且可訪問")
                        else:
                            print(f"✗ 圖片無法訪問 (狀態碼: {response.status_code})")
                except Exception as e:
                    print(f"✗ 圖片訪問錯誤: {e}")
            else:
                print("⚠ 沒有設置圖片")
        
        # 測試產品頁面
        print("\n=== 產品頁面測試 ===")
        
        for product in products:
            print(f"\n測試產品頁面: {product.name}")
            
            try:
                with app.test_client() as client:
                    # 測試通過ID訪問
                    response = client.get(f'/product/{product.id}')
                    if response.status_code == 200:
                        print(f"✓ 通過ID訪問成功")
                    else:
                        print(f"✗ 通過ID訪問失敗 (狀態碼: {response.status_code})")
                    
                    # 測試通過名稱訪問
                    response = client.get(f'/product?name={product.name}')
                    if response.status_code == 200:
                        print(f"✓ 通過名稱訪問成功")
                    else:
                        print(f"✗ 通過名稱訪問失敗 (狀態碼: {response.status_code})")
                        
            except Exception as e:
                print(f"✗ 頁面訪問錯誤: {e}")

def test_image_selection():
    """測試圖片選擇功能"""
    
    print("\n=== 圖片選擇測試 ===")
    
    # 可用的圖片列表
    available_images = [
        'images/gamepad.png',
        'images/keyboard_300_200.png',
        'images/home_phone.png',
        'images/home_phone2.PNG',
        'images/applelogo.png',
        'images/gamepad1.png',
        'images/gamepad2.png',
        'images/gamepad3.png',
        'images/gamepad4.png',
        'images/mug1.png',
        'images/mug2.png',
        'images/red_apple.png'
    ]
    
    print("可用的圖片:")
    for i, image in enumerate(available_images, 1):
        print(f"{i:2d}. {image}")
    
    # 測試圖片文件是否存在
    print("\n檢查圖片文件:")
    for image in available_images:
        try:
            with app.test_client() as client:
                response = client.get(f'/static/{image}')
                if response.status_code == 200:
                    print(f"✓ {image}")
                else:
                    print(f"✗ {image} (狀態碼: {response.status_code})")
        except Exception as e:
            print(f"✗ {image} (錯誤: {e})")

if __name__ == '__main__':
    test_product_images()
    test_image_selection() 