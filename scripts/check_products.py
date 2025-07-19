#!/usr/bin/env python3
"""
查看數據庫中的產品數據
"""

from app import app, Product

def check_products():
    """查看所有產品數據"""
    with app.app_context():
        products = Product.query.all()
        
        print("=== 數據庫中的產品數據 ===")
        print(f"總共有 {len(products)} 個產品\n")
        
        for i, product in enumerate(products, 1):
            print(f"產品 {i}:")
            print(f"  ID: {product.id}")
            print(f"  名稱: {product.name}")
            print(f"  描述: {product.description}")
            print(f"  價格: ${product.price}")
            print(f"  分類: {product.category}")
            print(f"  圖片: {product.image_url}")
            print(f"  啟用狀態: {product.is_active}")
            print("-" * 50)

if __name__ == '__main__':
    check_products() 