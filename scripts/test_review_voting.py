#!/usr/bin/env python3
"""
測試評論投票功能的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, ReviewVote, User, Product
import json

def test_review_voting():
    """測試評論投票功能"""
    print("🧪 開始測試評論投票功能...")
    
    with app.test_client() as client:
        with app.app_context():
            try:
                # 1. 檢查數據
                users = User.query.all()
                reviews = Review.query.all()
                
                if not users or not reviews:
                    print("❌ 沒有用戶或評論數據")
                    return
                
                user = users[0]
                review = reviews[0]
                
                print(f"👤 測試用戶: {user.username} (ID: {user.id})")
                print(f"📝 測試評論: ID {review.id} - {review.user.username} 的評論")
                print(f"📊 當前有用票數: {review.helpful_votes}")
                
                # 2. 模擬登入
                with client.session_transaction() as sess:
                    sess['user_id'] = user.id
                
                # 3. 檢查是否已投票
                existing_vote = ReviewVote.query.filter_by(
                    user_id=user.id,
                    review_id=review.id
                ).first()
                
                if existing_vote:
                    print(f"⚠️ 用戶已對此評論投票，將刪除現有投票")
                    db.session.delete(existing_vote)
                    db.session.commit()
                
                # 4. 測試投票API
                print("\n📤 測試投票API...")
                
                response = client.post(f'/api/reviews/{review.id}/helpful')
                
                print(f"📊 響應狀態碼: {response.status_code}")
                print(f"📄 響應內容: {response.get_data(as_text=True)}")
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success'):
                        print("✅ 投票成功！")
                        
                        # 驗證投票記錄
                        vote_record = ReviewVote.query.filter_by(
                            user_id=user.id,
                            review_id=review.id
                        ).first()
                        
                        if vote_record:
                            print(f"✅ 投票記錄已保存，ID: {vote_record.id}")
                        else:
                            print("❌ 投票記錄未保存")
                        
                        # 檢查評論票數是否更新
                        updated_review = Review.query.get(review.id)
                        print(f"📊 更新後的有用票數: {updated_review.helpful_votes}")
                        
                    else:
                        print(f"❌ API返回錯誤: {response_data.get('error')}")
                else:
                    print(f"❌ HTTP錯誤: {response.status_code}")
                
                # 5. 測試重複投票
                print("\n🔄 測試重複投票...")
                
                response = client.post(f'/api/reviews/{review.id}/helpful')
                
                print(f"📊 響應狀態碼: {response.status_code}")
                print(f"📄 響應內容: {response.get_data(as_text=True)}")
                
                if response.status_code == 400:
                    response_data = json.loads(response.get_data(as_text=True))
                    if '已經對此評論投票過了' in response_data.get('error', ''):
                        print("✅ 重複投票被正確阻止")
                    else:
                        print(f"❌ 重複投票處理異常: {response_data.get('error')}")
                else:
                    print("❌ 重複投票未被阻止")
                
                # 6. 統計投票數據
                print("\n📊 投票統計:")
                total_votes = ReviewVote.query.count()
                print(f"   - 總投票記錄: {total_votes}")
                
                for user in users[:3]:
                    user_votes = ReviewVote.query.filter_by(user_id=user.id).count()
                    print(f"   - 用戶 {user.username}: {user_votes} 次投票")
                
                print("\n✅ 投票功能測試完成！")
                
            except Exception as e:
                print(f"❌ 測試失敗: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    test_review_voting() 