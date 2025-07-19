#!/usr/bin/env python3
"""
創建測試用戶
"""

from app import app, User, db
from werkzeug.security import generate_password_hash

def create_test_user():
    """創建測試用戶"""
    with app.app_context():
        # 檢查用戶是否已存在
        existing_user = User.query.filter_by(username='testuser').first()
        if existing_user:
            print("測試用戶已存在")
            return
        
        # 創建新用戶
        test_user = User()
        test_user.username = 'testuser'
        test_user.email = 'test@example.com'
        test_user.password = generate_password_hash('testpass')
        test_user.first_name = 'Test'
        test_user.last_name = 'User'
        
        try:
            db.session.add(test_user)
            db.session.commit()
            print("✓ 測試用戶創建成功")
            print("  用戶名: testuser")
            print("  密碼: testpass")
        except Exception as e:
            print(f"✗ 創建用戶失敗: {e}")
            db.session.rollback()

if __name__ == '__main__':
    create_test_user() 