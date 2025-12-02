from pydantic import BaseModel, Field


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=500, description="搜索查询")
    limit: int = Field(default=5, ge=1, le=20, description="返回结果数量")


class SearchResult(BaseModel):
    title: str
    content: str
    url: str
    score: float


class SearchResponse(BaseModel):
    results: list[SearchResult]
    query: str
