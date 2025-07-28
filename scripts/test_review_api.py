#!/usr/bin/env python3
"""
直接測試評論API的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, User, Product
import requests
import json

def test_review_api():
    """直接測試評論API"""
    print("🧪 開始測試評論API...")
    
    with app.test_client() as client:
        with app.app_context():
            try:
                # 1. 檢查用戶和產品
                users = User.query.all()
                products = Product.query.all()
                
                if not users or not products:
                    print("❌ 沒有用戶或產品數據")
                    return
                
                user = users[0]
                product = products[0]
                
                print(f"👤 測試用戶: {user.username} (ID: {user.id})")
                print(f"🛍️ 測試產品: {product.name} (ID: {product.id})")
                
                # 2. 模擬登入
                with client.session_transaction() as sess:
                    sess['user_id'] = user.id
                
                # 3. 檢查是否已評論過
                existing_review = Review.query.filter_by(
                    user_id=user.id,
                    product_id=product.id
                ).first()
                
                if existing_review:
                    print(f"⚠️ 用戶已評論過此產品，將刪除現有評論")
                    db.session.delete(existing_review)
                    db.session.commit()
                
                # 4. 測試添加評論API
                print("\n📤 測試添加評論API...")
                
                review_data = {
                    'product_id': product.id,
                    'rating': 5,
                    'title': 'API測試評論',
                    'comment': '這是一個通過API測試的評論'
                }
                
                print(f"📝 提交數據: {json.dumps(review_data, ensure_ascii=False, indent=2)}")
                
                response = client.post('/api/reviews/add',
                                    json=review_data,
                                    content_type='application/json')
                
                print(f"📊 響應狀態碼: {response.status_code}")
                print(f"📄 響應內容: {response.get_data(as_text=True)}")
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success'):
                        print("✅ 評論添加成功！")
                        
                        # 驗證評論是否真的保存了
                        new_review = Review.query.filter_by(
                            user_id=user.id,
                            product_id=product.id
                        ).first()
                        
                        if new_review:
                            print(f"✅ 數據庫驗證成功，評論ID: {new_review.id}")
                        else:
                            print("❌ 數據庫驗證失敗，評論未保存")
                    else:
                        print(f"❌ API返回錯誤: {response_data.get('error')}")
                else:
                    print(f"❌ HTTP錯誤: {response.status_code}")
                
                # 5. 測試獲取評論API
                print("\n📥 測試獲取評論API...")
                
                response = client.get(f'/api/reviews/{product.id}')
                
                print(f"📊 響應狀態碼: {response.status_code}")
                print(f"📄 響應內容: {response.get_data(as_text=True)}")
                
                if response.status_code == 200:
                    response_data = json.loads(response.get_data(as_text=True))
                    if response_data.get('success'):
                        reviews = response_data.get('reviews', [])
                        summary = response_data.get('summary', {})
                        print(f"✅ 成功獲取 {len(reviews)} 條評論")
                        print(f"📊 平均評分: {summary.get('average_rating', 0)}")
                        print(f"📊 總評論數: {summary.get('total_reviews', 0)}")
                    else:
                        print(f"❌ API返回錯誤: {response_data.get('error')}")
                else:
                    print(f"❌ HTTP錯誤: {response.status_code}")
                
                print("\n✅ API測試完成！")
                
            except Exception as e:
                print(f"❌ 測試失敗: {e}")
                import traceback
                traceback.print_exc()

if __name__ == "__main__":
    test_review_api() 