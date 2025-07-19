#!/usr/bin/env python3
"""
產品資料調試腳本
用於查看產品和變體的詳細資料
"""

from app import app, db, Product, ProductVariant

def debug_products():
    """調試產品資料"""
    with app.app_context():
        print("=== 產品資料調試 ===")
        
        # 查詢所有產品
        products = Product.query.all()
        print(f"總共有 {len(products)} 個產品:")
        
        for product in products:
            print(f"\n產品 ID: {product.id}")
            print(f"名稱: {product.name}")
            print(f"價格: ${product.price}")
            print(f"描述: {product.description}")
            print(f"變體數量: {len(product.variants)}")
            
            if product.variants:
                print("變體詳情:")
                for variant in product.variants:
                    print(f"  - 變體 ID: {variant.id}")
                    print(f"    顏色: {variant.color}")
                    print(f"    尺寸: {variant.size}")
                    print(f"    庫存: {variant.stock_quantity}")
                    print(f"    SKU: {variant.sku}")
                    print(f"    價格調整: ${variant.price_adjustment}")
                    print(f"    最終價格: ${variant.get_final_price()}")
                    print()
            else:
                print("  無變體")
        
        # 測試第一個產品
        first_product = Product.query.first()
        if first_product:
            print(f"\n=== 第一個產品詳情 ===")
            print(f"ID: {first_product.id}")
            print(f"名稱: {first_product.name}")
            print(f"變體數量: {len(first_product.variants)}")
            
            # 檢查變體的顏色和尺寸
            colors = [v.color for v in first_product.variants if v.color]
            sizes = [v.size for v in first_product.variants if v.size]
            
            print(f"可用顏色: {colors}")
            print(f"可用尺寸: {sizes}")
            
            # 測試模板條件
            print(f"\n=== 模板條件測試 ===")
            print(f"product 存在: {first_product is not None}")
            print(f"product.variants 存在: {hasattr(first_product, 'variants')}")
            print(f"variants 數量: {len(first_product.variants) if first_product.variants else 0}")
            
            if first_product.variants:
                print("變體檢查:")
                for i, variant in enumerate(first_product.variants):
                    print(f"  變體 {i+1}:")
                    print(f"    有顏色: {variant.color is not None}")
                    print(f"    有尺寸: {variant.size is not None}")
                    print(f"    顏色值: '{variant.color}'")
                    print(f"    尺寸值: '{variant.size}'")

if __name__ == "__main__":
    debug_products() 