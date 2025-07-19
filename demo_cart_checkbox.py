#!/usr/bin/env python3
"""
演示購物車勾選功能
"""

from app import app, CartItem, Product, ProductVariant

def demo_cart_checkbox():
    """演示購物車勾選功能"""
    
    print("=== 購物車勾選功能演示 ===\n")
    
    with app.app_context():
        # 獲取購物車數據
        cart_items = CartItem.query.all()
        
        if cart_items:
            print(f"購物車中有 {len(cart_items)} 個商品:")
            for i, item in enumerate(cart_items, 1):
                variant_info = ""
                if item.variant:
                    if item.variant.color:
                        variant_info += f"顏色: {item.variant.color}"
                    if item.variant.size:
                        variant_info += f", 尺寸: {item.variant.size}"
                
                print(f"  {i}. {item.product.name}")
                print(f"     價格: ${item.item_price}")
                print(f"     數量: {item.quantity}")
                print(f"     小計: ${item.total_price}")
                if variant_info:
                    print(f"     變體: {variant_info}")
                print()
            
            print("=== 功能說明 ===")
            print("1. 每個商品前都有勾選框，用戶可以選擇要結帳的商品")
            print("2. 表頭有全選/取消全選功能，方便批量操作")
            print("3. 勾選商品後，右側總計會動態更新")
            print("4. 只有選中商品時，結帳按鈕才會變為可用狀態")
            print("5. 結帳頁面只會顯示選中的商品")
            print()
            
            print("=== 使用步驟 ===")
            print("1. 訪問購物車頁面: http://127.0.0.1:5000/cart")
            print("2. 觀察每個商品前的勾選框")
            print("3. 點擊勾選框選擇要結帳的商品")
            print("4. 觀察右側總計的動態更新")
            print("5. 確認結帳按鈕的狀態變化")
            print("6. 點擊結帳按鈕進入結帳頁面")
            print("7. 確認結帳頁面只顯示選中的商品")
            print()
            
            print("=== 技術實現 ===")
            print("- 前端JavaScript處理勾選狀態和動態計算")
            print("- 使用sessionStorage傳遞選中商品ID")
            print("- 後端API提供選中商品的詳細信息")
            print("- 結帳頁面動態載入選中商品")
            print("- 響應式設計，支持移動端操作")
            
        else:
            print("購物車是空的")
            print("請先添加商品到購物車來測試勾選功能")

if __name__ == '__main__':
    demo_cart_checkbox() 