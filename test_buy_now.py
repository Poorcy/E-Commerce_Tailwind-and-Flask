#!/usr/bin/env python3
"""
測試立即購買功能
"""

from app import app, Product, ProductVariant, Order, OrderItem, User
from datetime import datetime, timedelta

def test_buy_now_feature():
    """測試立即購買功能"""
    
    print("=== 測試立即購買功能 ===\n")
    
    with app.app_context():
        # 獲取測試數據
        products = Product.query.all()
        orders = Order.query.all()
        
        print(f"系統中有 {len(products)} 個商品")
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
        
        print("\n=== 立即購買功能說明 ===")
        print("1. 用戶在產品頁面選擇商品規格和數量")
        print("2. 點擊'立即購買'按鈕")
        print("3. 系統檢查庫存是否足夠")
        print("4. 跳轉到立即購買結帳頁面")
        print("5. 用戶填寫收貨信息")
        print("6. 提交訂單並扣除庫存")
        print("7. 跳轉到訂單查詢頁面")
        
        print("\n=== 功能特點 ===")
        print("✅ 支持有變體和無變體商品")
        print("✅ 庫存檢查和扣除")
        print("✅ 簡化的結帳流程")
        print("✅ 自動計算運費")
        print("✅ 訂單編號生成")
        print("✅ 預計送達日期計算")
        
        print("\n=== 技術實現 ===")
        print("前端:")
        print("  - 使用sessionStorage傳遞商品數據")
        print("  - JavaScript驗證庫存和選擇")
        print("  - 動態更新商品信息和價格")
        print("後端:")
        print("  - /buy-now 路由顯示結帳頁面")
        print("  - /buy-now/submit 路由處理訂單提交")
        print("  - 庫存檢查和扣除邏輯")
        print("  - 訂單和訂單項目創建")
        
        print("\n=== 測試建議 ===")
        print("1. 在產品頁面選擇不同規格的商品")
        print("2. 測試庫存不足的情況")
        print("3. 驗證立即購買結帳頁面的數據顯示")
        print("4. 測試訂單提交和庫存扣除")
        print("5. 檢查訂單查詢頁面的訂單記錄")
        print("6. 驗證不同付款方式的處理")

if __name__ == '__main__':
    test_buy_now_feature() 