#!/usr/bin/env python3
"""
添加主頁所有商品到資料庫
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def add_all_products():
    """添加主頁所有商品到資料庫"""
    
    print("=== 添加主頁所有商品到資料庫 ===\n")
    
    # 主頁所有商品列表
    all_products = [
        # 精選商品
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
        },
        
        # Best Selling Products
        {
            "name": "The north coat",
            "description": "北面經典外套，防水透氣，適合戶外活動",
            "price": 260.0,
            "category": "Clothing",
            "image_url": "https://placehold.co/140x146",
            "variants": [
                {"color": "黑色", "size": "M", "stock_quantity": 30, "sku": "NORTH-COAT-BLK-M"},
                {"color": "藍色", "size": "L", "stock_quantity": 25, "sku": "NORTH-COAT-BLU-L"},
                {"color": "紅色", "size": "S", "stock_quantity": 20, "sku": "NORTH-COAT-RED-S"}
            ]
        },
        {
            "name": "Gucci duffle bag",
            "description": "Gucci經典帆布包，時尚設計，實用容量",
            "price": 960.0,
            "category": "Bag",
            "image_url": "https://placehold.co/178x129",
            "variants": [
                {"color": "棕色", "size": "標準", "stock_quantity": 15, "sku": "GUCCI-BAG-BRN"},
                {"color": "黑色", "size": "標準", "stock_quantity": 20, "sku": "GUCCI-BAG-BLK"}
            ]
        },
        {
            "name": "RGB liquid CPU Cooler",
            "description": "RGB水冷散熱器，高效散熱，炫彩燈效",
            "price": 160.0,
            "category": "Computer",
            "image_url": "https://placehold.co/191x95",
            "variants": [
                {"color": "黑色", "size": "240mm", "stock_quantity": 40, "sku": "RGB-COOLER-240"},
                {"color": "白色", "size": "360mm", "stock_quantity": 30, "sku": "RGB-COOLER-360"}
            ]
        },
        {
            "name": "Small BookSelf",
            "description": "小型書架，實木製作，簡約設計",
            "price": 360.0,
            "category": "Furniture",
            "image_url": "https://placehold.co/140x176",
            "variants": [
                {"color": "原木色", "size": "3層", "stock_quantity": 25, "sku": "BOOKSHELF-3"},
                {"color": "深棕色", "size": "5層", "stock_quantity": 20, "sku": "BOOKSHELF-5"}
            ]
        },
        
        # Explore Our Products
        {
            "name": "Breed Dry Dog Food",
            "description": "優質狗糧，營養均衡，適合各種犬種",
            "price": 100.0,
            "category": "Pet",
            "image_url": "https://placehold.co/115x180",
            "variants": [
                {"color": "標準", "size": "5kg", "stock_quantity": 50, "sku": "DOG-FOOD-5KG"},
                {"color": "標準", "size": "10kg", "stock_quantity": 30, "sku": "DOG-FOOD-10KG"}
            ]
        },
        {
            "name": "CANON EOS DSLR Camera",
            "description": "佳能EOS數位單眼相機，高畫質拍攝，專業級別",
            "price": 360.0,
            "category": "Camera",
            "image_url": "https://placehold.co/146x163",
            "variants": [
                {"color": "黑色", "size": "標準", "stock_quantity": 20, "sku": "CANON-EOS-BLK"},
                {"color": "銀色", "size": "標準", "stock_quantity": 15, "sku": "CANON-EOS-SLV"}
            ]
        },
        {
            "name": "ASUS FHD Gaming Laptop",
            "description": "華碩電競筆電，FHD螢幕，高效能處理器",
            "price": 700.0,
            "category": "Computer",
            "image_url": "https://placehold.co/172x180",
            "variants": [
                {"color": "黑色", "size": "15.6吋", "stock_quantity": 25, "sku": "ASUS-LAPTOP-15"},
                {"color": "黑色", "size": "17.3吋", "stock_quantity": 20, "sku": "ASUS-LAPTOP-17"}
            ]
        },
        {
            "name": "Curology Product Set",
            "description": "Curology護膚套組，個人化配方，改善膚質",
            "price": 500.0,
            "category": "Beauty",
            "image_url": "https://placehold.co/172x159",
            "variants": [
                {"color": "標準", "size": "基礎套組", "stock_quantity": 30, "sku": "CUROLOGY-BASIC"},
                {"color": "標準", "size": "進階套組", "stock_quantity": 25, "sku": "CUROLOGY-ADV"}
            ]
        },
        {
            "name": "Kids Electric Car",
            "description": "兒童電動車，安全設計，適合3-8歲兒童",
            "price": 960.0,
            "category": "Toy",
            "image_url": "https://placehold.co/180x133",
            "variants": [
                {"color": "紅色", "size": "標準", "stock_quantity": 15, "sku": "KIDS-CAR-RED"},
                {"color": "藍色", "size": "標準", "stock_quantity": 12, "sku": "KIDS-CAR-BLU"}
            ]
        },
        {
            "name": "Jr. Zoom Soccer Cleats",
            "description": "青少年足球鞋，輕量化設計，專業級別",
            "price": 1160.0,
            "category": "Sports",
            "image_url": "https://placehold.co/186x164",
            "variants": [
                {"color": "黑色", "size": "US 7", "stock_quantity": 20, "sku": "SOCCER-CLEATS-7"},
                {"color": "白色", "size": "US 8", "stock_quantity": 18, "sku": "SOCCER-CLEATS-8"}
            ]
        },
        {
            "name": "GP11 Shooter USB Gamepad",
            "description": "GP11射擊遊戲手柄，USB連接，精準控制",
            "price": 660.0,
            "category": "Gaming",
            "image_url": "https://placehold.co/178x150",
            "variants": [
                {"color": "黑色", "size": "標準", "stock_quantity": 30, "sku": "GP11-BLK"},
                {"color": "白色", "size": "標準", "stock_quantity": 25, "sku": "GP11-WHT"}
            ]
        },
        {
            "name": "Quilted Satin Jacket",
            "description": "緞面夾克，菱格紋設計，時尚優雅",
            "price": 660.0,
            "category": "Clothing",
            "image_url": "https://placehold.co/182x176",
            "variants": [
                {"color": "黑色", "size": "M", "stock_quantity": 20, "sku": "SATIN-JACKET-BLK-M"},
                {"color": "深藍色", "size": "L", "stock_quantity": 15, "sku": "SATIN-JACKET-BLU-L"}
            ]
        }
    ]
    
    print(f"需要添加的商品總數: {len(all_products)}")
    print("\n商品分類:")
    
    categories = {}
    for product in all_products:
        category = product['category']
        if category not in categories:
            categories[category] = []
        categories[category].append(product['name'])
    
    for category, products in categories.items():
        print(f"  {category}: {len(products)} 個商品")
        for product_name in products:
            print(f"    - {product_name}")
        print()
    
    print("請通過以下步驟添加商品:")
    print("1. 訪問管理介面: http://127.0.0.1:5000/admin/products")
    print("2. 點擊 '添加新商品'")
    print("3. 按照以下資訊填寫商品:")
    
    for i, product in enumerate(all_products, 1):
        print(f"\n{i}. 商品: {product['name']}")
        print(f"   - 名稱: {product['name']}")
        print(f"   - 描述: {product['description']}")
        print(f"   - 價格: ${product['price']}")
        print(f"   - 分類: {product['category']}")
        print(f"   - 圖片URL: {product['image_url']}")
        print(f"   - 變體:")
        for variant in product['variants']:
            print(f"     * 顏色: {variant['color']}, 尺寸: {variant['size']}, 庫存: {variant['stock_quantity']}, SKU: {variant['sku']}")
    
    print(f"\n添加完成後，主頁的所有商品連結將能正確導航到對應的商品頁面。")
    print(f"如果商品不存在，會顯示404錯誤頁面。")

if __name__ == "__main__":
    add_all_products() 