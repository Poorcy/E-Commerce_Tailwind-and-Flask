#!/usr/bin/env python3
"""
診斷評論提交失敗的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, User, Product
import requests
import json

def debug_review_submission():
    """診斷評論提交問題"""
    print("🔍 開始診斷評論提交問題...")
    
    with app.app_context():
        try:
            # 1. 檢查數據庫連接
            print("\n1. 檢查數據庫連接...")
            try:
                total_reviews = Review.query.count()
                print(f"   ✅ 數據庫連接正常，當前有 {total_reviews} 條評論")
            except Exception as e:
                print(f"   ❌ 數據庫連接失敗: {e}")
                return
            
            # 2. 檢查用戶登入狀態
            print("\n2. 檢查用戶數據...")
            users = User.query.all()
            print(f"   📊 用戶總數: {len(users)}")
            for user in users[:3]:
                print(f"   👤 用戶: {user.username} (ID: {user.id})")
            
            # 3. 檢查產品數據
            print("\n3. 檢查產品數據...")
            products = Product.query.all()
            print(f"   📦 產品總數: {len(products)}")
            for product in products[:3]:
                print(f"   🛍️ 產品: {product.name} (ID: {product.id})")
            
            # 4. 檢查現有評論
            print("\n4. 檢查現有評論...")
            for product in products[:2]:
                reviews = Review.query.filter_by(product_id=product.id).all()
                print(f"   📝 產品 '{product.name}' 有 {len(reviews)} 條評論")
                
                # 檢查用戶評論情況
                for user in users[:2]:
                    existing_review = Review.query.filter_by(
                        user_id=user.id,
                        product_id=product.id
                    ).first()
                    if existing_review:
                        print(f"      - 用戶 {user.username} 已評論過此產品")
                    else:
                        print(f"      - 用戶 {user.username} 未評論過此產品")
            
            # 5. 模擬API請求
            print("\n5. 模擬API請求...")
            if products and users:
                product_id = products[0].id
                user_id = users[0].id
                
                # 模擬評論數據
                review_data = {
                    'product_id': product_id,
                    'rating': 5,
                    'title': '測試評論',
                    'comment': '這是一個測試評論'
                }
                
                print(f"   📤 模擬提交評論數據:")
                print(f"      - 產品ID: {product_id}")
                print(f"      - 用戶ID: {user_id}")
                print(f"      - 評分: {review_data['rating']}")
                print(f"      - 標題: {review_data['title']}")
                print(f"      - 內容: {review_data['comment']}")
                
                # 檢查是否已評論過
                existing_review = Review.query.filter_by(
                    user_id=user_id,
                    product_id=product_id
                ).first()
                
                if existing_review:
                    print(f"   ⚠️ 用戶已評論過此產品，這會導致提交失敗")
                else:
                    print(f"   ✅ 用戶未評論過此產品，可以正常提交")
            
            # 6. 檢查常見問題
            print("\n6. 檢查常見問題...")
            
            # 檢查評分範圍
            print("   📊 評分範圍檢查:")
            for rating in range(0, 7):
                if 1 <= rating <= 5:
                    print(f"      - 評分 {rating}: ✅ 有效")
                else:
                    print(f"      - 評分 {rating}: ❌ 無效")
            
            # 檢查必填欄位
            print("   📝 必填欄位檢查:")
            test_cases = [
                {'product_id': 1, 'rating': 5, 'comment': 'test'},
                {'product_id': 1, 'rating': 5, 'comment': ''},
                {'product_id': 1, 'rating': 0, 'comment': 'test'},
                {'product_id': None, 'rating': 5, 'comment': 'test'},
            ]
            
            for i, case in enumerate(test_cases):
                is_valid = all([
                    case.get('product_id'),
                    case.get('rating') and 1 <= case.get('rating') <= 5,
                    case.get('comment')
                ])
                print(f"      - 測試案例 {i+1}: {'✅ 有效' if is_valid else '❌ 無效'}")
            
            print("\n✅ 診斷完成！")
            print("\n💡 可能的問題原因:")
            print("   1. 用戶未登入 (session中沒有user_id)")
            print("   2. 用戶已經評論過此產品")
            print("   3. 評分不在1-5範圍內")
            print("   4. 必填欄位未填寫")
            print("   5. 產品ID不存在")
            print("   6. 數據庫連接問題")
            
        except Exception as e:
            print(f"❌ 診斷失敗: {e}")

if __name__ == "__main__":
    debug_review_submission() 