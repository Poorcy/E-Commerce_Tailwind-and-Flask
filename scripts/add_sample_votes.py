#!/usr/bin/env python3
"""
添加示例投票數據的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, ReviewVote, User, Product
from datetime import datetime

def add_sample_votes():
    """添加示例投票數據"""
    with app.app_context():
        try:
            # 獲取用戶和評論
            users = User.query.all()
            reviews = Review.query.all()
            
            if not users or not reviews:
                print("❌ 沒有用戶或評論數據")
                return
            
            print(f"📊 開始添加示例投票...")
            print(f"   - 用戶數量: {len(users)}")
            print(f"   - 評論數量: {len(reviews)}")
            
            # 為每個用戶添加一些投票
            vote_count = 0
            for user in users:
                # 為每個用戶隨機選擇3-5個評論進行投票
                import random
                selected_reviews = random.sample(reviews, min(4, len(reviews)))
                
                for review in selected_reviews:
                    # 檢查是否已經投票過
                    existing_vote = ReviewVote.query.filter_by(
                        user_id=user.id,
                        review_id=review.id
                    ).first()
                    
                    if existing_vote:
                        continue
                    
                    # 創建投票記錄
                    vote = ReviewVote(
                        user_id=user.id,
                        review_id=review.id,
                        is_helpful=True,
                        created_at=datetime.utcnow()
                    )
                    
                    # 更新評論的有用票數
                    review.helpful_votes += 1
                    
                    db.session.add(vote)
                    vote_count += 1
                    
                    print(f"   ✅ 用戶 {user.username} 對評論 {review.id} 投票")
            
            db.session.commit()
            print(f"\n✅ 成功添加 {vote_count} 個投票記錄")
            
            # 統計結果
            total_votes = ReviewVote.query.count()
            print(f"📊 投票統計:")
            print(f"   - 總投票記錄: {total_votes}")
            
            # 顯示每個評論的投票數
            print(f"\n📝 評論投票統計:")
            for review in reviews[:5]:  # 只顯示前5個評論
                votes = ReviewVote.query.filter_by(review_id=review.id).count()
                print(f"   - 評論 {review.id}: {votes} 票")
            
            print(f"\n🎉 示例投票添加完成！")
            
        except Exception as e:
            print(f"❌ 添加示例投票失敗: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_sample_votes() 