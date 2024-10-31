from typing import List, Dict, Optional, Any
from openai import AsyncOpenAI
from src.core.config import settings
import json
import logging
import re

logger = logging.getLogger(__name__)

class LLMEngine:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
        self.model = settings.OPENAI_MODEL
        self.temperature = settings.OPENAI_TEMPERATURE
        self.max_tokens = settings.OPENAI_MAX_TOKENS

    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        system_prompt: Optional[str] = None
    ) -> str:
        """生成 AI 回應"""
        try:
            api_messages = []
            
            if system_prompt:
                api_messages.append({
                    "role": "system",
                    "content": system_prompt
                })
            
            api_messages.extend(messages)
            
            logger.debug(f"發送請求至 OpenAI: {json.dumps(api_messages, indent=2, ensure_ascii=False)}")
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=api_messages,
                temperature=self.temperature,
                max_tokens=self.max_tokens
            )
            
            response_text = response.choices[0].message.content
            
            logger.debug(f"收到 OpenAI 回應: {response_text}")
            
            return response_text
            
        except Exception as e:
            logger.error(f"生成回應時發生錯誤: {str(e)}")
            raise Exception(f"無法生成回應: {str(e)}")

    async def analyze_sentiment(self, text: str) -> Dict[str, Any]:
        """分析文本情感"""
        try:
            prompt = f"""請分析以下文本的情感，並以 JSON 格式回傳結果：

文本：{text}

請依照以下格式回傳（請只回傳 JSON，不要加入其他文字）：
{{
    "score": <數字，介於-1到1之間，精確到小數點後一位>,
    "label": "<情感標籤：正面、負面或中性>",
    "explanation": "<簡短說明分析結果的理由>"
}}"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            # 解析回應
            try:
                result = json.loads(response.choices[0].message.content)
                return {
                    "text": text,
                    "sentiment_score": float(result["score"]),
                    "sentiment_label": result["label"],
                    "explanation": result["explanation"]
                }
            except json.JSONDecodeError:
                # 如果 JSON 解析失敗，嘗試使用正則表達式提取分數
                content = response.choices[0].message.content
                score_match = re.search(r'-?\d+\.?\d*', content)
                if score_match:
                    score = float(score_match.group())
                    return {
                        "text": text,
                        "sentiment_score": score,
                        "sentiment_label": "正面" if score > 0 else "負面" if score < 0 else "中性",
                        "explanation": "無法解析詳細說明"
                    }
                else:
                    raise ValueError("無法解析情感分析結果")
            
        except Exception as e:
            logger.error(f"情感分析時發生錯誤: {str(e)}")
            raise Exception(f"無法進行情感分析: {str(e)}")

    async def detect_intent(self, text: str) -> Dict[str, str]:
        """檢測用戶意圖"""
        try:
            prompt = f"""請分析以下客服對話信息並以 JSON 格式回傳結果：

文本：{text}

請依照以下格式回傳（請只回傳 JSON，不要加入其他文字）：
{{
    "intent": "<意圖分類：提問、投訴、反饋、請求、問候、其他>",
    "confidence": <信心分數，介於0到1之間>,
    "explanation": "<簡短說明分類理由>"
}}"""
            
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[{"role": "user", "content": prompt}],
                temperature=0.3
            )
            
            try:
                result = json.loads(response.choices[0].message.content)
                return result
            except json.JSONDecodeError:
                raise ValueError("無法解析意圖分析結果")
            
        except Exception as e:
            logger.error(f"意圖檢測時發生錯誤: {str(e)}")
            raise Exception(f"無法檢測意圖: {str(e)}")

# Create LLM engine instance
llm_engine = LLMEngine()