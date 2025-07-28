#!/usr/bin/env python3
"""
診斷評論刪除失敗問題的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, ReviewVote, User, Product
import json

def debug_review_deletion():
    """診斷評論刪除失敗問題"""
    print("🔍 開始診斷評論刪除失敗問題...")
    
    with app.test_client() as client:
        with app.app_context():
            try:
                # 1. 檢查數據庫狀態
                print("\n1. 檢查數據庫狀態...")
                users = User.query.all()
                reviews = Review.query.all()
                votes = ReviewVote.query.all()
                
                print(f"   📊 數據統計:")
                print(f"      - 用戶數量: {len(users)}")
                print(f"      - 評論數量: {len(reviews)}")
                print(f"      - 投票記錄: {len(votes)}")
                
                if not users or not reviews:
                    print("   ❌ 沒有用戶或評論數據")
                    return
                
                # 2. 檢查評論和投票的關聯
                print("\n2. 檢查評論和投票關聯...")
                
                for review in reviews[:3]:  # 檢查前3個評論
                    vote_count = ReviewVote.query.filter_by(review_id=review.id).count()
                    print(f"   - 評論 {review.id}: {vote_count} 個投票")
                    
                    # 檢查是否有外鍵約束問題
                    try:
                        review.user.username
                        review.product.name
                        print(f"      ✅ 關聯正常")
                    except Exception as e:
                        print(f"      ❌ 關聯錯誤: {e}")
                
                # 3. 測試刪除評論API
                print("\n3. 測試刪除評論API...")
                
                test_user = users[0]
                test_review = reviews[0]
                
                print(f"   👤 測試用戶: {test_user.username} (ID: {test_user.id})")
                print(f"   📝 測試評論: ID {test_review.id} - {test_review.user.username} 的評論")
                
                # 模擬用戶登入
                with client.session_transaction() as sess:
                    sess['user_id'] = test_user.id
                
                # 檢查權限
                if test_review.user_id == test_user.id:
                    print(f"   ✅ 用戶有權限刪除此評論")
                else:
                    print(f"   ❌ 用戶無權限刪除此評論")
                    print(f"      - 評論用戶ID: {test_review.user_id}")
                    print(f"      - 當前用戶ID: {test_user.id}")
                
                # 測試刪除API
                response = client.delete(f'/api/reviews/{test_review.id}')
                
                print(f"   📊 響應狀態碼: {response.status_code}")
                print(f"   📄 響應內容: {response.get_data(as_text=True)}")
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success'):
                        print(f"   ✅ 刪除成功")
                        
                        # 驗證評論是否真的被刪除
                        deleted_review = Review.query.get(test_review.id)
                        if not deleted_review:
                            print(f"   ✅ 評論已從數據庫刪除")
                        else:
                            print(f"   ❌ 評論仍在數據庫中")
                        
                        # 檢查相關的投票是否也被刪除
                        related_votes = ReviewVote.query.filter_by(review_id=test_review.id).count()
                        print(f"   📊 相關投票記錄: {related_votes}")
                        
                    else:
                        print(f"   ❌ API返回錯誤: {response_data.get('error')}")
                elif response.status_code == 401:
                    print(f"   ❌ 未登入")
                elif response.status_code == 403:
                    print(f"   ❌ 無權限")
                elif response.status_code == 404:
                    print(f"   ❌ 評論不存在")
                else:
                    print(f"   ❌ HTTP錯誤: {response.status_code}")
                
                # 4. 測試外鍵約束
                print("\n4. 測試外鍵約束...")
                
                # 檢查ReviewVote表的外鍵約束
                try:
                    # 嘗試刪除一個有投票的評論
                    review_with_votes = None
                    for review in reviews:
                        vote_count = ReviewVote.query.filter_by(review_id=review.id).count()
                        if vote_count > 0:
                            review_with_votes = review
                            break
                    
                    if review_with_votes:
                        print(f"   📝 找到有投票的評論: ID {review_with_votes.id}")
                        print(f"   📊 投票數量: {ReviewVote.query.filter_by(review_id=review_with_votes.id).count()}")
                        
                        # 檢查外鍵約束設置
                        print(f"   🔗 檢查外鍵約束...")
                        
                        # 嘗試刪除評論（這可能會因為外鍵約束失敗）
                        try:
                            db.session.delete(review_with_votes)
                            db.session.commit()
                            print(f"   ✅ 刪除成功（外鍵約束正常）")
                        except Exception as e:
                            print(f"   ❌ 刪除失敗（外鍵約束問題）: {e}")
                            db.session.rollback()
                    else:
                        print(f"   ⚠️ 沒有找到有投票的評論")
                        
                except Exception as e:
                    print(f"   ❌ 外鍵約束測試失敗: {e}")
                
                # 5. 檢查數據庫配置
                print("\n5. 檢查數據庫配置...")
                
                try:
                    # 檢查ReviewVote表的外鍵約束
                    from sqlalchemy import inspect
                    inspector = inspect(db.engine)
                    
                    foreign_keys = inspector.get_foreign_keys('review_vote')
                    print(f"   🔗 ReviewVote表外鍵約束:")
                    for fk in foreign_keys:
                        print(f"      - {fk}")
                        
                except Exception as e:
                    print(f"   ❌ 無法檢查外鍵約束: {e}")
                
                # 6. 建議解決方案
                print("\n6. 建議解決方案:")
                print(f"   🔧 如果外鍵約束導致刪除失敗:")
                print(f"      1. 先刪除相關的投票記錄")
                print(f"      2. 再刪除評論記錄")
                print(f"   🔧 如果權限問題:")
                print(f"      1. 檢查用戶登入狀態")
                print(f"      2. 確認評論歸屬權")
                print(f"   🔧 如果數據庫問題:")
                print(f"      1. 檢查數據庫連接")
                print(f"      2. 檢查表結構")
                
                print(f"\n✅ 診斷完成！")
                
            except Exception as e:
                print(f"❌ 診斷失敗: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    debug_review_deletion() 