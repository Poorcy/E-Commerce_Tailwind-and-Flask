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

    def __repr__(self):
        return f'<User {self.username}>'

@app.route('/')
def home():
    return render_template('Home_page.html', flash_sale_end=flash_sale_end.timestamp())

@app.route('/product')
def product():
    return render_template('Product.html')

@app.route('/account')
def account():
    return render_template('Account.html')

@app.route('/about')
def about():
    return render_template('About.html')

@app.route('/cart')
def cart():
    return render_template('Cart.html')

@app.route('/checkout')
def checkout():
    return render_template('Checkout.html')

@app.route('/contact')
def contact():
    return render_template('Contact.html')

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
            return redirect(url_for('account_dropdown'))
        else:
            flash('Invalid email or password!')
            return redirect(url_for('login'))
    return render_template('Login.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['name']  # 對應前端 name 欄位
        email = request.form['email']
        password = request.form['password']
        # 檢查帳號或信箱是否已存在
        if User.query.filter((User.username==username)|(User.email==email)).first():
            flash('Username or email already exists!')
            return redirect(url_for('signup'))
        hashed_pw = generate_password_hash(password)
        user = User(username=username, email=email, password=hashed_pw)
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
    return render_template('Wishlist.html')

@app.route('/account_dropdown')
def account_dropdown():
    return render_template('Account_Dropdown.html', flash_sale_end=flash_sale_end.timestamp())

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    # 啟動前自動建立資料表（開發用，正式環境建議用 migration 工具）
    with app.app_context():
        db.create_all()
    app.run(debug=True) 