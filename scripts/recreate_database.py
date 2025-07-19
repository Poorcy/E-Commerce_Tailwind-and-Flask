#!/usr/bin/env python3
"""
重新創建數據庫腳本
這個腳本會刪除現有的數據庫並重新創建，包含新的 WishlistItem 表
"""

import os
from app import app, db, User, Product, ProductVariant, CartItem, WishlistItem
from werkzeug.security import generate_password_hash

def recreate_database():
    """重新創建數據庫"""
    with app.app_context():
        # 刪除現有數據庫文件
        db_file = 'instance/site.db'
        if os.path.exists(db_file):
            os.remove(db_file)
            print(f"已刪除現有數據庫: {db_file}")
        
        # 創建所有表
        db.create_all()
        print("已創建新的數據庫表")
        
        # 創建測試用戶
        test_user = User(
            username='testuser',
            email='test@example.com',
            password=generate_password_hash('password123'),
            first_name='Test',
            last_name='User'
        )
        db.session.add(test_user)
        
        # 創建測試產品
        products_data = [
            {
                'name': 'HAVIT HV-G92 Gamepad',
                'description': '高品質遊戲手柄，支援多平台遊戲',
                'price': 120.00,
                'category': 'Gaming',
                'image_url': 'images/gamepad_red.png'
            },
            {
                'name': 'AK-900 Wired Keyboard',
                'description': '機械鍵盤，提供出色的打字體驗',
                'price': 960.00,
                'category': 'Computer',
                'image_url': 'images/keyboard_300_200.png'
            },
            {
                'name': 'IPS LCD Gaming Monitor',
                'description': '27吋IPS螢幕，144Hz刷新率',
                'price': 370.00,
                'category': 'Monitor',
                'image_url': 'images/gamepad.png'
            },
            {
                'name': 'S-Series Comfort Chair',
                'description': '人體工學辦公椅，提供舒適坐姿',
                'price': 375.00,
                'category': 'Furniture',
                'image_url': 'images/gamepad.png'
            }
        ]
        
        for product_data in products_data:
            product = Product(**product_data)
            db.session.add(product)
            db.session.flush()  # 獲取產品ID
            
            # 為每個產品創建變體
            variants_data = [
                {'color': 'Red', 'size': 'M', 'stock_quantity': 10},
                {'color': 'Blue', 'size': 'L', 'stock_quantity': 15},
                {'color': 'Black', 'size': 'S', 'stock_quantity': 5}
            ]
            
            for variant_data in variants_data:
                variant = ProductVariant(
                    product_id=product.id,
                    **variant_data,
                    sku=f"{product.id}-{variant_data['color']}-{variant_data['size']}"
                )
                db.session.add(variant)
        
        # 提交所有更改
        db.session.commit()
        print("已添加測試數據")
        print(f"創建了 {len(products_data)} 個產品")
        print("測試用戶: testuser / password123")

if __name__ == '__main__':
    recreate_database() 