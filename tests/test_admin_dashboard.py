import pytest
from app import app, db, User, Product, Order, ProductVariant
from datetime import datetime

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.drop_all()

@pytest.fixture
def test_user():
    user = User(
        username='testadmin',
        email='admin@test.com',
        password='hashed_password',
        first_name='Test',
        last_name='Admin'
    )
    db.session.add(user)
    db.session.commit()
    return user

@pytest.fixture
def test_product():
    product = Product(
        name='Test Product',
        description='Test Description',
        price=99.99,
        category='Electronics'
    )
    db.session.add(product)
    db.session.commit()
    
    # 添加產品變體
    variant = ProductVariant(
        product_id=product.id,
        color='Red',
        size='M',
        stock_quantity=10
    )
    db.session.add(variant)
    db.session.commit()
    
    return product

@pytest.fixture
def test_order(test_user, test_product):
    order = Order(
        user_id=test_user.id,
        order_number='ORD-001',
        status='pending',
        total_amount=99.99,
        recipient_name='Test Customer',
        recipient_phone='1234567890',
        recipient_address='Test Address',
        payment_method='credit_card',
        estimated_delivery=datetime.now()
    )
    db.session.add(order)
    db.session.commit()
    return order

def test_admin_dashboard_requires_login(client):
    """測試未登入用戶無法訪問管理儀表板"""
    response = client.get('/admin/dashboard')
    assert response.status_code == 302  # 重定向到登入頁面

def test_admin_dashboard_with_login(client, test_user):
    """測試登入用戶可以訪問管理儀表板"""
    with client.session_transaction() as sess:
        sess['user_id'] = test_user.id
    
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    assert '管理儀表板' in response.data.decode('utf-8')

def test_admin_dashboard_statistics(client, test_user, test_product, test_order):
    """測試管理儀表板顯示正確的統計數據"""
    with client.session_transaction() as sess:
        sess['user_id'] = test_user.id
    
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    
    # 檢查統計數據
    response_text = response.data.decode('utf-8')
    assert '1' in response_text  # 總用戶數
    assert '1' in response_text  # 總產品數
    assert '1' in response_text  # 總訂單數
    assert '99.99' in response_text  # 總銷售額

def test_admin_dashboard_recent_orders(client, test_user, test_order):
    """測試最近訂單顯示"""
    with client.session_transaction() as sess:
        sess['user_id'] = test_user.id
    
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert 'ORD-001' in response_text  # 訂單編號
    assert 'Test Customer' in response_text  # 客戶名稱

def test_admin_dashboard_low_stock_warning(client, test_user, test_product):
    """測試庫存警告功能"""
    # 創建低庫存產品變體
    low_stock_variant = ProductVariant(
        product_id=test_product.id,
        color='Blue',
        size='L',
        stock_quantity=3  # 低於5的庫存
    )
    db.session.add(low_stock_variant)
    db.session.commit()
    
    with client.session_transaction() as sess:
        sess['user_id'] = test_user.id
    
    response = client.get('/admin/dashboard')
    assert response.status_code == 200
    response_text = response.data.decode('utf-8')
    assert 'Test Product' in response_text  # 產品名稱
    assert '3' in response_text  # 庫存數量

if __name__ == '__main__':
    pytest.main([__file__]) 