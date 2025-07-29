#!/usr/bin/env python3
"""
創建簡單的測試用戶
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, User, db
from werkzeug.security import generate_password_hash

def create_simple_user():
    """創建簡單的測試用戶"""
    print("🔧 創建簡單的測試用戶...")
    
    with app.app_context():
        # 檢查用戶是否已存在
        existing_user = User.query.filter_by(username='simple').first()
        if existing_user:
            print("用戶 'simple' 已存在，刪除舊用戶...")
            db.session.delete(existing_user)
            db.session.commit()
        
        # 創建新用戶
        simple_user = User()
        simple_user.username = 'simple'
        simple_user.email = 'simple@test.com'
        simple_user.password = generate_password_hash('123456')
        simple_user.first_name = 'Simple'
        simple_user.last_name = 'User'
        
        try:
            db.session.add(simple_user)
            db.session.commit()
            print("✓ 簡單用戶創建成功")
            print("  用戶名: simple")
            print("  密碼: 123456")
            
            # 驗證用戶是否創建成功
            created_user = User.query.filter_by(username='simple').first()
            if created_user:
                print(f"  用戶ID: {created_user.id}")
                print("  用戶創建驗證成功")
            else:
                print("  用戶創建驗證失敗")
                
        except Exception as e:
            print(f"✗ 創建用戶失敗: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_simple_user() 