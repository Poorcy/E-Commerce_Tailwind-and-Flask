#!/usr/bin/env python3
"""
購物車功能測試腳本
用於測試購物車的增刪改查功能
"""

from app import app, db, User, Product, ProductVariant, CartItem
from datetime import datetime

def test_cart_functionality():
    """測試購物車功能"""
    with app.app_context():
        print("=== 測試購物車功能 ===")
        
        # 清空現有資料
        CartItem.query.delete()
        ProductVariant.query.delete()
        Product.query.delete()
        User.query.delete()
        db.session.commit()
        
        # 創建測試用戶
        user = User()
        user.username = "testuser"
        user.email = "test@example.com"
        user.password = "hashed_password"
        db.session.add(user)
        db.session.commit()
        print(f"創建測試用戶: {user.username}")
        
        # 創建測試產品
        product = Product()
        product.name = "測試產品"
        product.description = "這是一個測試產品"
        product.price = 100.00
        product.category = "測試類別"
        db.session.add(product)
        db.session.commit()
        print(f"創建測試產品: {product.name}")
        
        # 創建產品變體
        variant1 = ProductVariant()
        variant1.product_id = product.id
        variant1.color = "紅色"
        variant1.size = "M"
        variant1.stock_quantity = 10
        variant1.sku = f"{product.id}-紅色-M"
        db.session.add(variant1)
        
        variant2 = ProductVariant()
        variant2.product_id = product.id
        variant2.color = "藍色"
        variant2.size = "L"
        variant2.stock_quantity = 5
        variant2.sku = f"{product.id}-藍色-L"
        db.session.add(variant2)
        
        db.session.commit()
        print(f"創建產品變體: {variant1.color} {variant1.size}, {variant2.color} {variant2.size}")
        
        # 測試加入購物車
        print("\n--- 測試加入購物車 ---")
        
        # 加入基本產品（無變體）
        cart_item1 = CartItem()
        cart_item1.user_id = user.id
        cart_item1.product_id = product.id
        cart_item1.quantity = 2
        db.session.add(cart_item1)
        print(f"加入購物車: {product.name} x2 (無變體)")
        
        # 加入產品變體
        cart_item2 = CartItem()
        cart_item2.user_id = user.id
        cart_item2.product_id = product.id
        cart_item2.variant_id = variant1.id
        cart_item2.quantity = 1
        db.session.add(cart_item2)
        print(f"加入購物車: {product.name} - {variant1.color} {variant1.size} x1")
        
        db.session.commit()
        
        # 查詢購物車
        print("\n--- 查詢購物車 ---")
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        print(f"用戶購物車項目數量: {len(cart_items)}")
        
        for item in cart_items:
            if item.variant:
                print(f"  - {item.product.name} - {item.variant.color} {item.variant.size} x{item.quantity}")
                print(f"    單價: ${item.item_price}, 小計: ${item.total_price}")
            else:
                print(f"  - {item.product.name} x{item.quantity}")
                print(f"    單價: ${item.item_price}, 小計: ${item.total_price}")
        
        # 計算總計
        total = sum(item.total_price for item in cart_items)
        print(f"購物車總計: ${total}")
        
        # 測試更新數量
        print("\n--- 測試更新數量 ---")
        cart_item1.quantity = 3
        db.session.commit()
        print(f"更新數量: {product.name} 從 2 改為 3")
        
        # 測試移除項目
        print("\n--- 測試移除項目 ---")
        db.session.delete(cart_item2)
        db.session.commit()
        print(f"移除項目: {product.name} - {variant1.color} {variant1.size}")
        
        # 查詢更新後的購物車
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        print(f"更新後購物車項目數量: {len(cart_items)}")
        total = sum(item.total_price for item in cart_items)
        print(f"更新後總計: ${total}")
        
        print("\n購物車功能測試完成！")

def test_cart_edge_cases():
    """測試購物車邊界情況"""
    with app.app_context():
        print("\n=== 測試購物車邊界情況 ===")
        
        # 測試重複加入相同產品
        user = User.query.filter_by(username="testuser").first()
        product = Product.query.filter_by(name="測試產品").first()
        
        # 檢查是否已存在相同項目
        existing_item = CartItem.query.filter_by(
            user_id=user.id,
            product_id=product.id,
            variant_id=None
        ).first()
        
        if existing_item:
            print(f"發現重複項目: {existing_item.product.name} x{existing_item.quantity}")
            # 模擬增加數量
            existing_item.quantity += 1
            db.session.commit()
            print(f"更新後數量: x{existing_item.quantity}")
        
        # 測試價格計算
        print("\n--- 測試價格計算 ---")
        cart_items = CartItem.query.filter_by(user_id=user.id).all()
        for item in cart_items:
            print(f"項目: {item.product.name}")
            print(f"  基本價格: ${item.product.price}")
            if item.variant:
                print(f"  變體價格調整: ${item.variant.price_adjustment}")
            print(f"  最終單價: ${item.item_price}")
            print(f"  數量: {item.quantity}")
            print(f"  小計: ${item.total_price}")
        
        print("\n邊界情況測試完成！")

if __name__ == "__main__":
    print("開始測試購物車功能...\n")
    
    try:
        test_cart_functionality()
        test_cart_edge_cases()
        
        print("\n所有測試完成！")
        print("\n您可以通過以下方式測試購物車功能:")
        print("1. 啟動應用程式: python app.py")
        print("2. 註冊/登入帳號")
        print("3. 訪問產品頁面並加入購物車")
        print("4. 查看購物車: http://localhost:5000/cart")
        
    except Exception as e:
        print(f"測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc() 