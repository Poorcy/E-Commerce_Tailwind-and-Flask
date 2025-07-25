# Exclusive 電商平台

## 🎯 專案概述

這是我獨立開發的完整電商網站，採用現代化的 Web 技術棧。
UI 設計參考自 [Figma 範本](https://www.figma.com/design/TXKTwUTSp7Vwl2mDkOpZ1w/Full-E-Commerce-Website-UI-UX-Design--Community-?node-id=1-3&p=f&t=GskzpELhvVBp9PrF-0)，
後端邏輯和功能實現完全由我獨立開發。
專案重點在於展示完整的電商業務邏輯實現和全端開發能力。

**技術棧**: Python, Flask, SQLAlchemy, SQLite, HTML/CSS, JavaScript, Tailwind CSS

## ✨ 核心功能

### 🛒 電商核心功能
- **用戶認證系統**: 註冊、登入、個人資料管理
- **產品管理**: 完整的 CRUD 操作，支援產品變體
- **購物車系統**: 持久化購物車，支援產品變體選擇
- **願望清單**: 收藏喜愛的商品
- **訂單系統**: 完整的訂單處理流程
- **庫存管理**: 即時庫存追蹤和驗證

### 🎨 用戶體驗
- **響應式設計**: 適配桌面和移動設備
- **動態交互**: JavaScript 實現流暢的用戶體驗
- **即時驗證**: 表單驗證和庫存檢查
- **狀態管理**: 購物車和願望清單狀態同步

### 🔧 管理功能
- **管理儀表板**: 完整的數據概覽和快速操作
- **產品管理後台**: 完整的產品 CRUD 操作
- **庫存監控**: 庫存狀態可視化和警告系統
- **訂單追蹤**: 訂單狀態管理和歷史查詢
- **用戶管理**: 用戶資料和訂單查詢
- **統計分析**: 銷售數據和用戶統計

## 🏗️ 系統架構

### 設計參考
- **UI 設計**: 參考 [Figma 範本](https://www.figma.com/design/TXKTwUTSp7Vwl2mDkOpZ1w/Full-E-Commerce-Website-UI-UX-Design--Community-?node-id=1-3&p=f&t=GskzpELhvVBp9PrF-0)
- **後端邏輯**: 完全自主設計和實現
- **資料庫設計**: 根據業務需求自主設計

### 技術架構
- **後端**: Flask + SQLAlchemy (ORM)
- **前端**: Tailwind CSS + JavaScript
- **資料庫**: SQLite (可擴展到 PostgreSQL/MySQL)
- **模板引擎**: Jinja2
- **認證**: Werkzeug Security

## 🚀 快速開始

### 環境需求
- Python 3.7+
- pip

### 安裝步驟

1. **複製專案**
   ```bash
   git clone [your-repo-url]
   cd tailwind-and-Flask
   ```

2. **安裝依賴**
   ```bash
   pip install -r requirements.txt
   ```

3. **啟動應用**
   ```bash
   python app.py
   ```

4. **訪問網站**
   - 主頁: http://localhost:5000
   - 管理儀表板: http://localhost:5000/admin/dashboard
   - 產品管理: http://localhost:5000/admin/products

### 創建演示數據（可選）
```bash
# 創建測試數據和管理員帳號
python scripts/demo_admin_dashboard.py
```
**管理員登入資訊**:
- 帳號: admin
- 密碼: admin123

### 測試功能
```bash
# 運行所有測試
python -m pytest tests/

# 運行特定測試
python tests/test_cart.py
python tests/test_products.py
```

## 📁 專案結構

```
tailwind-and-Flask/
├── app.py                 # 主應用程式
├── requirements.txt       # Python 依賴
├── README.md             # 專案文檔
├── instance/
│   └── site.db           # SQLite 資料庫
├── static/               # 靜態資源
│   └── images/           # 圖片資源
├── templates/            # HTML 模板
│   ├── Home_page.html    # 首頁
│   ├── Product.html      # 產品頁面
│   ├── Cart.html         # 購物車
│   ├── Checkout.html     # 結帳頁面
│   ├── Orders.html       # 訂單查詢
│   ├── Wishlist.html     # 願望清單
│   ├── Account.html      # 個人資料
│   ├── Login.html        # 登入頁面
│   ├── Sign_up.html      # 註冊頁面
│   ├── admin_dashboard.html # 管理儀表板
│   └── admin_*.html      # 管理後台
├── tests/                # 測試檔案
│   ├── test_cart.py      # 購物車測試
│   ├── test_products.py  # 產品測試
│   ├── test_order_system.py # 訂單系統測試
│   └── ...               # 其他測試
└── scripts/              # 工具腳本
    ├── add_all_products.py # 批量添加產品
    ├── create_test_user.py # 創建測試用戶
    ├── demo_admin_dashboard.py # 管理儀表板演示數據
    └── ...               # 其他腳本
```

## 🔧 核心功能詳解

### 購物車系統
- **持久化**: 用戶登入後購物車數據自動保存
- **變體支援**: 支援選擇顏色、尺寸等產品變體
- **庫存驗證**: 即時檢查庫存是否充足
- **價格計算**: 自動計算小計、運費、總計
- **批量操作**: 支援批量選擇和結帳

### 訂單系統
- **訂單編號**: 自動生成唯一訂單編號
- **狀態追蹤**: 訂單狀態管理 (pending → processing → shipped → delivered)
- **庫存扣除**: 訂單確認後自動扣除庫存
- **預計送達**: 自動計算預計送達日期
- **訂單快照**: 保存訂單時的產品資訊

### 產品管理
- **變體系統**: 支援顏色、尺寸、庫存獨立管理
- **SKU 管理**: 自動生成商品編號
- **價格調整**: 變體可設定價格調整
- **庫存監控**: 庫存狀態可視化顯示和警告系統
- **圖片管理**: 支援產品圖片上傳

### 管理儀表板
- **數據概覽**: 用戶數、產品數、訂單數、銷售額統計
- **最近訂單**: 顯示最近 10 筆訂單詳情
- **庫存警告**: 自動檢測低庫存產品並提醒
- **快速操作**: 一鍵跳轉到新增產品、管理產品、查看訂單
- **系統狀態**: 資料庫和網站運行狀態監控
- **自動刷新**: 每 5 分鐘自動更新數據

## 🎨 設計亮點

### 用戶體驗
- **響應式設計**: 完美適配各種設備
- **直觀導航**: 清晰的網站結構和導航
- **即時反饋**: 操作結果即時顯示
- **錯誤處理**: 友好的錯誤提示

### 技術實現
- **模組化設計**: 清晰的代碼結構
- **RESTful API**: 標準的 API 設計
- **資料驗證**: 完整的輸入驗證
- **安全性**: 密碼加密、SQL 注入防護

## 📊 功能統計

- **頁面數量**: 16+ 個完整頁面
- **API 端點**: 20+ 個 RESTful API
- **資料表**: 6 個核心資料表
- **測試案例**: 30+ 個測試檔案
- **功能模組**: 9 個核心功能模組
- **管理功能**: 完整的儀表板和數據分析

## 📊 管理儀表板功能

### 🎯 核心功能
- **數據概覽**: 即時顯示用戶數、產品數、訂單數、總銷售額
- **本月統計**: 當月銷售額和待處理訂單數量
- **最近訂單**: 顯示最近 10 筆訂單的詳細資訊
- **庫存警告**: 自動檢測庫存低於 5 件的產品並提醒
- **快速操作**: 一鍵跳轉到新增產品、管理產品、查看訂單
- **系統狀態**: 監控資料庫和網站運行狀態

### 🚀 快速訪問
1. **登入後**: 點擊右上角「我的帳號」→「管理儀表板」
2. **直接訪問**: http://localhost:5000/admin/dashboard
3. **全域導航**: 所有登入後頁面都可快速訪問管理儀表板

### 📈 數據統計
- **用戶統計**: 總註冊用戶數和活躍用戶
- **產品統計**: 總產品數和變體數量
- **訂單統計**: 總訂單數和銷售額
- **庫存監控**: 低庫存產品自動警告
- **系統監控**: 資料庫連接和網站狀態

### 🔧 管理工具
- **產品管理**: 完整的 CRUD 操作和變體管理
- **訂單管理**: 訂單狀態追蹤和歷史查詢
- **庫存管理**: 即時庫存監控和警告系統
- **用戶管理**: 用戶資料和訂單查詢

## 🔮 未來規劃

### 短期目標 
- [x] 完整的管理儀表板 ✅
- [ ] 產品搜尋和篩選功能
- [ ] 電子郵件通知系統
- [ ] 銷售圖表和數據分析

### 中期目標 
- [ ] 真實支付系統整合
- [ ] 用戶評價和評論系統
- [x] 庫存警告功能 ✅
- [ ] 批量操作和數據導出

### 長期目標 
- [ ] 移動端 APP
- [ ] 多語言支援
- [ ] 進階分析功能

## 🤝 貢獻指南

歡迎提交 Issue 和 Pull Request！

### 開發環境設置
1. Fork 本專案
2. 創建功能分支
3. 提交變更
4. 發起 Pull Request

## 📄 授權

**MIT License**

本專案採用 MIT 授權條款，詳見 [LICENSE](LICENSE) 檔案。

## 👨‍💻 作者

**開發者**: 張維安
**GitHub**: [Poorcy](https://github.com/Poorcy)
**技術棧**: Python, Flask, SQLAlchemy, Tailwind CSS
**專案類型**: 獨立開發的電商平台
**設計參考**: [Figma 範本](https://www.figma.com/design/TXKTwUTSp7Vwl2mDkOpZ1w/Full-E-Commerce-Website-UI-UX-Design--Community-?node-id=1-3&p=f&t=GskzpELhvVBp9PrF-0)

---

## 📚 相關文檔

- [管理儀表板使用說明](ADMIN_DASHBOARD_README.md) - 詳細的使用指南
- [管理儀表板實作總結](DASHBOARD_SUMMARY.md) - 技術實作詳情
- [導航更新總結](NAVIGATION_UPDATE_SUMMARY.md) - 全域導航整合
- [返回按鈕更新總結](DASHBOARD_RETURN_BUTTONS_SUMMARY.md) - 頁面導航優化

## 🎯 專案亮點

- ✅ **完整電商功能**: 從用戶註冊到訂單完成的完整流程
- ✅ **現代化設計**: 響應式設計，支援各種設備
- ✅ **管理儀表板**: 完整的數據分析和管理工具
- ✅ **測試覆蓋**: 30+ 個測試檔案確保功能穩定
- ✅ **文檔完整**: 詳細的使用說明和技術文檔

⭐ 如果這個專案對你有幫助，請給個 Star！

