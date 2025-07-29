#!/usr/bin/env python3
"""
為測試用戶創建購物車項目
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, User, Product, CartItem, ProductVariant, db

def create_cart_items():
    """為測試用戶創建購物車項目"""
    print("🔧 為測試用戶創建購物車項目...")
    
    with app.app_context():
        # 查找測試用戶
        user = User.query.filter_by(email='simple@test.com').first()
        if not user:
            print("❌ 找不到測試用戶 simple@test.com")
            return False
        
        print(f"✅ 找到用戶: {user.username} (ID: {user.id})")
        
        # 查找產品
        products = Product.query.all()
        if not products:
            print("❌ 沒有找到產品")
            return False
        
        print(f"✅ 找到 {len(products)} 個產品")
        
        # 檢查用戶是否已有購物車項目
        existing_items = CartItem.query.filter_by(user_id=user.id).all()
        if existing_items:
            print(f"用戶已有 {len(existing_items)} 個購物車項目")
            for item in existing_items:
                print(f"  - 產品: {item.product.name}, 數量: {item.quantity}")
            return True
        
        # 為用戶創建購物車項目
        print("創建購物車項目...")
        
        for i, product in enumerate(products[:2]):  # 只為前2個產品創建項目
            # 查找產品的變體
            variants = ProductVariant.query.filter_by(product_id=product.id).all()
            
            if variants:
                variant = variants[0]  # 使用第一個變體
                print(f"  為產品 {product.name} 創建項目，使用變體: {variant.color}")
            else:
                variant = None
                print(f"  為產品 {product.name} 創建項目（無變體）")
            
            cart_item = CartItem()
            cart_item.user_id = user.id
            cart_item.product_id = product.id
            cart_item.variant_id = variant.id if variant else None
            cart_item.quantity = i + 1  # 數量 1, 2
            
            db.session.add(cart_item)
        
        try:
            db.session.commit()
            print("✅ 購物車項目創建成功")
            
            # 顯示創建的項目
            new_items = CartItem.query.filter_by(user_id=user.id).all()
            print(f"用戶現在有 {len(new_items)} 個購物車項目:")
            for item in new_items:
                variant_info = f" ({item.variant.color})" if item.variant else ""
                print(f"  - {item.product.name}{variant_info}: 數量 {item.quantity}, ID: {item.id}")
            
            return True
            
        except Exception as e:
            print(f"❌ 創建購物車項目失敗: {e}")
            db.session.rollback()
            return False

if __name__ == "__main__":
    try:
        create_cart_items()
    except Exception as e:
        print(f"❌ 執行過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc() 