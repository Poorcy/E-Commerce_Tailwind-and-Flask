#!/usr/bin/env python3
"""
添加示例評論數據的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, User, Product
from datetime import datetime

def add_sample_reviews():
    """添加示例評論數據"""
    with app.app_context():
        try:
            # 獲取用戶和產品
            users = User.query.all()
            products = Product.query.all()
            
            if not users:
                print("❌ 沒有找到用戶，請先創建用戶")
                return
                
            if not products:
                print("❌ 沒有找到產品，請先創建產品")
                return
            
            # 示例評論數據
            sample_reviews = [
                {
                    'rating': 5,
                    'title': '品質超棒！',
                    'comment': '這個產品品質真的很好，包裝也很精美，完全符合我的期望。強烈推薦！',
                    'is_verified_purchase': True
                },
                {
                    'rating': 4,
                    'title': '性價比不錯',
                    'comment': '整體來說還不錯，價格合理，品質也過得去。會考慮再次購買。',
                    'is_verified_purchase': True
                },
                {
                    'rating': 5,
                    'title': '超出預期',
                    'comment': '比我想像的還要好！做工精細，使用體驗很棒。',
                    'is_verified_purchase': False
                },
                {
                    'rating': 3,
                    'title': '還可以',
                    'comment': '產品本身沒問題，但是配送時間有點長，希望能改進。',
                    'is_verified_purchase': True
                },
                {
                    'rating': 5,
                    'title': '非常滿意',
                    'comment': '第二次購買了，品質一如既往的好，客服也很專業。',
                    'is_verified_purchase': True
                },
                {
                    'rating': 4,
                    'title': '值得推薦',
                    'comment': '產品設計很人性化，使用起來很方便，推薦給朋友們。',
                    'is_verified_purchase': False
                },
                {
                    'rating': 5,
                    'title': '完美體驗',
                    'comment': '從下單到收貨都很順利，產品品質優秀，會繼續支持！',
                    'is_verified_purchase': True
                },
                {
                    'rating': 4,
                    'title': '不錯的選擇',
                    'comment': '性價比很高，適合日常使用，包裝也很環保。',
                    'is_verified_purchase': True
                }
            ]
            
            # 為每個產品添加評論
            for product in products:
                print(f"為產品 '{product.name}' 添加評論...")
                
                for i, review_data in enumerate(sample_reviews):
                    # 輪流使用不同的用戶
                    user = users[i % len(users)]
                    
                    # 檢查是否已經有這個用戶對這個產品的評論
                    existing_review = Review.query.filter_by(
                        user_id=user.id,
                        product_id=product.id
                    ).first()
                    
                    if existing_review:
                        print(f"  跳過用戶 {user.username} 的評論（已存在）")
                        continue
                    
                    # 創建新評論
                    review = Review(
                        user_id=user.id,
                        product_id=product.id,
                        rating=review_data['rating'],
                        title=review_data['title'],
                        comment=review_data['comment'],
                        is_verified_purchase=review_data['is_verified_purchase'],
                        helpful_votes=0,
                        created_at=datetime.utcnow()
                    )
                    
                    db.session.add(review)
                    print(f"  添加評論: {user.username} - {review_data['rating']}星")
                
                db.session.commit()
                print(f"✅ 產品 '{product.name}' 的評論添加完成")
            
            # 統計
            total_reviews = Review.query.count()
            print(f"\n✅ 示例評論添加完成！總共有 {total_reviews} 條評論")
            
        except Exception as e:
            print(f"❌ 添加示例評論失敗: {e}")
            db.session.rollback()

if __name__ == "__main__":
    add_sample_reviews() 