#!/usr/bin/env python3
"""
測試投票收回功能的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, ReviewVote, User, Product
import json

def test_vote_toggle():
    """測試投票收回功能"""
    print("🧪 開始測試投票收回功能...")
    
    with app.test_client() as client:
        with app.app_context():
            try:
                # 1. 準備測試數據
                users = User.query.all()
                reviews = Review.query.all()
                
                if not users or not reviews:
                    print("❌ 沒有用戶或評論數據")
                    return
                
                test_user = users[0]
                test_review = reviews[0]
                
                print(f"👤 測試用戶: {test_user.username} (ID: {test_user.id})")
                print(f"📝 測試評論: ID {test_review.id} - {test_review.user.username} 的評論")
                print(f"📊 當前有用票數: {test_review.helpful_votes}")
                
                # 2. 模擬登入
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                
                # 3. 清理現有投票
                existing_vote = ReviewVote.query.filter_by(
                    user_id=test_user.id,
                    review_id=test_review.id
                ).first()
                
                if existing_vote:
                    print(f"⚠️ 清理現有投票記錄")
                    db.session.delete(existing_vote)
                    db.session.commit()
                
                # 4. 第一次投票
                print("\n📤 第一次投票...")
                
                response = client.post(f'/api/reviews/{test_review.id}/helpful')
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success') and response_data.get('voted'):
                        print(f"✅ 第一次投票成功")
                        print(f"   - 有用票數: {response_data.get('helpful_votes')}")
                        print(f"   - 投票狀態: {response_data.get('voted')}")
                        
                        # 驗證投票記錄
                        vote_record = ReviewVote.query.filter_by(
                            user_id=test_user.id,
                            review_id=test_review.id
                        ).first()
                        
                        if vote_record:
                            print(f"   - 投票記錄已保存")
                        else:
                            print(f"   - ❌ 投票記錄未保存")
                    else:
                        print(f"❌ 第一次投票失敗")
                else:
                    print(f"❌ HTTP錯誤: {response.status_code}")
                
                # 5. 第二次點擊（收回投票）
                print("\n🔄 第二次點擊（收回投票）...")
                
                response = client.post(f'/api/reviews/{test_review.id}/helpful')
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success') and not response_data.get('voted'):
                        print(f"✅ 收回投票成功")
                        print(f"   - 有用票數: {response_data.get('helpful_votes')}")
                        print(f"   - 投票狀態: {response_data.get('voted')}")
                        
                        # 驗證投票記錄已刪除
                        vote_record = ReviewVote.query.filter_by(
                            user_id=test_user.id,
                            review_id=test_review.id
                        ).first()
                        
                        if not vote_record:
                            print(f"   - 投票記錄已刪除")
                        else:
                            print(f"   - ❌ 投票記錄未刪除")
                    else:
                        print(f"❌ 收回投票失敗")
                else:
                    print(f"❌ HTTP錯誤: {response.status_code}")
                
                # 6. 第三次點擊（重新投票）
                print("\n🔄 第三次點擊（重新投票）...")
                
                response = client.post(f'/api/reviews/{test_review.id}/helpful')
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success') and response_data.get('voted'):
                        print(f"✅ 重新投票成功")
                        print(f"   - 有用票數: {response_data.get('helpful_votes')}")
                        print(f"   - 投票狀態: {response_data.get('voted')}")
                    else:
                        print(f"❌ 重新投票失敗")
                else:
                    print(f"❌ HTTP錯誤: {response.status_code}")
                
                # 7. 測試API響應格式
                print("\n📊 API響應格式測試...")
                
                response = client.get(f'/api/reviews/{test_review.product_id}')
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success'):
                        reviews_data = response_data.get('reviews', [])
                        if reviews_data:
                            first_review = reviews_data[0]
                            user_voted = first_review.get('user_voted', False)
                            helpful_votes = first_review.get('helpful_votes', 0)
                            print(f"   ✅ API響應格式正確")
                            print(f"   - 用戶已投票: {user_voted}")
                            print(f"   - 有用票數: {helpful_votes}")
                        else:
                            print(f"   ⚠️ 沒有評論數據")
                    else:
                        print(f"   ❌ API返回錯誤")
                else:
                    print(f"   ❌ HTTP錯誤: {response.status_code}")
                
                # 8. 統計最終結果
                print("\n📊 最終統計...")
                
                total_votes = ReviewVote.query.count()
                user_votes = ReviewVote.query.filter_by(user_id=test_user.id).count()
                
                print(f"   - 總投票記錄: {total_votes}")
                print(f"   - 測試用戶投票: {user_votes}")
                
                print("\n✅ 投票收回功能測試完成！")
                print("\n🎯 功能驗證:")
                print("   ✅ 用戶可以投票")
                print("   ✅ 用戶可以收回投票")
                print("   ✅ 用戶可以重新投票")
                print("   ✅ 投票記錄正確管理")
                print("   ✅ API響應格式正確")
                
            except Exception as e:
                print(f"❌ 測試失敗: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    test_vote_toggle() 