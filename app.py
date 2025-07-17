from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
import os
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

@app.route('/')
def home():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('Home_page.html', flash_sale_end=flash_sale_end.timestamp(), user=user)

@app.route('/product')
def product():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('Product.html', user=user)

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
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('Cart.html', user=user)

@app.route('/checkout')
def checkout():
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('Checkout.html', user=user)

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
    user = None
    if 'user_id' in session:
        user = User.query.get(session['user_id'])
    return render_template('Wishlist.html', user=user)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # 啟動前自動建立資料表（開發用，正式環境建議用 migration 工具）
    with app.app_context():
        db.create_all()
    app.run(debug=True) 