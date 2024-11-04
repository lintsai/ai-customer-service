"use client";

import dynamic from 'next/dynamic';
import React, { useState, useRef, useLayoutEffect } from 'react';
import { Send, Loader, Bot, User, AlertCircle, Dog } from 'lucide-react';

interface Message {
  role: 'user' | 'assistant' | 'error';
  content: string;
  timestamp?: string;
  isSpecialKnowledge?: boolean;
}

interface ChatResponse {
  response: string;
}

interface ConversationResponse {
  conversation_id: string;
}

const ChatComponent: React.FC = () => {
  const [mounted, setMounted] = useState(false);
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const [conversationId, setConversationId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [isSpecialMode, setIsSpecialMode] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useLayoutEffect(() => {
    setMounted(true);
    return () => setMounted(false);
  }, []);

  const scrollToBottom = () => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  useLayoutEffect(() => {
    if (mounted) {
      scrollToBottom();
    }
  }, [messages, mounted]);

  const createConversation = async () => {
    if (!mounted) return;
    
    try {
      setError(null);
      const response = await fetch('http://localhost:8000/api/v1/chat/conversations', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_id: 'test_user'
        })
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ConversationResponse = await response.json();
      setConversationId(data.conversation_id);
      
      const welcomeMessage = isSpecialMode 
        ? '您好！我是特定知識助手。我可以回答關於西遊記、三國志、西廂記、勇者鬥惡龍和紅樓夢的問題。請問您想了解什麼？'
        : '您好！我是 AI 客服助理。請問有什麼可以協助您的嗎？';
        
      setMessages([{
        role: 'assistant',
        content: welcomeMessage,
        isSpecialKnowledge: isSpecialMode
      }]);
    } catch (error) {
      console.error('Error creating conversation:', error);
      setError('無法建立對話，請重新整理頁面試試。');
    }
  };

  const sendMessage = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || loading || !mounted) return;

    const userMessage = input.trim();
    setInput('');
    setLoading(true);
    setError(null);

    setMessages(prev => [...prev, { 
      role: 'user', 
      content: userMessage,
      isSpecialKnowledge: isSpecialMode
    }]);

    try {
      const endpoint = isSpecialMode
        ? 'http://localhost:8000/api/v1/knowledge/special-knowledge'
        : `http://localhost:8000/api/v1/chat/conversations/${conversationId}/messages`;

      // 在 sendMessage 函數中
      const body = isSpecialMode
      ? {
          messages: messages.map(msg => ({
            role: msg.role,
            content: msg.content
          })).concat([{
            role: "user",
            content: userMessage
          }])
        }
      : { content: userMessage };

      if (!isSpecialMode && !conversationId) {
        await createConversation();
      }

      const response = await fetch(endpoint, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify(body)
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }

      const data: ChatResponse = await response.json();
      setMessages(prev => [...prev, { 
        role: 'assistant', 
        content: data.response,
        isSpecialKnowledge: isSpecialMode
      }]);
    } catch (error) {
      console.error('Error sending message:', error);
      setMessages(prev => [...prev, {
        role: 'error',
        content: '抱歉，發生錯誤。請稍後再試。'
      }]);
      setError('發送消息時發生錯誤，請重試。');
    } finally {
      setLoading(false);
    }
  };

  useLayoutEffect(() => {
    if (mounted && !conversationId && !isSpecialMode) {
      createConversation();
    }
  }, [mounted, conversationId, isSpecialMode]);

  const toggleMode = () => {
    setIsSpecialMode(!isSpecialMode);
    setMessages([]);
    setConversationId(null);
    if (!isSpecialMode) {
      setMessages([{
        role: 'assistant',
        content: '您好！我是特定知識助手。我可以回答關於西遊記、三國志、西廂記、勇者鬥惡龍和紅樓夢的問題。請問您想了解什麼？',
        isSpecialKnowledge: true
      }]);
    }
  };

  if (!mounted) {
    return (
      <div className="flex items-center justify-center min-h-screen">
        <Loader className="w-8 h-8 animate-spin text-blue-500" />
      </div>
    );
  }

  return (
    <div className="flex flex-col h-screen max-w-2xl mx-auto p-4">
      <div className="flex items-center justify-between mb-4">
        <div className="text-xl font-bold text-center text-gray-800 flex-1">
          {isSpecialMode ? '特定知識助手' : 'AI 智慧客服'}
        </div>
        <button
          onClick={toggleMode}
          className={`px-4 py-2 rounded-lg flex items-center gap-2 transition-colors ${
            isSpecialMode 
              ? 'bg-orange-500 text-white hover:bg-orange-600' 
              : 'bg-blue-500 text-white hover:bg-blue-600'
          }`}
        >
          <Dog className="w-4 h-4" />
          {isSpecialMode ? '切換至一般模式' : '切換至特定模式'}
        </button>
      </div>
      
      {error && (
        <div className="mb-4 p-3 bg-red-50 border border-red-200 rounded-lg flex items-center gap-2 text-red-600">
          <AlertCircle className="w-5 h-5" />
          <span>{error}</span>
        </div>
      )}
      
      <div className="flex-1 overflow-y-auto mb-4 p-4 bg-gray-50 rounded-lg">
        {messages.map((message, index) => (
          <div
            key={index}
            className={`flex items-start gap-2 mb-4 ${
              message.role === 'user' ? 'justify-end' : 'justify-start'
            }`}
          >
            {message.role === 'assistant' && (
              <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
                message.isSpecialKnowledge ? 'bg-orange-500' : 'bg-blue-500'
              }`}>
                <Bot className="w-5 h-5 text-white" />
              </div>
            )}
            <div
              className={`max-w-[80%] rounded-lg p-3 ${
                message.role === 'user'
                  ? `${isSpecialMode ? 'bg-orange-500' : 'bg-blue-500'} text-white`
                  : message.role === 'error'
                  ? 'bg-red-50 text-red-600 border border-red-200'
                  : 'bg-white shadow-sm'
              }`}
            >
              {message.content}
            </div>
            {message.role === 'user' && (
              <div className="w-8 h-8 rounded-full bg-gray-300 flex items-center justify-center">
                <User className="w-5 h-5 text-gray-600" />
              </div>
            )}
          </div>
        ))}
        {loading && (
          <div className="flex items-center justify-start gap-2 mb-4">
            <div className={`w-8 h-8 rounded-full flex items-center justify-center ${
              isSpecialMode ? 'bg-orange-500' : 'bg-blue-500'
            }`}>
              <Bot className="w-5 h-5 text-white" />
            </div>
            <div className="bg-white rounded-lg p-3 shadow-sm">
              <Loader className="w-5 h-5 animate-spin" />
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      <form onSubmit={sendMessage} className="flex gap-2">
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder={isSpecialMode ? "請輸入特定知識相關問題..." : "輸入您的問題..."}
          className="flex-1 p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className={`px-4 py-2 rounded-lg hover:opacity-90 disabled:bg-gray-400 disabled:cursor-not-allowed transition-colors ${
            isSpecialMode ? 'bg-orange-500' : 'bg-blue-500'
          } text-white`}
        >
          <Send className="w-5 h-5" />
        </button>
      </form>

      <div className="mt-2 text-center text-xs text-gray-500">
        Version 1.0.0
      </div>
    </div>
  );
};

const Chat = dynamic(() => Promise.resolve(ChatComponent), {
  ssr: false,
});

export default Chat;