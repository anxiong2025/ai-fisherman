from fastapi import APIRouter, Depends

from app.schemas.search import SearchRequest, SearchResponse, SearchResult
from app.services.rag.vector_store import VectorStore, get_vector_store

router = APIRouter()


@router.post("", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    vector_store: VectorStore = Depends(get_vector_store),
) -> SearchResponse:
    """搜索站内内容"""
    results = vector_store.search(query=request.query, limit=request.limit)

    return SearchResponse(
        query=request.query,
        results=[
            SearchResult(
                title=r.get("title", ""),
                content=r.get("content", ""),
                url=r.get("url", ""),
                score=r.get("score", 0.0),
            )
            for r in results
        ],
    )
