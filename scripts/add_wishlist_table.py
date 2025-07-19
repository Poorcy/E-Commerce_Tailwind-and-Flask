#!/usr/bin/env python3
"""
添加願望清單表到現有數據庫
"""

from app import app, db
from sqlalchemy import text

def add_wishlist_table():
    """添加願望清單表到現有數據庫"""
    with app.app_context():
        try:
            # 檢查表是否已存在
            result = db.session.execute(text("SELECT name FROM sqlite_master WHERE type='table' AND name='wishlist_item'"))
            if result.fetchone():
                print("WishlistItem 表已存在")
                return
            
            # 創建 WishlistItem 表
            create_table_sql = """
            CREATE TABLE wishlist_item (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER NOT NULL,
                product_id INTEGER NOT NULL,
                created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES user (id),
                FOREIGN KEY (product_id) REFERENCES product (id)
            )
            """
            
            db.session.execute(text(create_table_sql))
            db.session.commit()
            print("已成功創建 WishlistItem 表")
            
        except Exception as e:
            print(f"創建表時發生錯誤: {e}")
            db.session.rollback()

if __name__ == '__main__':
    add_wishlist_table() 