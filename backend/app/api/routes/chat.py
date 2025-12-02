from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse

from app.schemas.chat import ChatRequest, ChatResponse
from app.services.rag.chat_service import ChatService, get_chat_service

router = APIRouter()


@router.post("", response_model=ChatResponse)
async def chat(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> ChatResponse:
    """基于 RAG 的聊天接口"""
    response, sources = await chat_service.chat(
        message=request.message,
        history=request.history,
    )

    return ChatResponse(response=response, sources=sources)


@router.post("/stream")
async def chat_stream(
    request: ChatRequest,
    chat_service: ChatService = Depends(get_chat_service),
) -> StreamingResponse:
    """流式聊天接口"""
    return StreamingResponse(
        chat_service.chat_stream(message=request.message, history=request.history),
        media_type="text/event-stream",
    )
