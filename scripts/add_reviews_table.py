#!/usr/bin/env python3
"""
添加評論表到數據庫的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review

def add_reviews_table():
    """添加評論表到數據庫"""
    with app.app_context():
        try:
            # 創建評論表
            db.create_all()
            print("✅ 評論表已成功添加到數據庫")
            
            # 檢查表是否創建成功
            try:
                # 嘗試查詢評論表
                review_count = Review.query.count()
                print(f"✅ 評論表創建成功，當前有 {review_count} 條評論")
            except Exception as e:
                print(f"❌ 評論表查詢失敗: {e}")
                
        except Exception as e:
            print(f"❌ 創建評論表失敗: {e}")

if __name__ == "__main__":
    add_reviews_table() 