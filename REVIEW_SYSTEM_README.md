# 評論系統使用說明

## 🎯 功能概述

評論系統為電商平台提供完整的用戶評價功能，包括評分、評論、投票等核心功能。

## ✨ 核心功能

### 📝 評論功能
- **評分系統**: 1-5 星評分，支援小數點平均分計算
- **評論內容**: 支援標題和詳細評論內容
- **驗證購買**: 標記是否為驗證購買的評論
- **權限管理**: 用戶只能編輯/刪除自己的評論

### 👍 投票機制
- **有用投票**: 用戶可對評論投"有用"票
- **單次限制**: 每人每評論限投一次
- **投票收回**: 用戶可以收回自己的投票
- **即時更新**: 投票數量即時更新

### 📊 統計功能
- **平均評分**: 自動計算產品平均評分
- **評論數量**: 顯示總評論數量
- **評分分布**: 支援評分統計分析
- **動態更新**: 統計數據即時更新

## 🚀 快速開始

### 1. 設置數據庫
```bash
# 創建評論表
python scripts/add_reviews_table.py

# 創建投票表
python scripts/add_review_votes_table.py

# 添加示例數據
python scripts/add_sample_reviews.py
```

### 2. 訪問評論功能
1. 登入用戶帳號
2. 進入任意產品頁面
3. 滾動到頁面底部的"評論區域"
4. 查看現有評論或添加新評論

## 📖 使用指南

### 查看評論
1. **進入產品頁面**: 點擊任意產品進入詳情頁
2. **滾動到評論區**: 頁面底部有專門的評論區域
3. **瀏覽評論**: 查看評分、標題、內容、投票數
4. **分頁瀏覽**: 支援分頁顯示大量評論

### 添加評論
1. **登入帳號**: 確保已登入用戶帳號
2. **點擊寫評論**: 在評論區域點擊"寫評論"按鈕
3. **填寫評分**: 點擊星星進行 1-5 星評分
4. **填寫標題**: 可選的評論標題
5. **填寫內容**: 必填的詳細評論內容
6. **提交評論**: 點擊"提交評論"按鈕

### 投票功能
1. **查看評論**: 在評論列表中查看評論
2. **點擊有用**: 點擊評論下方的"有用"按鈕
3. **收回投票**: 再次點擊可收回投票
4. **查看結果**: 投票數量會即時更新

### 管理評論
1. **編輯評論**: 點擊自己評論的"編輯"按鈕
2. **刪除評論**: 點擊自己評論的"刪除"按鈕
3. **確認刪除**: 系統會要求確認刪除操作

## 🔧 API 端點

### 獲取評論
```
GET /api/reviews/<product_id>
```
**參數**:
- `page`: 頁碼 (可選，預設 1)
- `per_page`: 每頁數量 (可選，預設 10)

**響應**:
```json
{
  "reviews": [...],
  "summary": {
    "average_rating": 4.2,
    "total_reviews": 15,
    "rating_stars": 4
  },
  "pagination": {
    "page": 1,
    "pages": 2,
    "per_page": 10,
    "total": 15
  }
}
```

### 添加評論
```
POST /api/reviews/add
```
**參數**:
- `product_id`: 產品ID
- `rating`: 評分 (1-5)
- `title`: 標題 (可選)
- `comment`: 評論內容

### 刪除評論
```
DELETE /api/reviews/<review_id>
```

### 投票功能
```
POST /api/reviews/<review_id>/helpful
```

## 🗄️ 數據庫結構

### Review 表
```sql
CREATE TABLE review (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    product_id INTEGER NOT NULL,
    rating INTEGER NOT NULL,
    title VARCHAR(200),
    comment TEXT NOT NULL,
    is_verified_purchase BOOLEAN DEFAULT FALSE,
    helpful_votes INTEGER DEFAULT 0,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### ReviewVote 表
```sql
CREATE TABLE review_vote (
    id INTEGER PRIMARY KEY,
    user_id INTEGER NOT NULL,
    review_id INTEGER NOT NULL,
    is_helpful BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(user_id, review_id)
);
```

## 🎨 前端實現

### 評論顯示
- **響應式設計**: 適配各種設備
- **動態加載**: AJAX 加載評論數據
- **分頁功能**: 支援大量評論分頁顯示
- **即時更新**: 評論統計即時更新

### 交互功能
- **星級評分**: 直觀的星級評分界面
- **投票按鈕**: 簡潔的投票交互
- **權限控制**: 根據用戶權限顯示操作按鈕
- **確認對話**: 刪除操作的安全確認

## 🔒 安全特性

### 權限控制
- **登入驗證**: 只有登入用戶才能評論
- **所有權驗證**: 用戶只能編輯/刪除自己的評論
- **投票限制**: 每人每評論只能投票一次

### 數據驗證
- **評分範圍**: 限制評分在 1-5 之間
- **內容驗證**: 評論內容不能為空
- **重複檢查**: 防止同一用戶對同一產品重複評論

## 🧪 測試功能

### 運行測試
```bash
# 測試評論系統
python tests/test_review_system.py

# 測試評論刪除修復
python scripts/test_review_deletion_fix.py

# 測試投票功能
python scripts/test_review_voting.py
```

### 診斷問題
```bash
# 診斷評論提交問題
python scripts/debug_review_submission.py

# 診斷評論刪除問題
python scripts/debug_review_deletion.py

# 測試投票切換功能
python scripts/test_vote_toggle.py
```

## 📊 功能統計

- **評論功能**: 完整的 CRUD 操作
- **投票系統**: 單次投票限制和收回功能
- **權限管理**: 完整的用戶權限控制
- **API 端點**: 4 個核心 API 端點
- **數據表**: 2 個核心數據表
- **測試覆蓋**: 完整的測試案例

## 🎯 最佳實踐

### 用戶體驗
1. **簡潔界面**: 評論區域設計簡潔直觀
2. **即時反饋**: 操作結果即時顯示
3. **錯誤處理**: 友好的錯誤提示
4. **權限提示**: 清楚的操作權限說明

### 技術實現
1. **模組化設計**: 評論功能獨立模組
2. **RESTful API**: 標準的 API 設計
3. **數據驗證**: 完整的輸入驗證
4. **安全性**: 權限控制和數據保護

## 🔮 未來規劃

### 短期目標
- [x] 基本評論功能 ✅
- [x] 投票機制 ✅
- [x] 權限管理 ✅
- [ ] 評論圖片上傳
- [ ] 評論回覆功能

### 中期目標
- [ ] 評論篩選和排序
- [ ] 評論舉報功能
- [ ] 管理員評論管理
- [ ] 評論數據分析

### 長期目標
- [ ] 評論推薦系統
- [ ] 評論情感分析
- [ ] 評論質量評分

---

⭐ 評論系統為電商平台提供完整的用戶評價功能，提升用戶體驗和產品可信度！ 