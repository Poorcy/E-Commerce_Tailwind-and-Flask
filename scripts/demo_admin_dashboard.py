#!/usr/bin/env python3
"""
管理儀表板演示腳本
這個腳本會創建一些測試數據來展示管理儀表板的功能
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, User, Product, Order, ProductVariant
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

def create_demo_data():
    """創建演示數據"""
    with app.app_context():
        print("正在創建演示數據...")
        
        # 創建測試用戶
        admin_user = User(
            username='admin',
            email='admin@exclusive.com',
            password=generate_password_hash('admin123'),
            first_name='管理員',
            last_name='測試',
            created_at=datetime.now() - timedelta(days=30)
        )
        db.session.add(admin_user)
        
        # 創建一些測試用戶
        for i in range(1, 6):
            user = User(
                username=f'user{i}',
                email=f'user{i}@example.com',
                password=generate_password_hash('password123'),
                first_name=f'用戶{i}',
                last_name='測試',
                created_at=datetime.now() - timedelta(days=i*5)
            )
            db.session.add(user)
        
        # 創建一些測試產品
        products_data = [
            {
                'name': 'iPhone 15 Pro',
                'description': '最新款 iPhone，搭載 A17 Pro 晶片',
                'price': 35900.0,
                'category': '手機',
                'image_url': '/static/images/applelogo.png'
            },
            {
                'name': 'MacBook Pro 14"',
                'description': '專業級筆電，搭載 M3 晶片',
                'price': 59900.0,
                'category': '筆電',
                'image_url': '/static/images/applelogo.png'
            },
            {
                'name': 'iPad Air',
                'description': '輕薄平板，搭載 M2 晶片',
                'price': 19900.0,
                'category': '平板',
                'image_url': '/static/images/applelogo.png'
            },
            {
                'name': 'Apple Watch Series 9',
                'description': '智能手錶，健康監測',
                'price': 12900.0,
                'category': '穿戴裝置',
                'image_url': '/static/images/applelogo.png'
            },
            {
                'name': 'AirPods Pro',
                'description': '主動降噪耳機',
                'price': 7490.0,
                'category': '音訊',
                'image_url': '/static/images/applelogo.png'
            }
        ]
        
        products = []
        for i, data in enumerate(products_data):
            product = Product(
                name=data['name'],
                description=data['description'],
                price=data['price'],
                category=data['category'],
                image_url=data['image_url'],
                created_at=datetime.now() - timedelta(days=i*3)
            )
            db.session.add(product)
            products.append(product)
        
        db.session.commit()
        
        # 為每個產品創建變體
        for product in products:
            # 正常庫存的變體
            variant1 = ProductVariant(
                product_id=product.id,
                color='太空灰',
                size='標準',
                stock_quantity=50,
                sku=f"{product.id}-SG-STD"
            )
            db.session.add(variant1)
            
            # 低庫存的變體（用於測試警告）
            variant2 = ProductVariant(
                product_id=product.id,
                color='銀色',
                size='大',
                stock_quantity=3,  # 低庫存
                sku=f"{product.id}-SL-LG"
            )
            db.session.add(variant2)
        
        # 創建一些測試訂單
        order_statuses = ['pending', 'processing', 'shipped', 'delivered']
        customers = ['張小明', '李小華', '王小美', '陳小強', '林小芳']
        
        for i in range(1, 11):
            # 隨機選擇產品和變體
            product = products[i % len(products)]
            variant = ProductVariant.query.filter_by(product_id=product.id).first()
            
            # 隨機訂單狀態
            status = order_statuses[i % len(order_statuses)]
            
            # 隨機客戶
            customer = customers[i % len(customers)]
            
            # 計算訂單金額
            quantity = (i % 3) + 1
            total_amount = product.price * quantity
            
            order = Order(
                user_id=admin_user.id,
                order_number=f'ORD-{i:03d}',
                status=status,
                total_amount=total_amount,
                shipping_fee=0.0,
                recipient_name=customer,
                recipient_phone=f'09{i:08d}',
                recipient_address=f'台北市信義區{i}號',
                payment_method='credit_card',
                estimated_delivery=datetime.now() + timedelta(days=7),
                created_at=datetime.now() - timedelta(days=i*2)
            )
            db.session.add(order)
        
        db.session.commit()
        
        print("✅ 演示數據創建完成！")
        print("\n📊 管理儀表板數據統計：")
        print(f"   - 總用戶數: {User.query.count()}")
        print(f"   - 總產品數: {Product.query.count()}")
        print(f"   - 總訂單數: {Order.query.count()}")
        print(f"   - 總銷售額: ${db.session.query(db.func.sum(Order.total_amount)).scalar():.2f}")
        print(f"   - 低庫存產品: {ProductVariant.query.filter(ProductVariant.stock_quantity < 5).count()}")
        
        print("\n🔑 登入資訊：")
        print("   網址: http://localhost:5000/login")
        print("   帳號: admin")
        print("   密碼: admin123")
        
        print("\n📋 管理儀表板：")
        print("   網址: http://localhost:5000/admin/dashboard")
        print("   (需要先登入)")

if __name__ == '__main__':
    try:
        create_demo_data()
    except Exception as e:
        print(f"❌ 創建演示數據時發生錯誤: {e}")
        print("請確保資料庫已初始化且應用程式可以正常運行") 