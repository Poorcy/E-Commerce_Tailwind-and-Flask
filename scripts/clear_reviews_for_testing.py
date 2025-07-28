#!/usr/bin/env python3
"""
清理評論以便重新測試的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, User, Product

def clear_reviews_for_testing():
    """清理評論以便重新測試"""
    print("🧹 開始清理評論以便重新測試...")
    
    with app.app_context():
        try:
            # 獲取所有評論
            all_reviews = Review.query.all()
            print(f"📊 當前有 {len(all_reviews)} 條評論")
            
            if len(all_reviews) == 0:
                print("✅ 沒有評論需要清理")
                return
            
            # 顯示要刪除的評論
            print("\n🗑️ 將刪除以下評論:")
            for review in all_reviews[:5]:  # 只顯示前5條
                print(f"   - {review.user.username} 對 {review.product.name}: {review.rating}星")
            
            if len(all_reviews) > 5:
                print(f"   ... 還有 {len(all_reviews) - 5} 條評論")
            
            # 確認刪除
            confirm = input("\n❓ 確定要刪除所有評論嗎？(y/N): ")
            if confirm.lower() != 'y':
                print("❌ 操作已取消")
                return
            
            # 刪除所有評論
            deleted_count = 0
            for review in all_reviews:
                db.session.delete(review)
                deleted_count += 1
            
            db.session.commit()
            print(f"✅ 成功刪除 {deleted_count} 條評論")
            
            # 驗證刪除結果
            remaining_reviews = Review.query.count()
            print(f"📊 剩餘評論數量: {remaining_reviews}")
            
            if remaining_reviews == 0:
                print("🎉 所有評論已清理完成！現在可以重新測試評論功能了")
            else:
                print("⚠️ 還有評論未刪除，請檢查")
                
        except Exception as e:
            print(f"❌ 清理評論失敗: {e}")
            db.session.rollback()

if __name__ == "__main__":
    clear_reviews_for_testing() 