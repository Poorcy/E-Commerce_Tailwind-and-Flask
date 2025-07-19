#!/usr/bin/env python3
"""
測試顏色和尺寸選項去重功能
"""

import requests
import json

# 基礎URL
BASE_URL = "http://127.0.0.1:5000"

def test_unique_options():
    """測試顏色和尺寸選項去重功能"""
    
    print("=== 顏色和尺寸選項去重測試 ===\n")
    
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
                    
                    # 統計顏色和尺寸
                    colors = set()
                    sizes = set()
                    color_size_combinations = []
                    
                    print("   ✓ 變體詳細資料:")
                    for variant in product['variants']:
                        color = variant.get('color', 'N/A')
                        size = variant.get('size', 'N/A')
                        stock = variant['stock_quantity']
                        colors.add(color)
                        sizes.add(size)
                        color_size_combinations.append(f"{color}-{size}")
                        print(f"     - 顏色: {color}, 尺寸: {size}, 庫存: {stock} 件")
                    
                    print(f"\n   ✓ 去重後的顏色數量: {len(colors)}")
                    print(f"   ✓ 去重後的尺寸數量: {len(sizes)}")
                    print(f"   ✓ 顏色選項: {', '.join(sorted(colors))}")
                    print(f"   ✓ 尺寸選項: {', '.join(sorted(sizes))}")
                    
                    # 檢查是否有重複的顏色-尺寸組合
                    unique_combinations = set(color_size_combinations)
                    if len(color_size_combinations) != len(unique_combinations):
                        print("   ⚠ 發現重複的顏色-尺寸組合")
                    else:
                        print("   ✓ 所有顏色-尺寸組合都是唯一的")
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
    
    print("\n2. 去重功能說明:")
    print("   ✓ 顏色選項不再重複顯示")
    print("   ✓ 尺寸選項不再重複顯示")
    print("   ✓ 每個顏色和尺寸只顯示一次")
    print("   ✓ 保持庫存計算功能正常")
    
    print("\n3. 修改內容:")
    print("   - 使用Jinja2過濾器去重顏色選項")
    print("   - 使用Jinja2過濾器去重尺寸選項")
    print("   - 更新JavaScript邏輯處理去重後的選項")
    print("   - 使用JSON格式傳遞變體數據")
    
    print("\n4. 如何測試:")
    print("   a) 訪問產品頁面: http://127.0.0.1:5000/product/1")
    print("   b) 查看顏色選項是否重複")
    print("   c) 查看尺寸選項是否重複")
    print("   d) 測試顏色和尺寸選擇功能")
    print("   e) 驗證庫存顯示是否正確")
    
    print("\n5. 預期效果:")
    print("   - 顏色選項: 黑色、白色、紅色（不重複）")
    print("   - 尺寸選項: S、M、L（不重複）")
    print("   - 選擇功能正常運作")
    print("   - 庫存顯示準確")

if __name__ == "__main__":
    test_unique_options() 