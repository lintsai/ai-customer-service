# src/llm/engine.py

from typing import List, Dict, Optional, Any
import json
import logging
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from src.core.config import settings

logger = logging.getLogger(__name__)

class LLMEngine:
    def __init__(self):
        # 初始化 LLM
        self.llm = ChatOpenAI(
            model_name=settings.OPENAI_MODEL,
            temperature=settings.OPENAI_TEMPERATURE,
            max_tokens=settings.OPENAI_MAX_TOKENS
        )
        
        # 初始化向量存儲
        self.embeddings = OpenAIEmbeddings()
        self.vectorstore = Chroma(
            embedding_function=self.embeddings,
            persist_directory="./data/vectordb"
        )
        
        # 初始化基本提示模板
        self.prompt = ChatPromptTemplate.from_messages([
            ("system", "你是一個專業的客服助理。請提供準確、有幫助的回答。"),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 創建基本鏈
        self.chain = self.prompt | self.llm | StrOutputParser()

    def _format_chat_history(self, messages: List[Dict[str, str]]) -> List[Any]:
        """將消息歷史轉換為 LangChain 消息格式"""
        formatted_messages = []
        for msg in messages:
            if msg["role"] == "system":
                formatted_messages.append(SystemMessage(content=msg["content"]))
            elif msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            elif msg["role"] == "assistant":
                formatted_messages.append(AIMessage(content=msg["content"]))
        return formatted_messages

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """生成回應"""
        try:
            # 準備聊天歷史
            history = self._format_chat_history(messages[:-1])
            
            # 如果有系統提示，更新提示模板
            if system_prompt:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "{input}")
                ])
                chain = prompt | self.llm | StrOutputParser()
            else:
                chain = self.chain
            
            # 生成回應
            response = await chain.ainvoke({
                "history": history,
                "input": messages[-1]["content"]
            })
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"生成回應時發生錯誤: {str(e)}")
            raise Exception(f"無法生成回應: {str(e)}")

    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """情感分析"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """分析以下文本的情感，以 JSON 格式返回：
                {
                    "score": (數字，介於-1到1之間),
                    "label": "情感標籤",
                    "explanation": "分析說明"
                }"""),
                ("human", "{text}")
            ])
            
            chain = prompt | self.llm | StrOutputParser()
            response = await chain.ainvoke({"text": text})
            
            try:
                result = json.loads(response)
                return {
                    "text": text,
                    "sentiment_score": float(result["score"]),
                    "sentiment_label": result["label"],
                    "explanation": result["explanation"]
                }
            except json.JSONDecodeError:
                raise ValueError("無法解析情感分析結果")
            
        except Exception as e:
            logger.error(f"情感分析時發生錯誤: {str(e)}")
            raise Exception(f"無法進行情感分析: {str(e)}")

    async def detect_intent(self, text: str) -> Dict[str, str]:
        """意圖檢測"""
        try:
            prompt = ChatPromptTemplate.from_messages([
                ("system", """分析以下客服對話信息的意圖，以 JSON 格式返回：
                {
                    "intent": "意圖分類",
                    "confidence": 信心分數,
                    "explanation": "分類說明"
                }"""),
                ("human", "{text}")
            ])
            
            chain = prompt | self.llm | StrOutputParser()
            response = await chain.ainvoke({"text": text})
            
            try:
                result = json.loads(response)
                return result
            except json.JSONDecodeError:
                raise ValueError("無法解析意圖分析結果")
            
        except Exception as e:
            logger.error(f"意圖檢測時發生錯誤: {str(e)}")
            raise Exception(f"無法檢測意圖: {str(e)}")

    async def search_knowledge_base(self, query: str, k: int = 3) -> List[str]:
        """搜索知識庫"""
        try:
            docs = await self.vectorstore.asimilarity_search(query, k=k)
            return [doc.page_content for doc in docs]
        except Exception as e:
            logger.error(f"搜索知識庫時發生錯誤: {str(e)}")
            raise Exception(f"無法搜索知識庫: {str(e)}")

# Create LLM engine instance
llm_engine = LLMEngine()