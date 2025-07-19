#!/usr/bin/env python3
"""
測試庫存扣除功能
"""

from app import app, Product, ProductVariant, CartItem, Order, OrderItem, User
from datetime import datetime, timedelta

def test_stock_deduction():
    """測試庫存扣除功能"""
    
    print("=== 測試庫存扣除功能 ===\n")
    
    with app.app_context():
        # 獲取測試數據
        products = Product.query.all()
        cart_items = CartItem.query.all()
        orders = Order.query.all()
        
        print(f"系統中有 {len(products)} 個商品")
        print(f"購物車中有 {len(cart_items)} 個商品")
        print(f"系統中有 {len(orders)} 個訂單")
        
        if products:
            print("\n=== 商品庫存狀況 ===")
            for i, product in enumerate(products, 1):
                print(f"\n商品 {i}: {product.name}")
                if product.variants:
                    for variant in product.variants:
                        print(f"  - 變體: 顏色={variant.color}, 尺寸={variant.size}, 庫存={variant.stock_quantity}")
                else:
                    print(f"  - 無變體")
        
        if cart_items:
            print("\n=== 購物車商品 ===")
            for i, item in enumerate(cart_items, 1):
                variant_info = ""
                if item.variant:
                    variant_info = f" (顏色: {item.variant.color}, 尺寸: {item.variant.size})"
                print(f"  {i}. {item.product.name}{variant_info} x{item.quantity}")
        
        if orders:
            print("\n=== 訂單詳情 ===")
            for i, order in enumerate(orders, 1):
                print(f"\n訂單 {i}: {order.order_number}")
                print(f"  狀態: {order.status}")
                print(f"  總金額: ${order.total_amount}")
                print(f"  創建時間: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                if order.items:
                    print("  商品:")
                    for item in order.items:
                        variant_info = ""
                        if item.variant_info:
                            variant_info = f" ({item.variant_info})"
                        print(f"    - {item.product_name}{variant_info} x{item.quantity} (${item.subtotal})")
        
        print("\n=== 功能說明 ===")
        print("1. 用戶在購物車中修改商品數量時會檢查庫存")
        print("2. 結帳時會再次檢查庫存是否足夠")
        print("3. 訂單提交成功後會自動扣除相應的庫存數量")
        print("4. 庫存不足時會顯示詳細的錯誤信息")
        print("5. 支持有變體和無變體商品的庫存管理")
        
        print("\n=== 庫存扣除邏輯 ===")
        print("有變體的商品:")
        print("  - 檢查特定變體的庫存")
        print("  - 扣除該變體的庫存數量")
        print("無變體的商品:")
        print("  - 檢查所有變體的總庫存")
        print("  - 從有庫存的變體開始扣除")
        print("  - 按順序扣除直到滿足需求")
        
        print("\n=== 測試建議 ===")
        print("1. 在購物車中嘗試修改商品數量超過庫存")
        print("2. 結帳時檢查庫存不足的錯誤提示")
        print("3. 成功結帳後檢查庫存是否正確扣除")
        print("4. 驗證訂單查詢頁面顯示正確的訂單信息")

if __name__ == '__main__':
    test_stock_deduction() 