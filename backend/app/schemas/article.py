import json
from datetime import datetime

from pydantic import BaseModel, Field, field_validator

from app.schemas.auth import UserResponse


class ArticleCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    slug: str = Field(..., min_length=1, max_length=200)
    excerpt: str = Field(..., min_length=1)
    content: str = Field(..., min_length=1)
    category: str = Field(default="tutorial")
    tags: list[str] = Field(default_factory=list)
    status: str = Field(default="draft")
    gradient: str = Field(default="linear-gradient(135deg, #667eea 0%, #764ba2 100%)")


class ArticleUpdate(BaseModel):
    title: str | None = Field(None, min_length=1, max_length=200)
    slug: str | None = Field(None, min_length=1, max_length=200)
    excerpt: str | None = None
    content: str | None = None
    category: str | None = None
    tags: list[str] | None = None
    status: str | None = None
    gradient: str | None = None


class ArticleResponse(BaseModel):
    id: str
    slug: str
    title: str
    excerpt: str
    content: str
    category: str
    tags: list[str]
    status: str
    read_time: int
    gradient: str
    author: UserResponse
    created_at: datetime
    updated_at: datetime
    published_at: datetime | None

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            try:
                return json.loads(v) if v else []
            except json.JSONDecodeError:
                return []
        return v

    class Config:
        from_attributes = True


class ArticleListResponse(BaseModel):
    items: list[ArticleResponse]
    total: int
    page: int
    page_size: int


class ArticleBriefResponse(BaseModel):
    """Brief article info without content."""

    id: str
    slug: str
    title: str
    excerpt: str
    category: str
    tags: list[str]
    status: str
    read_time: int
    gradient: str
    author_name: str
    created_at: datetime
    published_at: datetime | None

    @field_validator("tags", mode="before")
    @classmethod
    def parse_tags(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            try:
                return json.loads(v) if v else []
            except json.JSONDecodeError:
                return []
        return v
