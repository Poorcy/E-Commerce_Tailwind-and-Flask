#!/usr/bin/env python3
"""
測試產品描述編輯功能
"""

import requests
from app import app, Product, db

def test_edit_description():
    """測試編輯產品描述"""
    with app.app_context():
        # 獲取第一個產品
        product = Product.query.first()
        if not product:
            print("沒有找到產品，無法測試")
            return
        
        print(f"=== 測試產品描述編輯功能 ===")
        print(f"產品ID: {product.id}")
        print(f"產品名稱: {product.name}")
        print(f"原始描述: {product.description}")
        
        # 模擬編輯描述
        new_description = "這是更新後的產品描述，測試編輯功能是否正常工作。"
        product.description = new_description
        
        try:
            db.session.commit()
            print(f"✓ 描述更新成功")
            print(f"新描述: {product.description}")
        except Exception as e:
            print(f"✗ 更新失敗: {e}")
            db.session.rollback()

if __name__ == '__main__':
    test_edit_description() 