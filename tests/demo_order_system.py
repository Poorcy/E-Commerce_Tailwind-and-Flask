#!/usr/bin/env python3
"""
演示訂單系統功能
"""

from app import app, Order, OrderItem, User, CartItem, Product, ProductVariant
from datetime import datetime, timedelta

def demo_order_system():
    """演示訂單系統功能"""
    
    print("=== 訂單系統功能演示 ===\n")
    
    with app.app_context():
        # 獲取用戶和訂單數據
        users = User.query.all()
        orders = Order.query.all()
        
        print(f"系統中有 {len(users)} 個用戶")
        print(f"系統中有 {len(orders)} 個訂單")
        
        if orders:
            print("\n=== 訂單列表 ===")
            for i, order in enumerate(orders, 1):
                print(f"\n訂單 {i}:")
                print(f"  訂單編號: {order.order_number}")
                print(f"  狀態: {order.status}")
                print(f"  總金額: ${order.total_amount}")
                print(f"  收件人: {order.recipient_name}")
                print(f"  預計抵達: {order.estimated_delivery.strftime('%Y-%m-%d')}")
                print(f"  創建時間: {order.created_at.strftime('%Y-%m-%d %H:%M:%S')}")
                
                if order.items:
                    print("  商品:")
                    for item in order.items:
                        print(f"    - {item.product_name} x{item.quantity} (${item.subtotal})")
                        if item.variant_info:
                            print(f"      變體: {item.variant_info}")
        
        # 檢查購物車數據
        cart_items = CartItem.query.all()
        print(f"\n購物車中有 {len(cart_items)} 個商品")
        
        print("\n=== 功能說明 ===")
        print("1. 用戶可以在購物車中選擇要結帳的商品")
        print("2. 結帳時需要填寫收件人信息")
        print("3. 訂單提交後會自動生成訂單編號")
        print("4. 預計抵達日期自動設為結帳後7天")
        print("5. 已結帳的商品會從購物車中移除")
        print("6. 用戶可以在訂單查詢頁面查看所有訂單")
        print("7. 訂單包含完整的商品信息和收件信息")
        
        print("\n=== 使用流程 ===")
        print("1. 用戶登入後訪問購物車頁面")
        print("2. 勾選要結帳的商品")
        print("3. 點擊結帳按鈕進入結帳頁面")
        print("4. 填寫收件人姓名、電話、地址")
        print("5. 選擇付款方式")
        print("6. 點擊送出訂單")
        print("7. 系統自動創建訂單並跳轉到訂單查詢頁面")
        print("8. 在訂單查詢頁面可以查看訂單詳情和預計抵達日期")
        
        print("\n=== 技術實現 ===")
        print("- 使用SQLAlchemy ORM管理數據庫")
        print("- 訂單和訂單項目分別存儲在不同表中")
        print("- 訂單編號自動生成，格式為ORD+時間戳+隨機字符")
        print("- 商品信息在訂單項目中快照保存")
        print("- 支持多種訂單狀態管理")
        print("- 響應式設計，支持移動端查看")
        print("- 完整的錯誤處理和用戶提示")
        
        print("\n=== 數據庫結構 ===")
        print("Order表:")
        print("  - id: 主鍵")
        print("  - user_id: 用戶ID")
        print("  - order_number: 訂單編號")
        print("  - status: 訂單狀態")
        print("  - total_amount: 總金額")
        print("  - shipping_fee: 運費")
        print("  - recipient_name: 收件人姓名")
        print("  - recipient_phone: 收件人電話")
        print("  - recipient_address: 收件地址")
        print("  - payment_method: 付款方式")
        print("  - estimated_delivery: 預計抵達日期")
        print("  - created_at: 創建時間")
        
        print("\nOrderItem表:")
        print("  - id: 主鍵")
        print("  - order_id: 訂單ID")
        print("  - product_id: 商品ID")
        print("  - variant_id: 變體ID")
        print("  - product_name: 商品名稱（快照）")
        print("  - variant_info: 變體信息（快照）")
        print("  - price: 單價（快照）")
        print("  - quantity: 數量")
        print("  - subtotal: 小計")

if __name__ == '__main__':
    demo_order_system() 