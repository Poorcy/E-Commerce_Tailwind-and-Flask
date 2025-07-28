#!/usr/bin/env python3
"""
演示投票收回功能的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, ReviewVote, User, Product

def demo_vote_toggle():
    """演示投票收回功能"""
    print("🎬 投票收回功能演示")
    print("=" * 50)
    
    with app.app_context():
        try:
            # 1. 顯示當前投票統計
            print("\n📊 當前投票統計:")
            total_votes = ReviewVote.query.count()
            total_reviews = Review.query.count()
            total_users = User.query.count()
            
            print(f"   - 總投票記錄: {total_votes}")
            print(f"   - 總評論數量: {total_reviews}")
            print(f"   - 總用戶數量: {total_users}")
            
            # 2. 顯示投票最多的評論
            from sqlalchemy import func
            top_reviews = db.session.query(
                Review.id,
                Review.helpful_votes,
                func.count(ReviewVote.id).label('vote_count')
            ).outerjoin(ReviewVote).group_by(Review.id).order_by(
                func.count(ReviewVote.id).desc()
            ).limit(5).all()
            
            print(f"\n🏆 投票最多的評論:")
            for review_id, helpful_votes, vote_count in top_reviews:
                print(f"   - 評論 {review_id}: {vote_count} 票 (有用票數: {helpful_votes})")
            
            # 3. 顯示用戶投票統計
            print(f"\n👥 用戶投票統計:")
            user_votes = db.session.query(
                User.username,
                func.count(ReviewVote.id).label('vote_count')
            ).outerjoin(ReviewVote).group_by(User.id).order_by(
                func.count(ReviewVote.id).desc()
            ).limit(5).all()
            
            for username, vote_count in user_votes:
                print(f"   - {username}: {vote_count} 次投票")
            
            # 4. 功能說明
            print(f"\n🎯 投票收回功能說明:")
            print(f"   1. 用戶可以對評論點擊'有用'進行投票")
            print(f"   2. 已投票的評論會顯示藍色和 ✓ 標記")
            print(f"   3. 再次點擊可以收回投票")
            print(f"   4. 收回後可以重新投票")
            print(f"   5. 投票記錄會正確更新")
            
            # 5. API端點說明
            print(f"\n🔗 API端點:")
            print(f"   - POST /api/reviews/<review_id>/helpful")
            print(f"   - 功能: 投票或收回投票")
            print(f"   - 響應: {{'success': true, 'voted': true/false, 'helpful_votes': number}}")
            
            # 6. 前端功能說明
            print(f"\n💻 前端功能:")
            print(f"   - 投票按鈕會根據投票狀態改變樣式")
            print(f"   - 已投票: 藍色 + ✓ 標記")
            print(f"   - 未投票: 灰色 + hover效果")
            print(f"   - 點擊後會顯示相應的提示訊息")
            
            # 7. 數據庫設計
            print(f"\n🗄️ 數據庫設計:")
            print(f"   - ReviewVote 表記錄投票")
            print(f"   - 複合唯一索引防止重複投票")
            print(f"   - 支持投票和收回操作")
            
            print(f"\n✅ 演示完成！")
            print(f"\n💡 使用提示:")
            print(f"   1. 訪問產品頁面查看評論")
            print(f"   2. 登入後可以對評論投票")
            print(f"   3. 再次點擊可以收回投票")
            print(f"   4. 觀察投票數量和按鈕樣式的變化")
            
        except Exception as e:
            print(f"❌ 演示失敗: {e}")

if __name__ == "__main__":
    demo_vote_toggle() 