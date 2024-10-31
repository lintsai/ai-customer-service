# AI 智慧客服系統

基於 OpenAI 和 LangChain 的智慧客服系統，整合了大型語言模型、知識庫管理和對話管理功能。

## 功能特點

- 💬 即時智慧對話
  - 基於 GPT 的自然語言處理
  - 多輪對話支援
  - 上下文理解和記憶

- 📚 知識庫管理
  - RAG（檢索增強生成）
  - 向量化文檔搜索
  - 動態知識更新

- 🤖 對話增強
  - 自動意圖識別
  - 情感分析
  - 智能路由分配

- 🎯 品質控制
  - 回應準確性評估
  - 對話品質監控
  - 自動糾錯機制

- 📊 數據分析
  - 對話歷史管理
  - 使用者行為分析
  - 效能統計報告

## 技術堆疊

### 後端技術
- FastAPI - Web 框架
- MongoDB - 文檔數據庫
- Redis - 快取和會話管理
- ChromaDB - 向量數據庫
- LangChain - LLM 應用框架

### AI/LLM
- OpenAI GPT - 大型語言模型
- LangChain 整合：
  - langchain-core - 核心功能
  - langchain-openai - OpenAI 整合
  - langchain-chroma - 向量數據庫整合

### 前端技術
- Next.js 13+ - React 框架
- TailwindCSS - 樣式框架
- TypeScript - 類型系統
- Lucide Icons - 圖標庫

## 快速開始

### 系統需求
- Python 3.9+
- Node.js 18+
- MongoDB
- Redis
- OpenAI API 金鑰

### 後端設置

1. 建立虛擬環境：
```bash
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
cp .env.example .env
# 編輯 .env 文件，填入必要的設定：
# - OPENAI_API_KEY
# - MongoDB 連接設定
# - Redis 連接設定
```

4. 啟動後端服務：
```bash
uvicorn main:app --reload
```

### 前端設置

1. 安裝依賴：
```bash
npm install
```

2. 設定環境變數：
```bash
cp .env.example .env.local
# 編輯 .env.local 文件
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
│   │   │   ├── routes/   # 路由定義
│   │   │   └── middleware/ # 中間件
│   │   ├── core/         # 核心配置
│   │   ├── db/           # 數據庫連接
│   │   │   ├── mongodb/  # MongoDB 操作
│   │   │   ├── redis/    # Redis 操作
│   │   │   └── vector/   # 向量數據庫
│   │   ├── llm/          # LLM 服務
│   │   │   ├── engine.py # LLM 引擎
│   │   │   └── prompts/  # 提示模板
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

## 主要 API 端點

### 對話管理
- POST `/api/v1/chat/conversations` - 建立新對話
- POST `/api/v1/chat/conversations/{conversation_id}/messages` - 發送消息
- GET `/api/v1/chat/conversations/{conversation_id}` - 獲取對話歷史

### LLM 服務
- POST `/api/v1/llm/generate` - 生成回應
- POST `/api/v1/llm/analyze/sentiment` - 情感分析
- POST `/api/v1/llm/analyze/intent` - 意圖檢測

## 開發指南

### 後端開發
- 使用 async/await 進行非同步操作
- 遵循 PEP 8 代碼規範
- 使用類型提示增加代碼可讀性
- 確保錯誤處理和日誌記錄

### 前端開發
- 使用 TypeScript 進行類型檢查
- 遵循 React 最佳實踐
- 使用 TailwindCSS 進行樣式開發
- 實現響應式設計

## 測試

### 後端測試
```bash
pytest
```

### 前端測試
```bash
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

### 已完成 ✅
- [x] 基礎架構搭建（第零階段）
  - [x] FastAPI 框架設置
  - [x] 資料庫連接
  - [x] LLM 整合
  - [x] 基本對話功能

### 進行中 🔄
- [ ] 知識庫管理系統（第一階段）
  - [x] 向量數據庫整合
  - [ ] RAG 實現
  - [ ] 知識庫更新機制

### 計劃中 📋
- [ ] 對話增強功能（第二階段）
  - [ ] 意圖識別優化
  - [ ] 情感分析整合
  - [ ] 多輪對話優化

- [ ] 後台管理系統（第三階段）
  - [ ] 管理介面開發
  - [ ] 數據分析功能
  - [ ] 監控系統

- [ ] 系統優化和安全增強（第四階段）
  - [ ] 性能優化
  - [ ] 安全增強
  - [ ] 系統監控

## 貢獻指南

1. Fork 專案
2. 創建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 開啟 Pull Request

## 授權條款

此專案採用 [MIT 授權條款](LICENSE)。

## 關於

本專案是一個整合了最新 AI 技術的智慧客服系統，目標是提供高效、準確的自動化客戶服務解決方案。我們持續關注 AI 技術的發展，並不斷更新和優化系統功能。

## 支持與反饋

如有任何問題或建議，請透過以下方式聯繫：
- 提交 Issue
- 發送郵件至 [lin15642@gmail.com](mailto:lin15642@gmail.com)
- 參與討論區討論