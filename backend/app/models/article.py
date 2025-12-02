from datetime import datetime
from enum import Enum

from sqlalchemy import DateTime, ForeignKey, Integer, String, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class ArticleStatus(str, Enum):
    DRAFT = "draft"
    PUBLISHED = "published"


class ArticleCategory(str, Enum):
    AI_NEWS = "ai-news"
    AGENTS = "agents"
    TUTORIAL = "tutorial"
    TOOLS = "tools"


class Article(Base):
    __tablename__ = "articles"

    id: Mapped[str] = mapped_column(String(36), primary_key=True)
    slug: Mapped[str] = mapped_column(String(200), unique=True, index=True)
    title: Mapped[str] = mapped_column(String(200))
    excerpt: Mapped[str] = mapped_column(Text)
    content: Mapped[str] = mapped_column(Text)
    category: Mapped[str] = mapped_column(String(50), default=ArticleCategory.TUTORIAL.value)
    tags: Mapped[str] = mapped_column(Text, default="")  # JSON string of tags
    status: Mapped[str] = mapped_column(String(20), default=ArticleStatus.DRAFT.value)
    read_time: Mapped[int] = mapped_column(Integer, default=5)
    gradient: Mapped[str] = mapped_column(
        String(200), default="linear-gradient(135deg, #667eea 0%, #764ba2 100%)"
    )

    # Foreign keys
    author_id: Mapped[str] = mapped_column(String(36), ForeignKey("users.id"))

    # Timestamps
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), onupdate=func.now()
    )
    published_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )

    # Relationships
    author: Mapped["User"] = relationship("User", back_populates="articles")  # noqa: F821

    def __repr__(self) -> str:
        return f"<Article {self.slug}>"
