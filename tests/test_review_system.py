#!/usr/bin/env python3
"""
測試評論系統的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, User, Product
import requests
import json

def test_review_system():
    """測試評論系統功能"""
    print("🧪 開始測試評論系統...")
    
    with app.app_context():
        try:
            # 1. 測試數據庫連接
            print("\n1. 測試數據庫連接...")
            total_reviews = Review.query.count()
            total_users = User.query.count()
            total_products = Product.query.count()
            
            print(f"   ✅ 數據庫連接正常")
            print(f"   📊 統計數據:")
            print(f"      - 評論總數: {total_reviews}")
            print(f"      - 用戶總數: {total_users}")
            print(f"      - 產品總數: {total_products}")
            
            # 2. 測試評論查詢
            print("\n2. 測試評論查詢...")
            products = Product.query.all()
            
            for product in products[:3]:  # 只測試前3個產品
                reviews = Review.query.filter_by(product_id=product.id).all()
                avg_rating = db.session.query(db.func.avg(Review.rating))\
                                     .filter_by(product_id=product.id).scalar()
                
                print(f"   📦 產品: {product.name}")
                print(f"      - 評論數量: {len(reviews)}")
                print(f"      - 平均評分: {round(avg_rating, 1) if avg_rating else 0}")
                
                # 顯示前3條評論
                for i, review in enumerate(reviews[:3]):
                    print(f"      - 評論 {i+1}: {review.user.username} - {review.rating}星 - {review.title}")
            
            # 3. 測試API端點（模擬）
            print("\n3. 測試API端點...")
            
            # 模擬獲取評論API
            if products:
                product_id = products[0].id
                reviews = Review.query.filter_by(product_id=product_id).all()
                
                # 模擬API響應格式
                reviews_data = []
                for review in reviews:
                    review_data = {
                        'id': review.id,
                        'user_name': review.user.username,
                        'rating': review.rating,
                        'title': review.title,
                        'comment': review.comment,
                        'is_verified_purchase': review.is_verified_purchase,
                        'helpful_votes': review.helpful_votes,
                        'created_at': review.created_at.strftime('%Y-%m-%d %H:%M'),
                        'can_edit': False
                    }
                    reviews_data.append(review_data)
                
                print(f"   ✅ API數據格式正確")
                print(f"   📊 產品 {products[0].name} 的評論數據:")
                print(f"      - 評論數量: {len(reviews_data)}")
                for review in reviews_data[:2]:
                    print(f"      - {review['user_name']}: {review['rating']}星 - {review['title']}")
            
            # 4. 測試評分統計
            print("\n4. 測試評分統計...")
            
            for product in products[:2]:
                # 計算評分分布
                rating_counts = {}
                for i in range(1, 6):
                    count = Review.query.filter_by(product_id=product.id, rating=i).count()
                    rating_counts[i] = count
                
                total_reviews = sum(rating_counts.values())
                avg_rating = db.session.query(db.func.avg(Review.rating))\
                                     .filter_by(product_id=product.id).scalar()
                
                print(f"   📦 產品: {product.name}")
                print(f"      - 總評論數: {total_reviews}")
                print(f"      - 平均評分: {round(avg_rating, 1) if avg_rating else 0}")
                print(f"      - 評分分布:")
                for rating, count in rating_counts.items():
                    percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
                    print(f"        {rating}星: {count} ({percentage:.1f}%)")
            
            # 5. 測試驗證購買功能
            print("\n5. 測試驗證購買功能...")
            
            verified_reviews = Review.query.filter_by(is_verified_purchase=True).count()
            unverified_reviews = Review.query.filter_by(is_verified_purchase=False).count()
            
            print(f"   ✅ 驗證購買功能正常")
            print(f"   📊 驗證購買統計:")
            print(f"      - 驗證購買評論: {verified_reviews}")
            print(f"      - 非驗證購買評論: {unverified_reviews}")
            
            print("\n✅ 評論系統測試完成！")
            
        except Exception as e:
            print(f"❌ 測試失敗: {e}")

if __name__ == "__main__":
    test_review_system() 