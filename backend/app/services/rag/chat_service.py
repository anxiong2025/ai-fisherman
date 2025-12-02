import json
from collections.abc import AsyncGenerator
from functools import lru_cache
from typing import Any

import google.generativeai as genai
from anthropic import AsyncAnthropic
from openai import AsyncOpenAI

from app.core.config import get_settings
from app.schemas.chat import ChatMessage
from app.services.rag.vector_store import get_vector_store

SYSTEM_PROMPT = """你是一个网站内容检索助手。你的任务是基于提供的网站内容回答用户的问题。

规则：
1. 只基于提供的上下文内容回答问题
2. 如果上下文中没有相关信息，请诚实地说不知道
3. 回答要简洁、准确
4. 如果引用了具体内容，请注明来源

上下文内容：
{context}
"""


class ChatService:
    """RAG 聊天服务"""

    def __init__(self):
        self.settings = get_settings()
        self.vector_store = get_vector_store()

        if self.settings.llm_provider == "openai":
            self.openai_client = AsyncOpenAI(
                api_key=self.settings.openai_api_key,
                base_url=self.settings.openai_base_url,
            )
        elif self.settings.llm_provider == "anthropic":
            self.anthropic_client = AsyncAnthropic(
                api_key=self.settings.anthropic_api_key,
            )
        elif self.settings.llm_provider == "gemini":
            genai.configure(api_key=self.settings.gemini_api_key)
            self.gemini_model = genai.GenerativeModel(self.settings.gemini_model)

    def _build_context(self, search_results: list[dict[str, Any]]) -> str:
        """构建上下文"""
        if not search_results:
            return "没有找到相关内容。"

        context_parts = []
        for i, result in enumerate(search_results, 1):
            context_parts.append(
                f"[来源 {i}] {result['title']}\n"
                f"URL: {result['url']}\n"
                f"内容: {result['content']}\n"
            )
        return "\n---\n".join(context_parts)

    async def chat(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> tuple[str, list[dict]]:
        """执行 RAG 聊天"""
        # 1. 检索相关内容
        search_results = self.vector_store.search(query=message, limit=3)

        # 2. 构建上下文
        context = self._build_context(search_results)
        system_prompt = SYSTEM_PROMPT.format(context=context)

        # 3. 构建消息
        messages = [{"role": m.role, "content": m.content} for m in history]
        messages.append({"role": "user", "content": message})

        # 4. 调用 LLM
        if self.settings.llm_provider == "openai":
            response = await self._chat_openai(system_prompt, messages)
        elif self.settings.llm_provider == "anthropic":
            response = await self._chat_anthropic(system_prompt, messages)
        else:  # gemini
            response = await self._chat_gemini(system_prompt, messages)

        # 5. 返回结果和来源
        sources = [
            {"title": r["title"], "url": r["url"], "score": r["score"]}
            for r in search_results
        ]
        return response, sources

    async def _chat_openai(self, system_prompt: str, messages: list[dict]) -> str:
        """OpenAI 聊天"""
        response = await self.openai_client.chat.completions.create(
            model=self.settings.openai_model,
            messages=[{"role": "system", "content": system_prompt}, *messages],
            temperature=0.7,
            max_tokens=1000,
        )
        return response.choices[0].message.content or ""

    async def _chat_anthropic(self, system_prompt: str, messages: list[dict]) -> str:
        """Anthropic 聊天"""
        response = await self.anthropic_client.messages.create(
            model=self.settings.anthropic_model,
            system=system_prompt,
            messages=messages,
            max_tokens=1000,
        )
        return response.content[0].text

    async def _chat_gemini(self, system_prompt: str, messages: list[dict]) -> str:
        """Gemini 聊天"""
        # 构建 Gemini 格式的对话历史
        gemini_history = []
        for msg in messages[:-1]:  # 除了最后一条消息
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        # 创建带历史的聊天
        chat = self.gemini_model.start_chat(history=gemini_history)

        # 构建包含系统提示的用户消息
        user_message = messages[-1]["content"]
        full_message = f"{system_prompt}\n\n用户问题：{user_message}"

        # 发送消息并获取响应
        response = await chat.send_message_async(full_message)
        return response.text

    async def chat_stream(
        self,
        message: str,
        history: list[ChatMessage],
    ) -> AsyncGenerator[str, None]:
        """流式 RAG 聊天"""
        # 1. 检索相关内容
        search_results = self.vector_store.search(query=message, limit=3)

        # 2. 构建上下文
        context = self._build_context(search_results)
        system_prompt = SYSTEM_PROMPT.format(context=context)

        # 3. 构建消息
        messages = [{"role": m.role, "content": m.content} for m in history]
        messages.append({"role": "user", "content": message})

        # 4. 发送来源信息
        sources = [
            {"title": r["title"], "url": r["url"], "score": r["score"]}
            for r in search_results
        ]
        yield f"data: {json.dumps({'type': 'sources', 'data': sources})}\n\n"

        # 5. 流式调用 LLM
        if self.settings.llm_provider == "openai":
            async for chunk in self._stream_openai(system_prompt, messages):
                yield f"data: {json.dumps({'type': 'content', 'data': chunk})}\n\n"
        elif self.settings.llm_provider == "anthropic":
            async for chunk in self._stream_anthropic(system_prompt, messages):
                yield f"data: {json.dumps({'type': 'content', 'data': chunk})}\n\n"
        else:  # gemini
            async for chunk in self._stream_gemini(system_prompt, messages):
                yield f"data: {json.dumps({'type': 'content', 'data': chunk})}\n\n"

        yield "data: [DONE]\n\n"

    async def _stream_openai(
        self, system_prompt: str, messages: list[dict]
    ) -> AsyncGenerator[str, None]:
        """OpenAI 流式输出"""
        stream = await self.openai_client.chat.completions.create(
            model=self.settings.openai_model,
            messages=[{"role": "system", "content": system_prompt}, *messages],
            temperature=0.7,
            max_tokens=1000,
            stream=True,
        )
        async for chunk in stream:
            if chunk.choices[0].delta.content:
                yield chunk.choices[0].delta.content

    async def _stream_anthropic(
        self, system_prompt: str, messages: list[dict]
    ) -> AsyncGenerator[str, None]:
        """Anthropic 流式输出"""
        async with self.anthropic_client.messages.stream(
            model=self.settings.anthropic_model,
            system=system_prompt,
            messages=messages,
            max_tokens=1000,
        ) as stream:
            async for text in stream.text_stream:
                yield text

    async def _stream_gemini(
        self, system_prompt: str, messages: list[dict]
    ) -> AsyncGenerator[str, None]:
        """Gemini 流式输出"""
        # 构建 Gemini 格式的对话历史
        gemini_history = []
        for msg in messages[:-1]:
            role = "user" if msg["role"] == "user" else "model"
            gemini_history.append({"role": role, "parts": [msg["content"]]})

        # 创建带历史的聊天
        chat = self.gemini_model.start_chat(history=gemini_history)

        # 构建包含系统提示的用户消息
        user_message = messages[-1]["content"]
        full_message = f"{system_prompt}\n\n用户问题：{user_message}"

        # 流式发送消息
        response = await chat.send_message_async(full_message, stream=True)
        async for chunk in response:
            if chunk.text:
                yield chunk.text


@lru_cache
def get_chat_service() -> ChatService:
    return ChatService()
