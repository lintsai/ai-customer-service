from typing import List, Dict, Optional, Any
import json
import logging
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from langchain_chroma import Chroma
from src.core.config import settings
from src.llm.prompts.templates import prompt_templates

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
        self.base_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_templates.CUSTOMER_SERVICE_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 初始化特殊知識提示模板
        self.special_knowledge_prompt = ChatPromptTemplate.from_messages([
            ("system", prompt_templates.SPECIAL_KNOWLEDGE_PROMPT),
            MessagesPlaceholder(variable_name="history"),
            ("human", "{input}")
        ])
        
        # 創建基本對話鏈
        self.chain = self.base_prompt | self.llm | StrOutputParser()
        # 創建特殊知識對話鏈
        self.special_knowledge_chain = self.special_knowledge_prompt | self.llm | StrOutputParser()

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """生成一般回應"""
        try:
            history = self._format_chat_history(messages[:-1])
            
            if system_prompt:
                prompt = ChatPromptTemplate.from_messages([
                    ("system", system_prompt),
                    MessagesPlaceholder(variable_name="history"),
                    ("human", "{input}")
                ])
                chain = prompt | self.llm | StrOutputParser()
            else:
                chain = self.chain
            
            response = await chain.ainvoke({
                "history": history,
                "input": messages[-1]["content"]
            })
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"生成回應時發生錯誤: {str(e)}")
            raise Exception(f"無法生成回應: {str(e)}")

    async def generate_special_knowledge_response(
        self,
        messages: List[Dict[str, str]]
    ) -> str:
        """生成特殊知識回應"""
        try:
            history = self._format_chat_history(messages[:-1])
            
            response = await self.special_knowledge_chain.ainvoke({
                "history": history,
                "input": messages[-1]["content"]
            })
            
            return response.strip()
            
        except Exception as e:
            logger.error(f"生成特殊知識回應時發生錯誤: {str(e)}")
            raise Exception(f"無法生成回應: {str(e)}")

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

# 創建 LLM 引擎實例
llm_engine = LLMEngine()