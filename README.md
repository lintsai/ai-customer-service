# AI 智慧客服系統

基於 OpenAI 的智慧客服系統，整合了大型語言模型、知識庫管理和對話管理功能。

## 功能特點

- 💬 即時智慧對話
- 📚 知識庫檢索增強
- 🤖 自動意圖識別
- 🎯 準確的回應生成
- 📊 對話歷史管理
- ⚡ 高效的資料處理

## 技術堆疊

### 後端技術
- FastAPI - 高性能 Web 框架
- MongoDB - 文檔資料庫
- Redis - 快取和會話管理
- OpenAI API - 大型語言模型
- ChromaDB - 向量資料庫

### 前端技術
- Next.js 13+ - React 框架
- TailwindCSS - 樣式框架
- TypeScript - 型別系統
- Lucide Icons - 圖標庫

## 快速開始

### 系統需求
- Python 3.9+
- Node.js 18+
- MongoDB
- Redis

### 後端設置

1. 建立虛擬環境：
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# 或
.\venv\Scripts\activate  # Windows
```

2. 安裝依賴：
```bash
pip install -r requirements.txt
```

3. 設定環境變數：
```bash
# 建立 .env 文件
cp .env.example .env
# 編輯 .env 文件，填入必要的設定
```

4. 啟動後端服務：
```bash
uvicorn main:app --reload
```

### 前端設置

1. 安裝依賴：
```bash
cd frontend
npm install
```

2. 設定環境變數：
```bash
cp .env.example .env.local
# 編輯 .env.local 文件，填入必要的設定
```

3. 啟動開發服務器：
```bash
npm run dev
```

## 專案結構

```
project/
├── backend/
│   ├── src/
│   │   ├── api/          # API 路由
│   │   ├── core/         # 核心配置
│   │   ├── db/           # 資料庫連接
│   │   ├── llm/          # LLM 服務
│   │   └── services/     # 業務邏輯
│   ├── requirements.txt
│   └── main.py
│
└── frontend/
    ├── app/              # Next.js 13 App Router
    ├── components/       # React 組件
    ├── styles/          # 全局樣式
    └── public/          # 靜態資源
```

## API 文檔

啟動後端服務後，可以訪問以下端點查看 API 文檔：
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## 開發指南

### 後端開發
- 遵循 PEP 8 Python 代碼規範
- 使用 async/await 處理異步操作
- 保持功能模組化和可測試性

### 前端開發
- 使用 TypeScript 進行型別檢查
- 遵循 React 最佳實踐
- 使用 TailwindCSS 進行樣式開發

## 測試

### 後端測試
```bash
cd backend
pytest
```

### 前端測試
```bash
cd frontend
npm test
```

## 部署

### 使用 Docker 部署
```bash
# 建構映像
docker-compose build

# 啟動服務
docker-compose up -d
```

## 開發路線圖

- [x] 基礎架構搭建（第零階段）
- [ ] 知識庫管理系統（第一階段）
- [ ] 對話增強功能（第二階段）
- [ ] 後台管理系統（第三階段）
- [ ] 系統優化和安全增強（第四階段）

## 貢獻指南

1. Fork 專案
2. 創建特性分支
3. 提交變更
4. 推送到分支
5. 創建 Pull Request

## 授權條款

此專案採用 [MIT 授權條款](LICENSE)。

## 關於

本專案是一個整合了多種先進技術的智慧客服系統，目標是提供高效、準確的自動化客戶服務解決方案。

## 聯絡方式

如有任何問題或建議，請透過以下方式聯繫：
- Email: lin15642@gmail.com
- Issues: 請在 GitHub 上創建 Issue