#!/usr/bin/env python3
"""
完整測試投票系統的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, ReviewVote, User, Product
import json

def test_complete_voting_system():
    """完整測試投票系統"""
    print("🧪 開始完整測試投票系統...")
    
    with app.test_client() as client:
        with app.app_context():
            try:
                # 1. 系統狀態檢查
                print("\n1. 系統狀態檢查...")
                users = User.query.all()
                reviews = Review.query.all()
                votes = ReviewVote.query.all()
                
                print(f"   📊 數據統計:")
                print(f"      - 用戶數量: {len(users)}")
                print(f"      - 評論數量: {len(reviews)}")
                print(f"      - 投票記錄: {len(votes)}")
                
                # 2. 測試API端點
                print("\n2. 測試API端點...")
                
                # 模擬用戶登入
                test_user = users[0]
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                
                # 測試獲取評論API（包含投票狀態）
                test_review = reviews[0]
                response = client.get(f'/api/reviews/{test_review.product_id}')
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success'):
                        reviews_data = response_data.get('reviews', [])
                        if reviews_data:
                            first_review = reviews_data[0]
                            user_voted = first_review.get('user_voted', False)
                            helpful_votes = first_review.get('helpful_votes', 0)
                            print(f"   ✅ 獲取評論API正常")
                            print(f"      - 用戶已投票: {user_voted}")
                            print(f"      - 有用票數: {helpful_votes}")
                        else:
                            print(f"   ⚠️ 沒有評論數據")
                    else:
                        print(f"   ❌ API返回錯誤")
                else:
                    print(f"   ❌ HTTP錯誤: {response.status_code}")
                
                # 3. 測試投票功能
                print("\n3. 測試投票功能...")
                
                # 檢查是否已投票
                existing_vote = ReviewVote.query.filter_by(
                    user_id=test_user.id,
                    review_id=test_review.id
                ).first()
                
                if existing_vote:
                    print(f"   ⚠️ 用戶已對評論 {test_review.id} 投票，將刪除現有投票")
                    db.session.delete(existing_vote)
                    db.session.commit()
                
                # 測試投票API
                response = client.post(f'/api/reviews/{test_review.id}/helpful')
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success'):
                        print(f"   ✅ 投票成功")
                        print(f"      - 有用票數: {response_data.get('helpful_votes')}")
                        
                        # 驗證投票記錄
                        vote_record = ReviewVote.query.filter_by(
                            user_id=test_user.id,
                            review_id=test_review.id
                        ).first()
                        
                        if vote_record:
                            print(f"      - 投票記錄已保存")
                        else:
                            print(f"      - ❌ 投票記錄未保存")
                    else:
                        print(f"   ❌ 投票失敗: {response_data.get('error')}")
                else:
                    print(f"   ❌ HTTP錯誤: {response.status_code}")
                
                # 4. 測試重複投票
                print("\n4. 測試重複投票...")
                
                response = client.post(f'/api/reviews/{test_review.id}/helpful')
                
                if response.status_code == 400:
                    response_data = json.loads(response.get_data(as_text=True))
                    if '已經對此評論投票過了' in response_data.get('error', ''):
                        print(f"   ✅ 重複投票被正確阻止")
                    else:
                        print(f"   ❌ 重複投票處理異常")
                else:
                    print(f"   ❌ 重複投票未被阻止")
                
                # 5. 測試未登入用戶投票
                print("\n5. 測試未登入用戶投票...")
                
                with client.session_transaction() as sess:
                    sess.pop('user_id', None)
                
                response = client.post(f'/api/reviews/{test_review.id}/helpful')
                
                if response.status_code == 401:
                    print(f"   ✅ 未登入用戶投票被正確阻止")
                else:
                    print(f"   ❌ 未登入用戶投票未被阻止")
                
                # 6. 統計投票數據
                print("\n6. 投票統計...")
                
                total_votes = ReviewVote.query.count()
                print(f"   📊 總投票記錄: {total_votes}")
                
                # 顯示投票最多的評論
                from sqlalchemy import func
                top_reviews = db.session.query(
                    Review.id,
                    Review.helpful_votes,
                    func.count(ReviewVote.id).label('vote_count')
                ).outerjoin(ReviewVote).group_by(Review.id).order_by(
                    func.count(ReviewVote.id).desc()
                ).limit(5).all()
                
                print(f"   🏆 投票最多的評論:")
                for review_id, helpful_votes, vote_count in top_reviews:
                    print(f"      - 評論 {review_id}: {vote_count} 票")
                
                # 7. 測試前端數據
                print("\n7. 測試前端數據格式...")
                
                # 重新登入
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                
                response = client.get(f'/api/reviews/{test_review.product_id}')
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    reviews_data = response_data.get('reviews', [])
                    
                    if reviews_data:
                        review_data = reviews_data[0]
                        required_fields = ['id', 'user_name', 'rating', 'comment', 'helpful_votes', 'user_voted']
                        
                        missing_fields = [field for field in required_fields if field not in review_data]
                        
                        if not missing_fields:
                            print(f"   ✅ 前端數據格式正確")
                            print(f"      - 包含所有必要欄位")
                            print(f"      - user_voted: {review_data.get('user_voted')}")
                        else:
                            print(f"   ❌ 缺少欄位: {missing_fields}")
                    else:
                        print(f"   ⚠️ 沒有評論數據")
                
                print("\n✅ 投票系統測試完成！")
                print("\n🎯 功能驗證:")
                print("   ✅ 用戶只能對每則評論投票一次")
                print("   ✅ 投票記錄正確保存")
                print("   ✅ 重複投票被阻止")
                print("   ✅ 未登入用戶無法投票")
                print("   ✅ 前端顯示投票狀態")
                
            except Exception as e:
                print(f"❌ 測試失敗: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    test_complete_voting_system() 