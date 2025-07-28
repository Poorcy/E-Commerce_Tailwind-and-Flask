#!/usr/bin/env python3
"""
添加評論投票表到數據庫的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, ReviewVote

def add_review_votes_table():
    """添加評論投票表到數據庫"""
    with app.app_context():
        try:
            # 創建投票表
            db.create_all()
            print("✅ 評論投票表已成功添加到數據庫")
            
            # 檢查表是否創建成功
            try:
                # 嘗試查詢投票表
                vote_count = ReviewVote.query.count()
                print(f"✅ 投票表創建成功，當前有 {vote_count} 條投票記錄")
            except Exception as e:
                print(f"❌ 投票表查詢失敗: {e}")
                
        except Exception as e:
            print(f"❌ 創建投票表失敗: {e}")

if __name__ == "__main__":
    add_review_votes_table() 