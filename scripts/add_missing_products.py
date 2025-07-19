#!/usr/bin/env python3
"""
添加缺少的精選商品到資料庫
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def add_missing_products():
    """添加缺少的精選商品到資料庫"""
    
    print("=== 添加缺少的精選商品到資料庫 ===\n")
    
    # 需要添加的商品列表
    missing_products = [
        {
            "name": "IPS LCD Gaming Monitor",
            "description": "27吋IPS電競螢幕，144Hz刷新率，1ms響應時間，支援FreeSync技術",
            "price": 370.0,
            "category": "Monitor",
            "image_url": "https://placehold.co/300x200",
            "variants": [
                {"color": "黑色", "size": "27吋", "stock_quantity": 40, "sku": "IPS-27-BLK"},
                {"color": "白色", "size": "27吋", "stock_quantity": 20, "sku": "IPS-27-WHT"}
            ]
        },
        {
            "name": "S-Series Comfort Chair",
            "description": "人體工學辦公椅，可調節高度和角度，網狀透氣設計",
            "price": 375.0,
            "category": "Furniture",
            "image_url": "https://placehold.co/300x200",
            "variants": [
                {"color": "黑色", "size": "標準", "stock_quantity": 35, "sku": "S-CHAIR-BLK"},
                {"color": "灰色", "size": "標準", "stock_quantity": 25, "sku": "S-CHAIR-GRY"}
            ]
        }
    ]
    
    print("需要添加的商品:")
    for i, product in enumerate(missing_products, 1):
        print(f"{i}. {product['name']}")
        print(f"   價格: ${product['price']}")
        print(f"   描述: {product['description']}")
        print(f"   變體數量: {len(product['variants'])}")
        print()
    
    print("請通過以下步驟添加商品:")
    print("1. 訪問管理介面: http://127.0.0.1:5000/admin/products")
    print("2. 點擊 '添加新商品'")
    print("3. 填寫商品資訊:")
    
    for product in missing_products:
        print(f"\n商品: {product['name']}")
        print(f"  - 名稱: {product['name']}")
        print(f"  - 描述: {product['description']}")
        print(f"  - 價格: ${product['price']}")
        print(f"  - 分類: {product['category']}")
        print(f"  - 圖片URL: {product['image_url']}")
        print(f"  - 變體:")
        for variant in product['variants']:
            print(f"    * 顏色: {variant['color']}, 尺寸: {variant['size']}, 庫存: {variant['stock_quantity']}, SKU: {variant['sku']}")
    
    print("\n添加完成後，主頁的精選商品連結將能正確導航到對應的商品頁面。")

if __name__ == "__main__":
    add_missing_products() 