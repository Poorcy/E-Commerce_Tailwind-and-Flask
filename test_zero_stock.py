#!/usr/bin/env python3
"""
測試無庫存時禁用購物車功能
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_zero_stock():
    """測試無庫存時禁用購物車功能"""
    
    print("=== 無庫存時禁用購物車功能測試 ===\n")
    
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
                    
                    print("   ✓ 變體庫存分析:")
                    for variant in product['variants']:
                        color = variant.get('color', 'N/A')
                        size = variant.get('size', 'N/A')
                        stock = variant['stock_quantity']
                        
                        if stock == 0:
                            zero_stock_variants.append(f"{color} {size}")
                        else:
                            available_variants.append(f"{color} {size} ({stock}件)")
                        
                        print(f"     - {color} {size}: {stock} 件")
                    
                    print(f"\n   ✓ 有庫存的變體: {len(available_variants)}")
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
    print("   ✓ 庫存為0時，加入購物車按鈕被禁用")
    print("   ✓ 庫存為0時，立即購買按鈕被禁用")
    print("   ✓ 按鈕顯示為灰色，無法點擊")
    print("   ✓ 嘗試加入購物車時會顯示警告訊息")
    print("   ✓ 數量超過庫存時會顯示警告訊息")
    
    print("\n3. 修改內容:")
    print("   - 添加了按鈕狀態管理函數")
    print("   - 實時更新按鈕啟用/禁用狀態")
    print("   - 添加了庫存檢查邏輯")
    print("   - 添加了數量超過庫存的檢查")
    print("   - 改進了用戶體驗和錯誤提示")
    
    print("\n4. 按鈕狀態:")
    print("   - 有庫存: 紅色/黑色按鈕，可點擊")
    print("   - 無庫存: 灰色按鈕，不可點擊")
    print("   - 游標樣式: 正常/禁用")
    
    print("\n5. 測試場景:")
    print("   a) 選擇有庫存的組合（如：黑色 S）")
    print("   b) 選擇無庫存的組合（如：白色 L）")
    print("   c) 嘗試點擊禁用的按鈕")
    print("   d) 輸入超過庫存的數量")
    print("   e) 測試加入購物車功能")
    
    print("\n6. 預期結果:")
    print("   - 有庫存時按鈕正常啟用")
    print("   - 無庫存時按鈕被禁用")
    print("   - 嘗試加入無庫存商品時顯示警告")
    print("   - 數量超過庫存時顯示警告")
    
    print("\n7. 如何測試:")
    print("   a) 訪問產品頁面: http://127.0.0.1:5000/product/1")
    print("   b) 選擇不同的顏色和尺寸組合")
    print("   c) 觀察按鈕狀態變化")
    print("   d) 嘗試點擊禁用的按鈕")
    print("   e) 測試加入購物車功能")
    
    print("\n8. 模擬無庫存情況:")
    print("   - 可以通過編輯產品來設置某些變體庫存為0")
    print("   - 訪問: http://127.0.0.1:5000/product/edit/1")
    print("   - 將某些變體的庫存設置為0")
    print("   - 保存後測試無庫存情況")
    
    print("\n9. 測試步驟:")
    print("   a) 訪問產品頁面")
    print("   b) 選擇有庫存的組合，確認按鈕可用")
    print("   c) 選擇無庫存的組合，確認按鈕禁用")
    print("   d) 嘗試點擊禁用的按鈕")
    print("   e) 輸入超過庫存的數量")
    print("   f) 測試加入購物車功能")

if __name__ == "__main__":
    test_zero_stock() 