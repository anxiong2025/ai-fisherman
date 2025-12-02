from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    role: str = Field(..., pattern="^(user|assistant)$")
    content: str


class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=2000, description="用户消息")
    history: list[ChatMessage] = Field(default_factory=list, description="对话历史")


class ChatResponse(BaseModel):
    response: str
    sources: list[dict] = Field(default_factory=list, description="引用来源")
