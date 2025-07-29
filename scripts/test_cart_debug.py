#!/usr/bin/env python3
"""
調試購物車和結帳功能的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, User, Product, CartItem, ProductVariant, db
from werkzeug.security import generate_password_hash

def debug_cart_system():
    """調試購物車系統"""
    print("🔧 開始調試購物車系統...")
    
    with app.app_context():
        # 1. 檢查用戶
        print("\n1. 檢查用戶...")
        users = User.query.all()
        print(f"   總用戶數: {len(users)}")
        for user in users:
            print(f"   - {user.username} (ID: {user.id})")
        
        # 2. 檢查產品
        print("\n2. 檢查產品...")
        products = Product.query.all()
        print(f"   總產品數: {len(products)}")
        for product in products[:5]:  # 只顯示前5個
            print(f"   - {product.name} (ID: {product.id})")
        
        # 3. 檢查產品變體
        print("\n3. 檢查產品變體...")
        variants = ProductVariant.query.all()
        print(f"   總變體數: {len(variants)}")
        for variant in variants[:5]:  # 只顯示前5個
            print(f"   - 產品ID: {variant.product_id}, 顏色: {variant.color}, 尺寸: {variant.size}")
        
        # 4. 檢查購物車項目
        print("\n4. 檢查購物車項目...")
        cart_items = CartItem.query.all()
        print(f"   總購物車項目數: {len(cart_items)}")
        for item in cart_items:
            print(f"   - 用戶ID: {item.user_id}, 產品ID: {item.product_id}, 變體ID: {item.variant_id}, 數量: {item.quantity}")
        
        # 5. 測試購物車查詢
        print("\n5. 測試購物車查詢...")
        if cart_items:
            test_item_ids = [item.id for item in cart_items[:2]]  # 取前2個項目
            print(f"   測試項目ID: {test_item_ids}")
            
            # 測試查詢
            test_items = CartItem.query.filter(CartItem.id.in_(test_item_ids)).all()
            print(f"   查詢結果: {len(test_items)} 個項目")
            
            for item in test_items:
                try:
                    print(f"   - 項目ID: {item.id}")
                    print(f"     用戶: {item.user.username if item.user else 'None'}")
                    print(f"     產品: {item.product.name if item.product else 'None'}")
                    print(f"     變體: {item.variant.color if item.variant else 'None'}")
                    print(f"     數量: {item.quantity}")
                    print(f"     價格: {item.item_price}")
                except Exception as e:
                    print(f"     處理項目時出錯: {e}")
        else:
            print("   沒有購物車項目可以測試")
        
        # 6. 創建測試數據（如果需要）
        print("\n6. 創建測試數據...")
        
        # 檢查是否有測試用戶
        test_user = User.query.filter_by(username='testuser').first()
        if not test_user:
            print("   創建測試用戶...")
            test_user = User()
            test_user.username = 'testuser'
            test_user.email = 'test@example.com'
            test_user.password = generate_password_hash('testpass')
            test_user.first_name = 'Test'
            test_user.last_name = 'User'
            db.session.add(test_user)
            db.session.commit()
            print("   ✓ 測試用戶創建成功")
        else:
            print("   ✓ 測試用戶已存在")
        
        # 檢查是否有產品
        if not products:
            print("   沒有產品，無法創建購物車項目")
            return
        
        # 創建測試購物車項目
        test_cart_item = CartItem.query.filter_by(user_id=test_user.id).first()
        if not test_cart_item:
            print("   創建測試購物車項目...")
            first_product = products[0]
            first_variant = ProductVariant.query.filter_by(product_id=first_product.id).first()
            
            test_cart_item = CartItem()
            test_cart_item.user_id = test_user.id
            test_cart_item.product_id = first_product.id
            test_cart_item.variant_id = first_variant.id if first_variant else None
            test_cart_item.quantity = 1
            
            db.session.add(test_cart_item)
            db.session.commit()
            print("   ✓ 測試購物車項目創建成功")
        else:
            print("   ✓ 測試購物車項目已存在")
        
        print(f"\n✅ 購物車系統調試完成！")
        print(f"   測試用戶: testuser / testpass")
        print(f"   測試購物車項目ID: {test_cart_item.id if test_cart_item else 'None'}")

if __name__ == "__main__":
    try:
        debug_cart_system()
    except Exception as e:
        print(f"❌ 調試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc() 