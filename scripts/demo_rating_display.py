#!/usr/bin/env python3
"""
演示評分顯示功能的腳本
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db, Review, Product, User
from sqlalchemy import func

def demo_rating_display():
    """演示評分顯示功能"""
    print("🎬 評分顯示功能演示")
    print("=" * 50)
    
    with app.app_context():
        try:
            # 1. 顯示所有產品的評分統計
            print("\n📊 產品評分統計:")
            
            # 查詢所有產品的平均評分
            products_with_ratings = db.session.query(
                Product.id,
                Product.name,
                func.avg(Review.rating).label('avg_rating'),
                func.count(Review.id).label('review_count')
            ).outerjoin(Review).group_by(Product.id, Product.name).all()
            
            for product_id, name, avg_rating, review_count in products_with_ratings:
                if avg_rating:
                    stars = "★" * int(round(avg_rating, 0)) + "☆" * (5 - int(round(avg_rating, 0)))
                    print(f"   - {name}: {avg_rating:.1f} ({stars}) - {review_count} 評論")
                else:
                    print(f"   - {name}: 無評論")
            
            # 2. 顯示評分分布
            print(f"\n📈 整體評分分布:")
            
            rating_distribution = db.session.query(
                Review.rating,
                func.count(Review.id).label('count')
            ).group_by(Review.rating).order_by(Review.rating).all()
            
            total_reviews = sum(count for _, count in rating_distribution)
            
            for rating, count in rating_distribution:
                percentage = (count / total_reviews * 100) if total_reviews > 0 else 0
                stars = "★" * rating + "☆" * (5 - rating)
                bar = "█" * int(percentage / 5)  # 每5%一個█
                print(f"   {stars} ({rating}星): {count:2d} 評論 ({percentage:5.1f}%) {bar}")
            
            # 3. 功能說明
            print(f"\n🎯 評分顯示功能說明:")
            print(f"   1. 產品頁面頂部顯示平均評分星數")
            print(f"   2. 評分根據用戶評論動態計算")
            print(f"   3. 支持小數評分（如4.2星）")
            print(f"   4. 顯示評論總數")
            print(f"   5. 評論區域顯示詳細評分統計")
            
            # 4. API端點說明
            print(f"\n🔗 API端點:")
            print(f"   - GET /api/reviews/<product_id>")
            print(f"   - 返回: {{'summary': {{'average_rating': 4.2, 'total_reviews': 8, 'rating_stars': 4}}}}")
            
            # 5. 前端功能說明
            print(f"\n💻 前端功能:")
            print(f"   - 產品頁面頂部評分圖示")
            print(f"   - 評論區域評分統計")
            print(f"   - 動態更新評分顯示")
            print(f"   - 支持部分星數顯示")
            
            # 6. 評分計算邏輯
            print(f"\n🧮 評分計算邏輯:")
            print(f"   - 平均評分 = 所有評論評分總和 / 評論數量")
            print(f"   - 評分星數 = 四捨五入(平均評分)")
            print(f"   - 支持1-5星評分系統")
            
            # 7. 顯示示例
            print(f"\n📝 顯示示例:")
            print(f"   - 4.2星平均評分 → 顯示4顆完整星")
            print(f"   - 4.7星平均評分 → 顯示5顆完整星")
            print(f"   - 3.5星平均評分 → 顯示4顆完整星")
            
            print(f"\n✅ 演示完成！")
            print(f"\n💡 使用提示:")
            print(f"   1. 訪問產品頁面查看評分顯示")
            print(f"   2. 添加評論後觀察評分變化")
            print(f"   3. 查看評論區域的詳細評分統計")
            print(f"   4. 觀察不同產品的評分差異")
            
        except Exception as e:
            print(f"❌ 演示失敗: {e}")

if __name__ == "__main__":
    demo_rating_display() 