#!/usr/bin/env python3
"""
創建訂單相關的數據庫表
"""

from app import app, db, Order, OrderItem

def create_orders_tables():
    """創建訂單相關的數據庫表"""
    
    print("=== 創建訂單相關數據庫表 ===\n")
    
    with app.app_context():
        try:
            # 創建訂單表
            print("1. 創建訂單表...")
            db.create_all()
            print("✓ 訂單表創建成功")
            
            # 檢查表是否創建成功
            print("\n2. 檢查表結構...")
            try:
                # 嘗試查詢訂單表
                result = db.session.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='order'"))
                if result.fetchone():
                    print("✓ 訂單表 (order) 存在")
                else:
                    print("⚠️ 訂單表 (order) 不存在")
                
                result = db.session.execute(db.text("SELECT name FROM sqlite_master WHERE type='table' AND name='order_item'"))
                if result.fetchone():
                    print("✓ 訂單項目表 (order_item) 存在")
                else:
                    print("⚠️ 訂單項目表 (order_item) 不存在")
            except Exception as e:
                print(f"⚠️ 檢查表結構時發生錯誤: {e}")
            
            print("\n=== 數據庫表創建完成 ===")
            print("現在可以進行訂單相關操作了！")
            
        except Exception as e:
            print(f"✗ 創建表失敗: {e}")

if __name__ == '__main__':
    create_orders_tables() 