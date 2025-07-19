#!/usr/bin/env python3
"""
為現有產品分配對應的圖片
"""

from app import app, db, Product

def assign_product_images():
    """為產品分配對應的圖片"""
    
    # 產品名稱到圖片的映射
    product_image_mapping = {
        'Havic HV G-92 Gamepad': 'images/gamepad.png',
        'AK-900 Wired Keyboard': 'images/keyboard_300_200.png',
        'IPS LCD Gaming Monitor': 'images/home_phone.png',
        'S-Series Comfort Chair': 'images/home_phone2.PNG',
        'Apple Watch Series 7': 'images/applelogo.png',
        'iPhone 14 Pro': 'images/home_phone.png',
        'MacBook Pro 16': 'images/home_phone2.PNG',
        'Sony WH-1000XM4': 'images/gamepad1.png',
        'Samsung Galaxy S21': 'images/gamepad2.png',
        'Nike Air Max 270': 'images/gamepad3.png',
        'Adidas Ultraboost 21': 'images/gamepad4.png',
        'Apple AirPods Pro': 'images/applelogo.png',
        'Sony PlayStation 5': 'images/gamepad.png',
        'Microsoft Xbox Series X': 'images/gamepad1.png',
        'Nintendo Switch': 'images/gamepad2.png',
        'Canon EOS R5': 'images/gamepad3.png',
        'Sony A7 III': 'images/gamepad4.png',
        'DJI Mavic Air 2': 'images/home_phone.png',
        'GoPro Hero 9': 'images/home_phone2.PNG',
        'Samsung QLED 4K TV': 'images/gamepad.png',
        'LG OLED 4K TV': 'images/gamepad1.png',
        'Bose QuietComfort 35': 'images/gamepad2.png',
        'Sennheiser HD 660S': 'images/gamepad3.png',
        'Logitech MX Master 3': 'images/gamepad4.png',
        'Razer DeathAdder V2': 'images/gamepad.png',
        'SteelSeries Arctis 7': 'images/gamepad1.png',
        'Corsair K95 RGB': 'images/gamepad2.png',
        'HyperX Cloud II': 'images/gamepad3.png',
        'ASUS ROG Strix G15': 'images/gamepad4.png',
        'Lenovo ThinkPad X1': 'images/home_phone.png',
        'Dell XPS 13': 'images/home_phone2.PNG',
        'HP Spectre x360': 'images/gamepad.png',
        'Acer Swift 3': 'images/gamepad1.png',
        'MSI GS66 Stealth': 'images/gamepad2.png',
        'Alienware m15 R4': 'images/gamepad3.png',
        'Razer Blade 15': 'images/gamepad4.png',
        'MacBook Air M1': 'images/applelogo.png',
        'iPad Pro 12.9': 'images/applelogo.png',
        'iPad Air': 'images/applelogo.png',
        'Apple TV 4K': 'images/applelogo.png',
        'HomePod mini': 'images/applelogo.png',
        'AirTag': 'images/applelogo.png',
        'MagSafe Charger': 'images/applelogo.png',
        'Apple Pencil': 'images/applelogo.png',
        'Magic Keyboard': 'images/applelogo.png',
        'Magic Mouse': 'images/applelogo.png',
        'Magic Trackpad': 'images/applelogo.png',
        'Studio Display': 'images/applelogo.png',
        'Pro Display XDR': 'images/applelogo.png',
        'Mac Pro': 'images/applelogo.png',
        'Mac mini': 'images/applelogo.png',
        'iMac': 'images/applelogo.png',
        'Mac Studio': 'images/applelogo.png'
    }
    
    with app.app_context():
        # 獲取所有產品
        products = Product.query.all()
        
        print(f"找到 {len(products)} 個產品")
        
        updated_count = 0
        
        for product in products:
            # 檢查是否有對應的圖片
            if product.name in product_image_mapping:
                product.image_url = product_image_mapping[product.name]
                updated_count += 1
                print(f"✓ 為產品 '{product.name}' 分配圖片: {product.image_url}")
            else:
                # 如果沒有對應的圖片，使用預設圖片
                product.image_url = 'images/gamepad.png'
                print(f"⚠ 產品 '{product.name}' 沒有對應的圖片，使用預設圖片")
        
        # 提交更改
        try:
            db.session.commit()
            print(f"\n成功更新 {updated_count} 個產品的圖片")
        except Exception as e:
            db.session.rollback()
            print(f"更新失敗: {e}")
        
        # 顯示所有產品的圖片分配情況
        print("\n=== 產品圖片分配情況 ===")
        products = Product.query.all()
        for product in products:
            print(f"{product.name}: {product.image_url}")

if __name__ == '__main__':
    assign_product_images() 