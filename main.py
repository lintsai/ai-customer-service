from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.core.config import settings
from src.api.routes import test, chat, llm, knowledge

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Add CORS middleware with more specific configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # 前端開發伺服器的網址
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(test.router, prefix="/api/v1", tags=["test"])
app.include_router(chat.router, prefix="/api/v1/chat", tags=["chat"])
app.include_router(llm.router, prefix="/api/v1/llm", tags=["llm"])
app.include_router(knowledge.router, prefix="/api/v1/knowledge", tags=["knowledge"])

@app.get("/")
async def root():
    return {
        "message": "歡迎使用 AI 智慧客服系統",
        "version": settings.VERSION,
        "docs": "/docs"
    }