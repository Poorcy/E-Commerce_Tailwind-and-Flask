#!/usr/bin/env python3
"""
測試JSON序列化問題修復
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_json_fix():
    """測試JSON序列化問題修復"""
    
    print("=== JSON序列化問題修復測試 ===\n")
    
    # 1. 測試產品API
    print("1. 測試產品API...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            products = response.json()['products']
            if products:
                product = products[0]
                print(f"   ✓ 產品API正常: {product['name']}")
                print(f"   ✓ 變體數量: {len(product['variants'])}")
            else:
                print("   ⚠ 沒有產品")
                return
        else:
            print(f"   ✗ API錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ 連接錯誤: {e}")
        return
    
    # 2. 測試變體API
    print("\n2. 測試變體API...")
    try:
        product_id = products[0]['id']
        response = requests.get(f"{BASE_URL}/api/products/{product_id}/variants")
        if response.status_code == 200:
            variants = response.json()['variants']
            print(f"   ✓ 變體API正常: {len(variants)} 個變體")
            
            # 檢查變體數據結構
            if variants:
                variant = variants[0]
                required_fields = ['id', 'color', 'size', 'stock_quantity']
                missing_fields = [field for field in required_fields if field not in variant]
                
                if missing_fields:
                    print(f"   ⚠ 缺少字段: {missing_fields}")
                else:
                    print("   ✓ 變體數據結構完整")
                    print(f"   ✓ 示例變體: ID={variant['id']}, 顏色={variant['color']}, 尺寸={variant['size']}, 庫存={variant['stock_quantity']}")
            else:
                print("   ⚠ 沒有變體數據")
        else:
            print(f"   ✗ 變體API錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ 變體API錯誤: {e}")
        return
    
    print("\n3. 修復說明:")
    print("   ✓ 創建了新的API端點: /api/products/<id>/variants")
    print("   ✓ 將SQLAlchemy對象轉換為字典格式")
    print("   ✓ 使用AJAX動態加載變體數據")
    print("   ✓ 避免了模板中的JSON序列化問題")
    
    print("\n4. 技術改進:")
    print("   - 分離了數據獲取和顯示邏輯")
    print("   - 使用RESTful API設計")
    print("   - 支持異步數據加載")
    print("   - 更好的錯誤處理")
    
    print("\n5. 如何測試:")
    print("   a) 訪問產品頁面: http://127.0.0.1:5000/product/1")
    print("   b) 檢查瀏覽器控制台是否有錯誤")
    print("   c) 驗證顏色和尺寸選項正常顯示")
    print("   d) 測試庫存顯示功能")
    
    print("\n6. 預期結果:")
    print("   - 不再出現JSON序列化錯誤")
    print("   - 變體數據正確加載")
    print("   - 顏色和尺寸選項去重正常")
    print("   - 庫存顯示功能正常")

if __name__ == "__main__":
    test_json_fix() 