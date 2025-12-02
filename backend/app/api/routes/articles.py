import json
import uuid
from datetime import datetime, timezone
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.core.database import get_db
from app.core.deps import get_admin_user, get_current_user_optional
from app.models import Article, User
from app.schemas.article import (
    ArticleBriefResponse,
    ArticleCreate,
    ArticleListResponse,
    ArticleResponse,
    ArticleUpdate,
)

router = APIRouter()


def _calculate_read_time(content: str) -> int:
    """Calculate read time in minutes based on content length."""
    words = len(content.split())
    return max(1, words // 200)  # ~200 words per minute


# ============== Public Endpoints ==============


@router.get("", response_model=ArticleListResponse)
async def list_articles(
    db: Annotated[AsyncSession, Depends(get_db)],
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=50),
    category: str | None = None,
    tag: str | None = None,
    status: str | None = None,
    current_user: Annotated[User | None, Depends(get_current_user_optional)] = None,
) -> ArticleListResponse:
    """List articles with pagination and filtering."""
    query = select(Article).options(selectinload(Article.author))

    # Non-admin users can only see published articles
    if not current_user or current_user.role != "admin":
        query = query.where(Article.status == "published")
    elif status:
        query = query.where(Article.status == status)

    if category:
        query = query.where(Article.category == category)

    if tag:
        query = query.where(Article.tags.contains(f'"{tag}"'))

    # Count total
    count_query = select(func.count()).select_from(query.subquery())
    total_result = await db.execute(count_query)
    total = total_result.scalar() or 0

    # Paginate
    query = query.order_by(Article.created_at.desc())
    query = query.offset((page - 1) * page_size).limit(page_size)

    result = await db.execute(query)
    articles = result.scalars().all()

    return ArticleListResponse(
        items=[ArticleResponse.model_validate(a) for a in articles],
        total=total,
        page=page,
        page_size=page_size,
    )


@router.get("/{slug}", response_model=ArticleResponse)
async def get_article(
    slug: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User | None, Depends(get_current_user_optional)] = None,
) -> ArticleResponse:
    """Get article by slug."""
    query = (
        select(Article)
        .options(selectinload(Article.author))
        .where(Article.slug == slug)
    )

    # Non-admin users can only see published articles
    if not current_user or current_user.role != "admin":
        query = query.where(Article.status == "published")

    result = await db.execute(query)
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    return ArticleResponse.model_validate(article)


# ============== Admin Endpoints ==============


@router.post("", response_model=ArticleResponse, status_code=status.HTTP_201_CREATED)
async def create_article(
    data: ArticleCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> ArticleResponse:
    """Create a new article (admin only)."""
    # Check slug uniqueness
    existing = await db.execute(select(Article).where(Article.slug == data.slug))
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Article with this slug already exists",
        )

    article = Article(
        id=str(uuid.uuid4()),
        slug=data.slug,
        title=data.title,
        excerpt=data.excerpt,
        content=data.content,
        category=data.category,
        tags=json.dumps(data.tags),
        status=data.status,
        gradient=data.gradient,
        read_time=_calculate_read_time(data.content),
        author_id=current_user.id,
        published_at=datetime.now(timezone.utc) if data.status == "published" else None,
    )

    db.add(article)
    await db.flush()
    await db.refresh(article, ["author"])

    return ArticleResponse.model_validate(article)


@router.put("/{article_id}", response_model=ArticleResponse)
async def update_article(
    article_id: str,
    data: ArticleUpdate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> ArticleResponse:
    """Update an article (admin only)."""
    result = await db.execute(
        select(Article)
        .options(selectinload(Article.author))
        .where(Article.id == article_id)
    )
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    # Check slug uniqueness if changing
    if data.slug and data.slug != article.slug:
        existing = await db.execute(select(Article).where(Article.slug == data.slug))
        if existing.scalar_one_or_none():
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Article with this slug already exists",
            )

    # Update fields
    update_data = data.model_dump(exclude_unset=True)

    if "tags" in update_data:
        update_data["tags"] = json.dumps(update_data["tags"])

    if "content" in update_data:
        update_data["read_time"] = _calculate_read_time(update_data["content"])

    # Handle publishing
    if data.status == "published" and article.status != "published":
        update_data["published_at"] = datetime.now(timezone.utc)

    for key, value in update_data.items():
        setattr(article, key, value)

    await db.flush()
    await db.refresh(article, ["author"])

    return ArticleResponse.model_validate(article)


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_article(
    article_id: str,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[User, Depends(get_admin_user)],
) -> None:
    """Delete an article (admin only)."""
    result = await db.execute(select(Article).where(Article.id == article_id))
    article = result.scalar_one_or_none()

    if not article:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Article not found",
        )

    await db.delete(article)
