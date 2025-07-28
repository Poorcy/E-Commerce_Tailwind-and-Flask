#!/usr/bin/env python3
"""
測試前端評論功能的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, User, Product

def test_review_frontend():
    """測試前端評論功能"""
    print("🧪 開始測試前端評論功能...")
    
    with app.app_context():
        try:
            # 1. 檢查數據
            users = User.query.all()
            products = Product.query.all()
            
            print(f"📊 數據統計:")
            print(f"   - 用戶數量: {len(users)}")
            print(f"   - 產品數量: {len(products)}")
            print(f"   - 評論數量: {Review.query.count()}")
            
            # 2. 檢查每個產品的評論
            print(f"\n📝 產品評論統計:")
            for product in products:
                reviews = Review.query.filter_by(product_id=product.id).all()
                avg_rating = db.session.query(db.func.avg(Review.rating))\
                                     .filter_by(product_id=product.id).scalar()
                
                print(f"   🛍️ {product.name}:")
                print(f"      - 評論數量: {len(reviews)}")
                print(f"      - 平均評分: {round(avg_rating, 1) if avg_rating else 0}")
                
                # 顯示最近的評論
                if reviews:
                    latest_review = reviews[0]
                    print(f"      - 最新評論: {latest_review.user.username} - {latest_review.rating}星")
            
            # 3. 檢查用戶評論情況
            print(f"\n👤 用戶評論統計:")
            for user in users[:3]:  # 只顯示前3個用戶
                user_reviews = Review.query.filter_by(user_id=user.id).all()
                print(f"   👤 {user.username}: {len(user_reviews)} 條評論")
                
                for review in user_reviews[:2]:  # 只顯示前2條評論
                    print(f"      - {review.product.name}: {review.rating}星 - {review.title}")
            
            # 4. 提供測試建議
            print(f"\n💡 測試建議:")
            print(f"   1. 訪問 http://localhost:5000/product/1 查看產品頁面")
            print(f"   2. 登入後點擊 '寫評論' 按鈕")
            print(f"   3. 選擇評分並填寫評論內容")
            print(f"   4. 提交評論並檢查是否成功")
            
            # 5. 檢查可能的問題
            print(f"\n🔍 潛在問題檢查:")
            
            # 檢查是否有用戶未評論的產品
            for user in users[:2]:
                for product in products[:2]:
                    existing_review = Review.query.filter_by(
                        user_id=user.id,
                        product_id=product.id
                    ).first()
                    
                    if existing_review:
                        print(f"   ⚠️ 用戶 {user.username} 已評論過 {product.name}")
                    else:
                        print(f"   ✅ 用戶 {user.username} 可以評論 {product.name}")
            
            print(f"\n✅ 前端測試準備完成！")
            print(f"🎯 現在可以訪問網站測試評論功能了")
            
        except Exception as e:
            print(f"❌ 測試失敗: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_review_frontend() 