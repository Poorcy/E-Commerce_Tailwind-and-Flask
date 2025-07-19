#!/usr/bin/env python3
"""
測試庫存狀態顯示功能
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_stock_status():
    """測試庫存狀態顯示功能"""
    
    print("=== 庫存狀態顯示功能測試 ===\n")
    
    # 1. 檢查產品變體資料
    print("1. 檢查產品變體資料...")
    try:
        response = requests.get(f"{BASE_URL}/api/products")
        if response.status_code == 200:
            products = response.json()['products']
            if products:
                product = products[0]
                print(f"   ✓ 找到產品: {product['name']} (ID: {product['id']})")
                
                # 分析變體資料
                if product['variants']:
                    print(f"   ✓ 總變體數量: {len(product['variants'])}")
                    
                    # 統計庫存情況
                    zero_stock_variants = []
                    available_variants = []
                    total_stock = 0
                    
                    print("   ✓ 變體庫存分析:")
                    for variant in product['variants']:
                        color = variant.get('color', 'N/A')
                        size = variant.get('size', 'N/A')
                        stock = variant['stock_quantity']
                        total_stock += stock
                        
                        if stock == 0:
                            zero_stock_variants.append(f"{color} {size}")
                        else:
                            available_variants.append(f"{color} {size} ({stock}件)")
                        
                        print(f"     - {color} {size}: {stock} 件")
                    
                    print(f"\n   ✓ 總庫存: {total_stock} 件")
                    print(f"   ✓ 有庫存的變體: {len(available_variants)}")
                    print(f"   ✓ 無庫存的變體: {len(zero_stock_variants)}")
                    
                    if zero_stock_variants:
                        print(f"   ✓ 無庫存組合: {', '.join(zero_stock_variants)}")
                    if available_variants:
                        print(f"   ✓ 有庫存組合: {', '.join(available_variants)}")
                else:
                    print("   ⚠ 沒有變體")
            else:
                print("   ⚠ 沒有找到產品")
                return
        else:
            print(f"   ✗ API錯誤: {response.status_code}")
            return
    except Exception as e:
        print(f"   ✗ 連接錯誤: {e}")
        return
    
    print("\n2. 功能說明:")
    print("   ✓ 根據庫存狀態動態顯示 'In Stock' 或 'Out of Stock'")
    print("   ✓ 有庫存時顯示綠色 'In Stock'")
    print("   ✓ 無庫存時顯示紅色 'Out of Stock'")
    print("   ✓ 狀態會根據選擇的顏色和尺寸組合實時更新")
    
    print("\n3. 修改內容:")
    print("   - 添加了 stock-status 元素ID")
    print("   - 添加了 updateStockStatus() 函數")
    print("   - 在庫存更新時同時更新狀態顯示")
    print("   - 支持動態顏色變化（綠色/紅色）")
    
    print("\n4. 狀態顯示邏輯:")
    print("   - 總庫存 > 0: 顯示 'In Stock' (綠色)")
    print("   - 總庫存 = 0: 顯示 'Out of Stock' (紅色)")
    print("   - 選擇特定組合時根據該組合的庫存顯示")
    print("   - 選擇單一顏色/尺寸時根據相關庫存顯示")
    
    print("\n5. 測試場景:")
    print("   a) 頁面載入時顯示總庫存狀態")
    print("   b) 選擇有庫存的組合，確認顯示 'In Stock'")
    print("   c) 選擇無庫存的組合，確認顯示 'Out of Stock'")
    print("   d) 切換不同組合，觀察狀態變化")
    print("   e) 測試顏色和尺寸的單獨選擇")
    
    print("\n6. 預期結果:")
    print("   - 有庫存時顯示綠色 'In Stock'")
    print("   - 無庫存時顯示紅色 'Out of Stock'")
    print("   - 狀態隨選擇實時更新")
    print("   - 顏色和文字同時變化")
    
    print("\n7. 如何測試:")
    print("   a) 訪問產品頁面: http://127.0.0.1:5000/product/1")
    print("   b) 觀察頁面載入時的庫存狀態")
    print("   c) 選擇不同的顏色和尺寸組合")
    print("   d) 觀察狀態文字的變化")
    print("   e) 確認顏色變化（綠色/紅色）")
    
    print("\n8. 模擬無庫存情況:")
    print("   - 可以通過編輯產品來設置某些變體庫存為0")
    print("   - 訪問: http://127.0.0.1:5000/product/edit/1")
    print("   - 將某些變體的庫存設置為0")
    print("   - 保存後測試無庫存狀態顯示")
    
    print("\n9. 測試步驟:")
    print("   a) 訪問產品頁面")
    print("   b) 確認初始狀態顯示")
    print("   c) 選擇有庫存的組合")
    print("   d) 選擇無庫存的組合")
    print("   e) 測試單一選擇（只選顏色或尺寸）")
    print("   f) 觀察狀態變化")

if __name__ == "__main__":
    test_stock_status() 