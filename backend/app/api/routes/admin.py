from pathlib import Path

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.core.config import get_settings
from app.services.rag.indexer import ContentIndexer
from app.services.rag.vector_store import get_vector_store

router = APIRouter()


class IndexRequest(BaseModel):
    directory: str | None = None
    base_url: str = ""


class IndexResponse(BaseModel):
    files: int
    chunks: int
    message: str


class StatsResponse(BaseModel):
    total_documents: int


@router.post("/index", response_model=IndexResponse)
async def index_content(request: IndexRequest) -> IndexResponse:
    """索引网站内容"""
    settings = get_settings()

    directory = Path(request.directory) if request.directory else Path(settings.content_dir)

    if not directory.exists():
        raise HTTPException(status_code=400, detail=f"目录不存在: {directory}")

    indexer = ContentIndexer()
    stats = indexer.index_directory(directory, request.base_url)

    return IndexResponse(
        files=stats["files"],
        chunks=stats["chunks"],
        message=f"成功索引 {stats['files']} 个文件，共 {stats['chunks']} 个文档块",
    )


@router.post("/reindex", response_model=IndexResponse)
async def reindex_content(request: IndexRequest) -> IndexResponse:
    """重新索引所有内容（清空后重建）"""
    settings = get_settings()

    directory = Path(request.directory) if request.directory else Path(settings.content_dir)

    if not directory.exists():
        raise HTTPException(status_code=400, detail=f"目录不存在: {directory}")

    indexer = ContentIndexer()
    stats = indexer.reindex_all(directory, request.base_url)

    return IndexResponse(
        files=stats["files"],
        chunks=stats["chunks"],
        message=f"重新索引完成：{stats['files']} 个文件，{stats['chunks']} 个文档块",
    )


@router.get("/stats", response_model=StatsResponse)
async def get_stats() -> StatsResponse:
    """获取索引统计信息"""
    vector_store = get_vector_store()
    return StatsResponse(total_documents=vector_store.count())
