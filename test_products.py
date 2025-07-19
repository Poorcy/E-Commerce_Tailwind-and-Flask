#!/usr/bin/env python3
"""
產品資料庫測試腳本
用於測試產品和產品變體的增刪改查功能
"""

from app import app, db, Product, ProductVariant
from datetime import datetime

def test_create_products():
    """測試創建產品和變體"""
    with app.app_context():
        # 清空現有資料
        ProductVariant.query.delete()
        Product.query.delete()
        db.session.commit()
        
        print("=== 測試創建產品 ===")
        
        # 創建第一個產品
        product1 = Product()
        product1.name = "Havic HV G-92 Gamepad"
        product1.description = "PlayStation 5 Controller Skin 高品質貼膜，易於安裝與移除，壓力感應黏著劑，無氣泡殘膠。"
        product1.price = 192.00
        product1.category = "遊戲配件"
        product1.image_url = "https://placehold.co/446x315"
        
        db.session.add(product1)
        db.session.commit()
        print(f"創建產品: {product1.name} (ID: {product1.id})")
        
        # 為第一個產品創建變體
        variants1 = [
            {"color": "黑色", "size": "標準", "stock_quantity": 50},
            {"color": "白色", "size": "標準", "stock_quantity": 30},
            {"color": "紅色", "size": "標準", "stock_quantity": 20},
        ]
        
        for i, variant_data in enumerate(variants1):
            variant = ProductVariant()
            variant.product_id = product1.id
            variant.color = variant_data["color"]
            variant.size = variant_data["size"]
            variant.stock_quantity = variant_data["stock_quantity"]
            variant.sku = f"{product1.id}-{variant_data['color']}-{variant_data['size']}"
            db.session.add(variant)
            print(f"  創建變體: {variant.color} {variant.size} (庫存: {variant.stock_quantity})")
        
        # 創建第二個產品
        product2 = Product()
        product2.name = "AK-900 Wired Keyboard"
        product2.description = "機械式鍵盤，青軸，RGB背光，遊戲專用"
        product2.price = 960.00
        product2.category = "電腦配件"
        product2.image_url = "https://placehold.co/300x200"
        
        db.session.add(product2)
        db.session.commit()
        print(f"創建產品: {product2.name} (ID: {product2.id})")
        
        # 為第二個產品創建變體
        variants2 = [
            {"color": "黑色", "size": "87鍵", "stock_quantity": 25},
            {"color": "黑色", "size": "104鍵", "stock_quantity": 15},
            {"color": "白色", "size": "87鍵", "stock_quantity": 10},
        ]
        
        for i, variant_data in enumerate(variants2):
            variant = ProductVariant()
            variant.product_id = product2.id
            variant.color = variant_data["color"]
            variant.size = variant_data["size"]
            variant.stock_quantity = variant_data["stock_quantity"]
            variant.sku = f"{product2.id}-{variant_data['color']}-{variant_data['size']}"
            db.session.add(variant)
            print(f"  創建變體: {variant.color} {variant.size} (庫存: {variant.stock_quantity})")
        
        db.session.commit()
        print("所有產品和變體創建完成！\n")

def test_query_products():
    """測試查詢產品"""
    with app.app_context():
        print("=== 測試查詢產品 ===")
        
        # 查詢所有產品
        products = Product.query.all()
        print(f"總共有 {len(products)} 個產品:")
        
        for product in products:
            print(f"\n產品: {product.name}")
            print(f"  價格: ${product.price}")
            print(f"  類別: {product.category}")
            print(f"  變體數量: {len(product.variants)}")
            
            for variant in product.variants:
                print(f"    - {variant.color} {variant.size}: 庫存 {variant.stock_quantity}, SKU: {variant.sku}")
        
        print()

def test_stock_management():
    """測試庫存管理"""
    with app.app_context():
        print("=== 測試庫存管理 ===")
        
        # 更新某個變體的庫存
        variant = ProductVariant.query.first()
        if variant:
            old_stock = variant.stock_quantity
            variant.stock_quantity = 0  # 設為缺貨
            db.session.commit()
            print(f"更新庫存: {variant.product.name} - {variant.color} {variant.size}: {old_stock} -> {variant.stock_quantity}")
        
        # 查詢缺貨的變體
        out_of_stock = ProductVariant.query.filter(ProductVariant.stock_quantity == 0).all()
        print(f"缺貨變體數量: {len(out_of_stock)}")
        
        # 查詢庫存充足的變體
        well_stocked = ProductVariant.query.filter(ProductVariant.stock_quantity > 10).all()
        print(f"庫存充足變體數量: {len(well_stocked)}")
        
        print()

def test_price_calculation():
    """測試價格計算"""
    with app.app_context():
        print("=== 測試價格計算 ===")
        
        # 為某個變體添加價格調整
        variant = ProductVariant.query.first()
        if variant:
            variant.price_adjustment = 50.00  # 加價50元
            db.session.commit()
            
            final_price = variant.get_final_price()
            print(f"產品: {variant.product.name}")
            print(f"基本價格: ${variant.product.price}")
            print(f"價格調整: ${variant.price_adjustment}")
            print(f"最終價格: ${final_price}")
        
        print()

if __name__ == "__main__":
    print("開始測試產品資料庫功能...\n")
    
    try:
        test_create_products()
        test_query_products()
        test_stock_management()
        test_price_calculation()
        
        print("所有測試完成！")
        print("\n您可以通過以下方式訪問產品管理介面:")
        print("1. 啟動應用程式: python app.py")
        print("2. 登入後訪問: http://localhost:5000/admin/products")
        print("3. 或者直接訪問產品頁面: http://localhost:5000/product")
        
    except Exception as e:
        print(f"測試過程中發生錯誤: {e}")
        import traceback
        traceback.print_exc() 