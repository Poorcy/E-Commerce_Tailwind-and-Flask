#!/usr/bin/env python3
"""
添加精選商品到資料庫
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def add_featured_products():
    """添加精選商品到資料庫"""
    
    print("=== 添加精選商品到資料庫 ===\n")
    
    # 精選商品列表
    featured_products = [
        {
            "name": "HAVIT HV-G92 Gamepad",
            "description": "高品質遊戲手柄，支援多平台，人體工學設計",
            "price": 120.0,
            "category": "Gaming",
            "image_url": "https://placehold.co/300x200",
            "variants": [
                {"color": "黑色", "size": "標準", "stock_quantity": 50, "sku": "HV-G92-BLK"},
                {"color": "白色", "size": "標準", "stock_quantity": 30, "sku": "HV-G92-WHT"},
                {"color": "紅色", "size": "標準", "stock_quantity": 20, "sku": "HV-G92-RED"}
            ]
        },
        {
            "name": "AK-900 Wired Keyboard",
            "description": "機械鍵盤，RGB背光，可程式化按鍵",
            "price": 960.0,
            "category": "Computer",
            "image_url": "/static/images/keyboard_300_200.png",
            "variants": [
                {"color": "黑色", "size": "標準", "stock_quantity": 25, "sku": "AK-900-BLK"},
                {"color": "白色", "size": "標準", "stock_quantity": 15, "sku": "AK-900-WHT"}
            ]
        },
        {
            "name": "IPS LCD Gaming Monitor",
            "description": "27吋IPS電競螢幕，144Hz刷新率，1ms響應時間",
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
            "description": "人體工學辦公椅，可調節高度和角度",
            "price": 375.0,
            "category": "Furniture",
            "image_url": "https://placehold.co/300x200",
            "variants": [
                {"color": "黑色", "size": "標準", "stock_quantity": 35, "sku": "S-CHAIR-BLK"},
                {"color": "灰色", "size": "標準", "stock_quantity": 25, "sku": "S-CHAIR-GRY"}
            ]
        }
    ]
    
    for product_data in featured_products:
        print(f"添加商品: {product_data['name']}")
        
        # 檢查商品是否已存在
        try:
            response = requests.get(f"{BASE_URL}/api/products")
            if response.status_code == 200:
                existing_products = response.json()['products']
                existing_names = [p['name'] for p in existing_products]
                
                if product_data['name'] in existing_names:
                    print(f"  ✓ 商品已存在，跳過")
                    continue
        except:
            pass
        
        # 添加商品
        try:
            # 這裡需要通過管理介面添加商品
            # 由於沒有直接的API，我們先檢查現有商品
            print(f"  ⚠ 需要通過管理介面手動添加: {product_data['name']}")
            print(f"     價格: ${product_data['price']}")
            print(f"     變體數量: {len(product_data['variants'])}")
            print()
        except Exception as e:
            print(f"  ✗ 添加失敗: {e}")
            print()

if __name__ == "__main__":
    add_featured_products() 