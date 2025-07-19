# 願望清單功能實現說明

## 功能概述

本項目已成功實現了完整的用戶願望清單功能，允許用戶：
- 在產品頁面和首頁點擊愛心按鈕將產品加入願望清單
- 查看自己的願望清單
- 從願望清單中移除產品
- 將願望清單中的產品加入購物車

## 實現的功能

### 1. 數據庫模型
- **WishlistItem**: 存儲用戶願望清單項目的數據模型
  - `user_id`: 用戶ID
  - `product_id`: 產品ID
  - `created_at`: 創建時間

### 2. API 端點
- `POST /api/wishlist/add`: 添加產品到願望清單
- `POST /api/wishlist/remove`: 從願望清單移除產品
- `GET /api/wishlist/check/<product_id>`: 檢查產品是否在願望清單中

### 3. 頁面功能
- **產品頁面**: 在產品標題旁邊顯示愛心按鈕
- **首頁**: 在產品卡片右上角顯示愛心按鈕
- **願望清單頁面**: 顯示用戶的所有願望清單項目

### 4. 用戶體驗
- 愛心按鈕會根據產品是否在願望清單中顯示不同狀態
  - 空心愛心 (empty_heart.png): 未加入願望清單
  - 實心愛心 (red_heart.png): 已在願望清單中
- 點擊愛心按鈕可以切換加入/移除狀態
- 願望清單頁面支持直接移除產品和加入購物車

## 技術實現

### 後端 (Flask)
```python
# 數據模型
class WishlistItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    user = db.relationship('User', backref='wishlist_items')
    product = db.relationship('Product', backref='wishlist_items')
```

### 前端 (JavaScript)
```javascript
// 愛心按鈕點擊事件
wishlistBtn.addEventListener('click', function() {
    const isInWishlist = wishlistIcon.src.includes('red_heart.png');
    
    if (isInWishlist) {
        // 從願望清單移除
        fetch('/api/wishlist/remove', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `product_id=${productId}`
        })
    } else {
        // 加入願望清單
        fetch('/api/wishlist/add', {
            method: 'POST',
            headers: {'Content-Type': 'application/x-www-form-urlencoded'},
            body: `product_id=${productId}`
        })
    }
});
```

## 使用方法

### 1. 啟動應用程序
```bash
python app.py
```

### 2. 登入系統
- 使用測試帳號: `test@example.com` / `password123`
- 或註冊新帳號

### 3. 使用願望清單功能
- **添加產品**: 在產品頁面或首頁點擊愛心按鈕
- **查看願望清單**: 點擊導航欄的"願望清單"連結
- **移除產品**: 在願望清單頁面點擊產品卡片右上角的愛心按鈕
- **加入購物車**: 在願望清單頁面點擊"加入購物車"按鈕

## 測試

運行測試腳本來驗證功能：
```bash
python test_wishlist.py
```

## 文件結構

```
full/
├── app.py                          # 主應用程序文件
├── templates/
│   ├── Home_page.html             # 首頁（包含愛心按鈕）
│   ├── Product.html               # 產品頁面（包含愛心按鈕）
│   └── Wishlist.html              # 願望清單頁面
├── static/
│   └── images/
│       ├── empty_heart.png        # 空心愛心圖標
│       └── red_heart.png          # 實心愛心圖標
├── test_wishlist.py               # 測試腳本
└── WISHLIST_README.md             # 本說明文件
```

## 注意事項

1. **用戶驗證**: 只有登入用戶才能使用願望清單功能
2. **產品唯一性**: 每個用戶對每個產品只能有一個願望清單項目
3. **圖片資源**: 確保 `static/images/` 目錄中有愛心圖標文件
4. **數據庫**: 系統會自動創建 `wishlist_item` 表

## 未來改進

1. 添加願望清單數量顯示在導航欄
2. 支持批量操作（批量移除、批量加入購物車）
3. 添加願望清單分享功能
4. 實現願望清單商品價格變動通知
5. 添加願望清單分類功能 