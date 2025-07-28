from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
import json
from datetime import datetime, timedelta

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # 請改成安全的 key

# SQLite 連線設定（本地開發用）
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Flask 啟動時設定倒數結束時間
flash_sale_end = datetime.now() + timedelta(days=2)

# 範例 User 資料表
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)  # 新增密碼欄位
    first_name = db.Column(db.String(50), nullable=True)
    last_name = db.Column(db.String(50), nullable=True)
    address = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(20), nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f'<User {self.username}>'

# 產品資料表
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    category = db.Column(db.String(100), nullable=True)
    image_url = db.Column(db.String(500), nullable=True)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯到產品變體
    variants = db.relationship('ProductVariant', backref='product', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Product {self.name}>'

# 產品變體資料表（顏色、尺寸、庫存）
class ProductVariant(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    color = db.Column(db.String(50), nullable=True)  # 顏色
    size = db.Column(db.String(20), nullable=True)   # 尺寸
    stock_quantity = db.Column(db.Integer, default=0)  # 庫存數量
    sku = db.Column(db.String(100), unique=True, nullable=True)  # 商品編號
    price_adjustment = db.Column(db.Float, default=0.0)  # 價格調整（可選）
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<ProductVariant {self.color} {self.size}>'
    
    def get_final_price(self):
        """計算最終價格（產品價格 + 變體價格調整）"""
        if hasattr(self, 'product') and self.product:
            return self.product.price + self.price_adjustment
        return self.price_adjustment

# 購物車項目資料表
class CartItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'), nullable=True)
    quantity = db.Column(db.Integer, default=1, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯
    user = db.relationship('User', backref='cart_items')
    product = db.relationship('Product', backref='cart_items')
    variant = db.relationship('ProductVariant', backref='cart_items')
    
    def __repr__(self):
        return f'<CartItem {self.user.username} - {self.product.name} x{self.quantity}>'
    
    @property
    def total_price(self):
        """計算此項目的總價格"""
        if self.variant:
            return self.variant.get_final_price() * self.quantity
        return self.product.price * self.quantity
    
    @property
    def item_price(self):
        """計算單項價格"""
        if self.variant:
            return self.variant.get_final_price()
        return self.product.price

# 評論資料表
class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5 星評分
    title = db.Column(db.String(200), nullable=True)  # 評論標題
    comment = db.Column(db.Text, nullable=False)  # 評論內容
    is_verified_purchase = db.Column(db.Boolean, default=False)  # 是否為驗證購買
    helpful_votes = db.Column(db.Integer, default=0)  # 有用票數
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯
    user = db.relationship('User', backref='reviews')
    product = db.relationship('Product', backref='reviews')
    
    def __repr__(self):
        return f'<Review {self.user.username} - {self.product.name} - {self.rating}星>'
    
    def get_rating_stars(self):
        """獲取評分星數的HTML"""
        stars = ''
        for i in range(5):
            if i < self.rating:
                stars += '<span class="text-amber-400">★</span>'
            else:
                stars += '<span class="text-gray-300">★</span>'
        return stars

# 評論投票記錄資料表
class ReviewVote(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey('review.id'), nullable=False)
    is_helpful = db.Column(db.Boolean, default=True)  # True表示有用，False表示無用
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯
    user = db.relationship('User', backref='review_votes')
    review = db.relationship('Review', backref='votes')
    
    # 複合唯一索引，確保每個用戶對每個評論只能投票一次
    __table_args__ = (db.UniqueConstraint('user_id', 'review_id', name='unique_user_review_vote'),)
    
    def __repr__(self):
        return f'<ReviewVote {self.user.username} - Review {self.review_id} - {self.is_helpful}>'

# 願望清單項目資料表
class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # 關聯
    user = db.relationship('User', backref='wishlist_items')
    product = db.relationship('Product', backref='wishlist_items')
    
    def __repr__(self):
        return f'<WishlistItem {self.user.username} - {self.product.name}>'

# 訂單資料表
class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    order_number = db.Column(db.String(50), unique=True, nullable=False)  # 訂單編號
    status = db.Column(db.String(20), default='pending')  # 訂單狀態：pending, processing, shipped, delivered, cancelled
    total_amount = db.Column(db.Float, nullable=False)  # 訂單總金額
    shipping_fee = db.Column(db.Float, default=0.0)  # 運費
    recipient_name = db.Column(db.String(100), nullable=False)  # 收件人姓名
    recipient_phone = db.Column(db.String(20), nullable=False)  # 收件人電話
    recipient_address = db.Column(db.String(200), nullable=False)  # 收件地址
    payment_method = db.Column(db.String(20), nullable=False)  # 付款方式
    note = db.Column(db.Text, nullable=True)  # 備註
    estimated_delivery = db.Column(db.DateTime, nullable=False)  # 預計抵達日期
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # 關聯
    user = db.relationship('User', backref='orders')
    items = db.relationship('OrderItem', backref='order', lazy=True, cascade='all, delete-orphan')
    
    def __repr__(self):
        return f'<Order {self.order_number}>'
    
    def generate_order_number(self):
        """生成訂單編號"""
        import random
        import string
        timestamp = datetime.utcnow().strftime('%Y%m%d%H%M%S')
        random_chars = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
        return f"ORD{timestamp}{random_chars}"

# 訂單項目資料表
class OrderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('order.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    variant_id = db.Column(db.Integer, db.ForeignKey('product_variant.id'), nullable=True)
    product_name = db.Column(db.String(200), nullable=False)  # 商品名稱（快照）
    variant_info = db.Column(db.String(100), nullable=True)  # 變體信息（快照）
    price = db.Column(db.Float, nullable=False)  # 單價（快照）
    quantity = db.Column(db.Integer, nullable=False)  # 數量
    subtotal = db.Column(db.Float, nullable=False)  # 小計
    
    # 關聯
    product = db.relationship('Product', backref='order_items')
    variant = db.relationship('ProductVariant', backref='order_items')
    
    def __repr__(self):
        return f'<OrderItem {self.product_name} x{self.quantity}>'

@app.route('/')
def home():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    
    # 獲取精選產品（前4個產品）
    featured_products = Product.query.filter_by(is_active=True).limit(4).all()
    
    return render_template('Home_page.html', 
                         flash_sale_end=flash_sale_end.timestamp(), 
                         user=user, 
                         featured_products=featured_products)

@app.route('/product')
@app.route('/product/<int:product_id>')
def product(product_id=None):
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    
    # 如果有指定產品ID，則獲取該產品
    product_obj = None
    if product_id:
        product_obj = Product.query.get(product_id)
    else:
        # 檢查是否有查詢參數指定商品名稱
        product_name = request.args.get('name')
        if product_name:
            # 根據商品名稱查找商品
            product_obj = Product.query.filter_by(name=product_name).first()
            if not product_obj:
                # 如果找不到商品，重定向到404頁面
                return render_template('404.html', user=user), 404
        else:
            # 如果沒有指定產品ID或名稱，預設顯示第一個產品
            product_obj = Product.query.first()
    
    return render_template('Product.html', user=user, product=product_obj)

@app.route('/account', methods=['GET', 'POST'])
def account():
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('使用者不存在')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # 更新個人資料
        user.first_name = request.form.get('firstName', '')
        user.last_name = request.form.get('lastName', '')
        user.address = request.form.get('address', '')
        user.phone = request.form.get('phone', '')
        
        # 處理密碼變更
        current_password = request.form.get('currentPassword', '')
        new_password = request.form.get('newPassword', '')
        confirm_password = request.form.get('confirmPassword', '')
        
        if current_password and new_password and confirm_password:
            if not check_password_hash(user.password, current_password):
                flash('目前密碼錯誤')
                return render_template('Account.html', user=user)
            
            if new_password != confirm_password:
                flash('新密碼與確認密碼不符')
                return render_template('Account.html', user=user)
            
            user.password = generate_password_hash(new_password)
            flash('密碼更新成功')
        
        try:
            db.session.commit()
            flash('個人資料更新成功')
        except Exception as e:
            db.session.rollback()
            flash('更新失敗，請稍後再試')
        
        return redirect(url_for('account'))
    
    return render_template('Account.html', user=user)

@app.route('/about')
def about():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('About.html', user=user)

@app.route('/cart')
def cart():
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    cart_items = CartItem.query.filter_by(user_id=user.id).all()
    
    # 計算總計
    subtotal = sum(item.total_price for item in cart_items)
    shipping = 0 if subtotal >= 140 else 30  # 滿140免運費
    total = subtotal + shipping
    
    return render_template('Cart.html', user=user, cart_items=cart_items, 
                         subtotal=subtotal, shipping=shipping, total=total)

@app.route('/cart/add', methods=['POST'])
def add_to_cart():
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    user_id = session['user_id']
    product_id = request.form.get('product_id', type=int)
    variant_id = request.form.get('variant_id', type=int)
    quantity = request.form.get('quantity', 1, type=int)
    
    if not product_id:
        return {'success': False, 'message': '產品ID不能為空'}, 400
    
    # 檢查產品是否存在
    product = Product.query.get(product_id)
    if not product:
        return {'success': False, 'message': '產品不存在'}, 404
    
    # 檢查變體是否存在（如果指定了變體）
    variant = None
    if variant_id:
        variant = ProductVariant.query.get(variant_id)
        if not variant or variant.product_id != product_id:
            return {'success': False, 'message': '產品變體不存在'}, 404
    
    # 檢查是否已經在購物車中
    existing_item = CartItem.query.filter_by(
        user_id=user_id, 
        product_id=product_id, 
        variant_id=variant_id
    ).first()
    
    if existing_item:
        # 更新數量
        existing_item.quantity += quantity
        db.session.commit()
        return {'success': True, 'message': '購物車數量已更新'}
    else:
        # 新增到購物車
        cart_item = CartItem()
        cart_item.user_id = user_id
        cart_item.product_id = product_id
        cart_item.variant_id = variant_id
        cart_item.quantity = quantity
        db.session.add(cart_item)
        db.session.commit()
        return {'success': True, 'message': '已加入購物車'}

@app.route('/cart/update', methods=['POST'])
def update_cart():
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    user_id = session['user_id']
    item_id = request.form.get('item_id', type=int)
    quantity = request.form.get('quantity', type=int)
    
    if not item_id or quantity is None:
        return {'success': False, 'message': '參數錯誤'}, 400
    
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not cart_item:
        return {'success': False, 'message': '購物車項目不存在'}, 404
    
    if quantity <= 0:
        # 數量為0或負數，移除項目
        db.session.delete(cart_item)
        db.session.commit()
        return {'success': True, 'message': '項目已移除'}
    else:
        # 檢查庫存是否足夠
        if cart_item.variant:
            # 有變體的商品
            if cart_item.variant.stock_quantity < quantity:
                return {
                    'success': False, 
                    'message': f'庫存不足！商品 {cart_item.product.name} ({cart_item.variant.color}, {cart_item.variant.size}) 當前庫存: {cart_item.variant.stock_quantity}，您選擇的數量: {quantity}'
                }
        else:
            # 沒有變體的商品，檢查所有變體的總庫存
            total_stock = sum(variant.stock_quantity for variant in cart_item.product.variants)
            if total_stock < quantity:
                return {
                    'success': False, 
                    'message': f'庫存不足！商品 {cart_item.product.name} 當前總庫存: {total_stock}，您選擇的數量: {quantity}'
                }
        
        # 更新數量
        cart_item.quantity = quantity
        db.session.commit()
        return {'success': True, 'message': '數量已更新'}

@app.route('/cart/remove', methods=['POST'])
def remove_from_cart():
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    user_id = session['user_id']
    item_id = request.form.get('item_id', type=int)
    
    if not item_id:
        return {'success': False, 'message': '項目ID不能為空'}, 400
    
    cart_item = CartItem.query.filter_by(id=item_id, user_id=user_id).first()
    if not cart_item:
        return {'success': False, 'message': '購物車項目不存在'}, 404
    
    db.session.delete(cart_item)
    db.session.commit()
    return {'success': True, 'message': '項目已移除'}

@app.route('/cart/clear', methods=['POST'])
def clear_cart():
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    user_id = session['user_id']
    CartItem.query.filter_by(user_id=user_id).delete()
    db.session.commit()
    return {'success': True, 'message': '購物車已清空'}

@app.route('/checkout')
def checkout():
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('Checkout.html', user=user)

@app.route('/buy-now')
def buy_now():
    """立即購買結帳頁面"""
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    return render_template('BuyNow.html', user=user)

@app.route('/checkout/submit', methods=['POST'])
def submit_order():
    """提交訂單"""
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return {'success': False, 'message': '用戶不存在'}, 404
        
        # 獲取表單數據
        recipient_name = request.form.get('name')
        recipient_phone = request.form.get('phone')
        recipient_address = request.form.get('address')
        payment_method = request.form.get('payment')
        note = request.form.get('note', '')
        
        # 驗證必填欄位
        if not all([recipient_name, recipient_phone, recipient_address, payment_method]):
            return {'success': False, 'message': '請填寫所有必填欄位'}
        
        # 獲取選中的購物車商品ID
        selected_item_ids = request.form.get('selected_items')
        if not selected_item_ids:
            return {'success': False, 'message': '沒有選中的商品'}
        
        selected_item_ids = json.loads(selected_item_ids)
        
        # 獲取選中的購物車商品
        cart_items = CartItem.query.filter(
            CartItem.id.in_(selected_item_ids),
            CartItem.user_id == user.id
        ).all()
        
        if not cart_items:
            return {'success': False, 'message': '沒有找到選中的商品'}
        
        # 計算總金額
        subtotal = sum(item.total_price for item in cart_items)
        shipping_fee = 0 if subtotal >= 140 else 30
        total_amount = subtotal + shipping_fee
        
        # 創建訂單
        order = Order()
        order.user_id = user.id
        order.order_number = order.generate_order_number()
        order.total_amount = total_amount
        order.shipping_fee = shipping_fee
        order.recipient_name = recipient_name
        order.recipient_phone = recipient_phone
        order.recipient_address = recipient_address
        order.payment_method = payment_method
        order.note = note
        order.estimated_delivery = datetime.utcnow() + timedelta(days=7)  # 7天後抵達
        
        db.session.add(order)
        db.session.flush()  # 獲取訂單ID
        
        # 創建訂單項目並扣除庫存
        for cart_item in cart_items:
            # 檢查庫存是否足夠
            if cart_item.variant:
                # 有變體的商品
                if cart_item.variant.stock_quantity < cart_item.quantity:
                    db.session.rollback()
                    return {
                        'success': False, 
                        'message': f'商品 {cart_item.product.name} ({cart_item.variant.color}, {cart_item.variant.size}) 庫存不足，當前庫存: {cart_item.variant.stock_quantity}，需要: {cart_item.quantity}'
                    }
                
                # 扣除變體庫存
                cart_item.variant.stock_quantity -= cart_item.quantity
            else:
                # 沒有變體的商品，檢查所有變體的總庫存
                total_stock = sum(variant.stock_quantity for variant in cart_item.product.variants)
                if total_stock < cart_item.quantity:
                    db.session.rollback()
                    return {
                        'success': False, 
                        'message': f'商品 {cart_item.product.name} 庫存不足，當前總庫存: {total_stock}，需要: {cart_item.quantity}'
                    }
                
                # 從第一個有庫存的變體開始扣除
                remaining_quantity = cart_item.quantity
                for variant in cart_item.product.variants:
                    if remaining_quantity <= 0:
                        break
                    if variant.stock_quantity > 0:
                        deduct_amount = min(variant.stock_quantity, remaining_quantity)
                        variant.stock_quantity -= deduct_amount
                        remaining_quantity -= deduct_amount
            
            # 創建訂單項目
            order_item = OrderItem()
            order_item.order_id = order.id
            order_item.product_id = cart_item.product_id
            order_item.variant_id = cart_item.variant_id
            order_item.product_name = cart_item.product.name
            order_item.price = cart_item.item_price
            order_item.quantity = cart_item.quantity
            order_item.subtotal = cart_item.total_price
            
            # 保存變體信息
            if cart_item.variant:
                variant_info_parts = []
                if cart_item.variant.color:
                    variant_info_parts.append(f"顏色: {cart_item.variant.color}")
                if cart_item.variant.size:
                    variant_info_parts.append(f"尺寸: {cart_item.variant.size}")
                order_item.variant_info = ", ".join(variant_info_parts)
            
            db.session.add(order_item)
        
        # 從購物車中移除已結帳的商品
        for cart_item in cart_items:
            db.session.delete(cart_item)
        
        db.session.commit()
        
        return {
            'success': True, 
            'message': '訂單提交成功！',
            'order_number': order.order_number
        }
        
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': '訂單提交失敗，請稍後再試'}, 500

@app.route('/buy-now/submit', methods=['POST'])
def submit_buy_now_order():
    """提交立即購買訂單"""
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    try:
        user = User.query.get(session['user_id'])
        if not user:
            return {'success': False, 'message': '用戶不存在'}, 404
        
        # 獲取表單數據
        recipient_name = request.form.get('name')
        recipient_phone = request.form.get('phone')
        recipient_address = request.form.get('address')
        payment_method = request.form.get('payment')
        note = request.form.get('note', '')
        
        # 驗證必填欄位
        if not all([recipient_name, recipient_phone, recipient_address, payment_method]):
            return {'success': False, 'message': '請填寫所有必填欄位'}
        
        # 獲取立即購買的商品數據
        product_id = request.form.get('product_id', type=int)
        variant_id = request.form.get('variant_id', type=int)
        quantity = request.form.get('quantity', type=int)
        product_name = request.form.get('product_name')
        price = request.form.get('price', type=float)
        
        if not all([product_id, quantity, product_name, price]):
            return {'success': False, 'message': '商品數據不完整'}
        
        # 檢查庫存
        if variant_id:
            variant = ProductVariant.query.get(variant_id)
            if not variant or variant.stock_quantity < quantity:
                return {'success': False, 'message': '庫存不足'}
        else:
            product = Product.query.get(product_id)
            if not product:
                return {'success': False, 'message': '商品不存在'}
            total_stock = sum(v.stock_quantity for v in product.variants)
            if total_stock < quantity:
                return {'success': False, 'message': '庫存不足'}
        
        # 計算總金額
        subtotal = price * quantity
        shipping_fee = 0 if subtotal >= 140 else 30
        total_amount = subtotal + shipping_fee
        
        # 創建訂單
        order = Order()
        order.user_id = user.id
        order.order_number = order.generate_order_number()
        order.total_amount = total_amount
        order.shipping_fee = shipping_fee
        order.recipient_name = recipient_name
        order.recipient_phone = recipient_phone
        order.recipient_address = recipient_address
        order.payment_method = payment_method
        order.note = note
        order.estimated_delivery = datetime.utcnow() + timedelta(days=7)  # 7天後抵達
        
        db.session.add(order)
        db.session.flush()  # 獲取訂單ID
        
        # 創建訂單項目並扣除庫存
        order_item = OrderItem()
        order_item.order_id = order.id
        order_item.product_id = product_id
        order_item.variant_id = variant_id
        order_item.product_name = product_name
        order_item.price = price
        order_item.quantity = quantity
        order_item.subtotal = subtotal
        
        # 保存變體信息
        if variant_id and variant:
            variant_info_parts = []
            if variant.color:
                variant_info_parts.append(f"顏色: {variant.color}")
            if variant.size:
                variant_info_parts.append(f"尺寸: {variant.size}")
            order_item.variant_info = ", ".join(variant_info_parts)
        
        db.session.add(order_item)
        
        # 扣除庫存
        if variant_id and variant:
            variant.stock_quantity -= quantity
        else:
            # 從第一個有庫存的變體開始扣除
            remaining_quantity = quantity
            for variant in product.variants:
                if remaining_quantity <= 0:
                    break
                if variant.stock_quantity > 0:
                    deduct_amount = min(variant.stock_quantity, remaining_quantity)
                    variant.stock_quantity -= deduct_amount
                    remaining_quantity -= deduct_amount
        
        db.session.commit()
        
        return {
            'success': True, 
            'message': '訂單提交成功！',
            'order_number': order.order_number
        }
        
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': '訂單提交失敗，請稍後再試'}, 500

@app.route('/orders')
def orders():
    """訂單查詢頁面"""
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    if not user:
        session.clear()
        flash('用戶不存在')
        return redirect(url_for('login'))
    
    # 獲取用戶的所有訂單，按創建時間倒序排列
    orders = Order.query.filter_by(user_id=user.id).order_by(Order.created_at.desc()).all()
    
    return render_template('Orders.html', user=user, orders=orders)

@app.route('/contact')
def contact():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('Contact.html', user=user)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Login successful!')
            return redirect(url_for('home'))
        else:
            flash('Invalid email or password!')
            return redirect(url_for('login'))
    return render_template('Login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        # 檢查信箱是否已存在
        if User.query.filter_by(email=email).first():
            flash('Email already exists!')
            return redirect(url_for('signup'))
        
        # 生成唯一的 username（使用 email 的前綴）
        base_username = email.split('@')[0]
        username = base_username
        counter = 1
        
        # 如果 username 已存在，添加數字後綴
        while User.query.filter_by(username=username).first():
            username = f"{base_username}{counter}"
            counter += 1
        
        hashed_pw = generate_password_hash(password)
        user = User()
        user.username = username
        user.email = email
        user.password = hashed_pw
        user.first_name = ''
        user.last_name = ''
        user.address = ''
        user.phone = ''
        db.session.add(user)
        db.session.commit()
        flash('Sign up successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('Sign_up.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!')
    return redirect(url_for('home'))

@app.route('/wishlist')
def wishlist():
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    wishlist_items = WishlistItem.query.filter_by(user_id=user.id).all()
    
    return render_template('Wishlist.html', user=user, wishlist_items=wishlist_items)

# 管理儀表板路由
@app.route('/admin/dashboard')
def admin_dashboard():
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    
    # 統計數據
    total_users = User.query.count()
    total_products = Product.query.count()
    total_orders = Order.query.count()
    total_sales = db.session.query(db.func.sum(Order.total_amount)).scalar() or 0
    
    # 最近訂單（最近10筆）
    recent_orders = Order.query.order_by(Order.created_at.desc()).limit(10).all()
    
    # 庫存警告（庫存小於5的產品變體）
    low_stock_variants = ProductVariant.query.filter(ProductVariant.stock_quantity < 5).all()
    
    # 本月銷售額
    from datetime import datetime, timedelta
    start_of_month = datetime.now().replace(day=1, hour=0, minute=0, second=0, microsecond=0)
    monthly_sales = db.session.query(db.func.sum(Order.total_amount)).filter(
        Order.created_at >= start_of_month
    ).scalar() or 0
    
    # 待處理訂單數量
    pending_orders = Order.query.filter(Order.status == 'pending').count()
    
    return render_template('admin_dashboard.html', 
                         user=user,
                         total_users=total_users,
                         total_products=total_products,
                         total_orders=total_orders,
                         total_sales=total_sales,
                         recent_orders=recent_orders,
                         low_stock_variants=low_stock_variants,
                         monthly_sales=monthly_sales,
                         pending_orders=pending_orders)

# 產品管理路由
@app.route('/admin/products')
def admin_products():
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    products = Product.query.all()
    return render_template('admin_products.html', products=products, user=user)

@app.route('/admin/products/add', methods=['GET', 'POST'])
def add_product():
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # 新增產品
        product = Product()
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.category = request.form['category']
        product.image_url = request.form['image_url']
        
        db.session.add(product)
        db.session.commit()
        
        # 新增產品變體
        colors = request.form.getlist('colors[]')
        sizes = request.form.getlist('sizes[]')
        stocks = request.form.getlist('stocks[]')
        
        for i, color in enumerate(colors):
            if color.strip():  # 確保顏色不為空
                variant = ProductVariant()
                variant.product_id = product.id
                variant.color = color.strip()
                variant.size = sizes[i] if i < len(sizes) else None
                variant.stock_quantity = int(stocks[i]) if i < len(stocks) and stocks[i] else 0
                variant.sku = f"{product.id}-{color.strip()}-{sizes[i] if i < len(sizes) else 'N/A'}"
                db.session.add(variant)
        
        db.session.commit()
        flash('產品新增成功！')
        return redirect(url_for('admin_products'))
    
    return render_template('add_product.html')

@app.route('/admin/products/<int:product_id>')
def view_product(product_id):
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    user = User.query.get(session['user_id'])
    product = Product.query.get_or_404(product_id)
    return render_template('view_product.html', product=product, user=user)

@app.route('/admin/products/<int:product_id>/edit', methods=['GET', 'POST'])
def edit_product(product_id):
    if 'user_id' not in session:
        flash('請先登入')
        return redirect(url_for('login'))
    
    product = Product.query.get_or_404(product_id)
    
    if request.method == 'POST':
        # 更新產品基本資訊
        product.name = request.form['name']
        product.description = request.form['description']
        product.price = float(request.form['price'])
        product.category = request.form['category']
        product.image_url = request.form['image_url']
        
        # 更新變體資訊
        variant_ids = request.form.getlist('variant_id[]')
        variant_colors = request.form.getlist('variant_color[]')
        variant_sizes = request.form.getlist('variant_size[]')
        variant_stocks = request.form.getlist('variant_stock[]')
        
        for i, variant_id in enumerate(variant_ids):
            if variant_id:  # 現有變體 - 更新
                variant = ProductVariant.query.get(variant_id)
                if variant:
                    variant.color = variant_colors[i]
                    variant.size = variant_sizes[i]
                    variant.stock_quantity = int(variant_stocks[i]) if variant_stocks[i] else 0
            else:  # 新變體 - 新增
                if variant_colors[i].strip():  # 確保顏色不為空
                    new_variant = ProductVariant()
                    new_variant.product_id = product.id
                    new_variant.color = variant_colors[i].strip()
                    new_variant.size = variant_sizes[i] if variant_sizes[i] else None
                    new_variant.stock_quantity = int(variant_stocks[i]) if variant_stocks[i] else 0
                    new_variant.sku = f"{product.id}-{variant_colors[i].strip()}-{variant_sizes[i] if variant_sizes[i] else 'N/A'}"
                    db.session.add(new_variant)
        
        db.session.commit()
        flash('產品更新成功！')
        return redirect(url_for('view_product', product_id=product.id))
    
    return render_template('edit_product.html', product=product)

@app.route('/api/products')
def api_products():
    """API 端點：獲取所有產品"""
    products = Product.query.filter_by(is_active=True).all()
    result = []
    
    for product in products:
        product_data = {
            'id': product.id,
            'name': product.name,
            'description': product.description,
            'price': product.price,
            'category': product.category,
            'image_url': product.image_url,
            'variants': []
        }
        
        for variant in product.variants:
            if variant.is_active:
                variant_data = {
                    'id': variant.id,
                    'color': variant.color,
                    'size': variant.size,
                    'stock_quantity': variant.stock_quantity,
                    'sku': variant.sku,
                    'final_price': variant.get_final_price()
                }
                product_data['variants'].append(variant_data)
        
        result.append(product_data)
    
    return {'products': result}

@app.route('/api/products/<int:product_id>/variants')
def api_product_variants(product_id):
    """API 端點：獲取特定產品的變體數據"""
    product = Product.query.get_or_404(product_id)
    variants = []
    
    for variant in product.variants:
        if variant.is_active:
            variant_data = {
                'id': variant.id,
                'color': variant.color,
                'size': variant.size,
                'stock_quantity': variant.stock_quantity
            }
            variants.append(variant_data)
    
    return {'variants': variants}

@app.route('/api/wishlist/add', methods=['POST'])
def add_to_wishlist():
    """API 端點：添加產品到願望清單"""
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    user_id = session['user_id']
    product_id = request.form.get('product_id', type=int)
    
    if not product_id:
        return {'success': False, 'message': '產品ID不能為空'}, 400
    
    # 檢查產品是否存在
    product = Product.query.get(product_id)
    if not product:
        return {'success': False, 'message': '產品不存在'}, 404
    
    # 檢查是否已經在願望清單中
    existing_item = WishlistItem.query.filter_by(
        user_id=user_id, 
        product_id=product_id
    ).first()
    
    if existing_item:
        return {'success': False, 'message': '產品已在願望清單中'}, 400
    
    # 新增到願望清單
    wishlist_item = WishlistItem()
    wishlist_item.user_id = user_id
    wishlist_item.product_id = product_id
    
    try:
        db.session.add(wishlist_item)
        db.session.commit()
        return {'success': True, 'message': '已添加到願望清單'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': '添加失敗，請稍後再試'}, 500

@app.route('/api/wishlist/remove', methods=['POST'])
def remove_from_wishlist():
    """API 端點：從願望清單移除產品"""
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    user_id = session['user_id']
    product_id = request.form.get('product_id', type=int)
    
    if not product_id:
        return {'success': False, 'message': '產品ID不能為空'}, 400
    
    # 查找並移除願望清單項目
    wishlist_item = WishlistItem.query.filter_by(
        user_id=user_id, 
        product_id=product_id
    ).first()
    
    if not wishlist_item:
        return {'success': False, 'message': '產品不在願望清單中'}, 404
    
    try:
        db.session.delete(wishlist_item)
        db.session.commit()
        return {'success': True, 'message': '已從願望清單移除'}
    except Exception as e:
        db.session.rollback()
        return {'success': False, 'message': '移除失敗，請稍後再試'}, 500

@app.route('/api/wishlist/check/<int:product_id>')
def check_wishlist_status(product_id):
    """API 端點：檢查產品是否在願望清單中"""
    if 'user_id' not in session:
        return {'in_wishlist': False}
    
    user_id = session['user_id']
    wishlist_item = WishlistItem.query.filter_by(
        user_id=user_id, 
        product_id=product_id
    ).first()
    
    return {'in_wishlist': wishlist_item is not None}

@app.route('/api/cart/selected', methods=['POST'])
def get_selected_cart_items():
    """API 端點：獲取選中的購物車商品詳細信息"""
    if 'user_id' not in session:
        return {'success': False, 'message': '請先登入'}, 401
    
    try:
        data = request.get_json()
        item_ids = data.get('item_ids', [])
        
        if not item_ids:
            return {'success': False, 'message': '沒有選中的商品'}
        
        user_id = session['user_id']
        cart_items = CartItem.query.filter(
            CartItem.id.in_(item_ids),
            CartItem.user_id == user_id
        ).all()
        
        items_data = []
        for item in cart_items:
            variant_info = ""
            if item.variant:
                if item.variant.color:
                    variant_info += f"顏色: {item.variant.color}"
                if item.variant.size:
                    variant_info += f", 尺寸: {item.variant.size}"
            
            items_data.append({
                'id': item.id,
                'name': item.product.name,
                'price': item.item_price,
                'quantity': item.quantity,
                'image_url': item.product.image_url,
                'variant_info': variant_info
            })
        
        return {'success': True, 'items': items_data}
        
    except Exception as e:
        return {'success': False, 'message': '獲取商品信息失敗'}, 500

# 評論相關API
@app.route('/api/reviews/<int:product_id>', methods=['GET'])
def get_product_reviews(product_id):
    """獲取產品的所有評論"""
    try:
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # 獲取評論，按時間倒序排列
        reviews = Review.query.filter_by(product_id=product_id)\
                             .order_by(Review.created_at.desc())\
                             .paginate(page=page, per_page=per_page, error_out=False)
        
        reviews_data = []
        for review in reviews.items:
            # 檢查是否為驗證購買
            is_verified = False
            if 'user_id' in session:
                # 檢查用戶是否購買過此產品
                order_items = OrderItem.query.join(Order).filter(
                    OrderItem.product_id == product_id,
                    Order.user_id == session['user_id'],
                    Order.status.in_(['delivered', 'shipped'])
                ).first()
                is_verified = order_items is not None
            
            # 檢查當前用戶是否已投票
            user_voted = False
            if 'user_id' in session:
                user_vote = ReviewVote.query.filter_by(
                    user_id=session['user_id'],
                    review_id=review.id
                ).first()
                user_voted = user_vote is not None
            
            review_data = {
                'id': review.id,
                'user_name': review.user.username,
                'rating': review.rating,
                'title': review.title,
                'comment': review.comment,
                'is_verified_purchase': review.is_verified_purchase or is_verified,
                'helpful_votes': review.helpful_votes,
                'created_at': review.created_at.strftime('%Y-%m-%d %H:%M'),
                'can_edit': 'user_id' in session and review.user_id == session['user_id'],
                'user_voted': user_voted
            }
            reviews_data.append(review_data)
        
        # 計算平均評分
        avg_rating = db.session.query(db.func.avg(Review.rating))\
                               .filter_by(product_id=product_id).scalar()
        total_reviews = Review.query.filter_by(product_id=product_id).count()
        
        return jsonify({
            'success': True,
            'reviews': reviews_data,
            'pagination': {
                'page': page,
                'per_page': per_page,
                'total': reviews.total,
                'pages': reviews.pages,
                'has_next': reviews.has_next,
                'has_prev': reviews.has_prev
            },
            'summary': {
                'average_rating': round(avg_rating, 1) if avg_rating else 0,
                'total_reviews': total_reviews,
                'rating_stars': int(round(avg_rating, 0)) if avg_rating else 0
            }
        })
        
    except Exception as e:
        print(f"Error getting reviews: {e}")
        return jsonify({'error': '獲取評論失敗'}), 500

@app.route('/api/reviews/add', methods=['POST'])
def add_review():
    """添加評論"""
    if 'user_id' not in session:
        return jsonify({'error': '請先登入'}), 401
    
    try:
        data = request.get_json()
        product_id = data.get('product_id')
        rating = data.get('rating')
        title = data.get('title', '')
        comment = data.get('comment')
        
        if not all([product_id, rating, comment]):
            return jsonify({'error': '請填寫所有必要欄位'}), 400
        
        if not (1 <= rating <= 5):
            return jsonify({'error': '評分必須在1-5之間'}), 400
        
        # 檢查是否已經評論過
        existing_review = Review.query.filter_by(
            user_id=session['user_id'], 
            product_id=product_id
        ).first()
        
        if existing_review:
            return jsonify({'error': '您已經評論過此產品'}), 400
        
        # 檢查是否購買過此產品（驗證購買）
        is_verified = False
        order_items = OrderItem.query.join(Order).filter(
            OrderItem.product_id == product_id,
            Order.user_id == session['user_id'],
            Order.status.in_(['delivered', 'shipped'])
        ).first()
        is_verified = order_items is not None
        
        # 創建新評論
        new_review = Review(
            user_id=session['user_id'],
            product_id=product_id,
            rating=rating,
            title=title,
            comment=comment,
            is_verified_purchase=is_verified
        )
        
        db.session.add(new_review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '評論添加成功',
            'review_id': new_review.id
        })
        
    except Exception as e:
        print(f"Error adding review: {e}")
        db.session.rollback()
        return jsonify({'error': '添加評論失敗'}), 500

@app.route('/api/reviews/<int:review_id>', methods=['DELETE'])
def delete_review(review_id):
    """刪除評論"""
    if 'user_id' not in session:
        return jsonify({'error': '請先登入'}), 401
    
    try:
        review = Review.query.get_or_404(review_id)
        
        # 檢查權限
        if review.user_id != session['user_id']:
            return jsonify({'error': '無權限刪除此評論'}), 403
        
        # 先刪除相關的投票記錄
        votes = ReviewVote.query.filter_by(review_id=review_id).all()
        for vote in votes:
            db.session.delete(vote)
        
        # 再刪除評論
        db.session.delete(review)
        db.session.commit()
        
        return jsonify({
            'success': True,
            'message': '評論刪除成功'
        })
        
    except Exception as e:
        print(f"Error deleting review: {e}")
        db.session.rollback()
        return jsonify({'error': '刪除評論失敗'}), 500

@app.route('/api/reviews/<int:review_id>/helpful', methods=['POST'])
def mark_review_helpful(review_id):
    """標記評論為有用或收回投票"""
    if 'user_id' not in session:
        return jsonify({'error': '請先登入'}), 401
    
    try:
        review = Review.query.get_or_404(review_id)
        
        # 檢查用戶是否已經投票過
        existing_vote = ReviewVote.query.filter_by(
            user_id=session['user_id'],
            review_id=review_id
        ).first()
        
        if existing_vote:
            # 如果已經投票過，則收回投票
            db.session.delete(existing_vote)
            review.helpful_votes -= 1
            db.session.commit()
            
            return jsonify({
                'success': True,
                'helpful_votes': review.helpful_votes,
                'message': '已收回投票',
                'voted': False
            })
        else:
            # 如果沒有投票過，則添加投票
            vote = ReviewVote(
                user_id=session['user_id'],
                review_id=review_id,
                is_helpful=True
            )
            
            # 更新評論的有用票數
            review.helpful_votes += 1
            
            db.session.add(vote)
            db.session.commit()
            
            return jsonify({
                'success': True,
                'helpful_votes': review.helpful_votes,
                'message': '投票成功',
                'voted': True
            })
        
    except Exception as e:
        print(f"Error marking review helpful: {e}")
        db.session.rollback()
        return jsonify({'error': '操作失敗'}), 500

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # 啟動前自動建立資料表（開發用，正式環境建議用 migration 工具）
    with app.app_context():
        db.create_all()
    app.run(debug=True) 