from functools import lru_cache
from pathlib import Path
from typing import Any

import chromadb

from app.core.config import get_settings
from app.services.rag.embeddings import get_embedding_service


class VectorStore:
    """ChromaDB 向量存储服务"""

    COLLECTION_NAME = "site_content"

    def __init__(self, persist_dir: str):
        # 确保目录存在
        Path(persist_dir).mkdir(parents=True, exist_ok=True)
        self.client = chromadb.PersistentClient(path=persist_dir)
        self.embedding_service = get_embedding_service()
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def add_documents(
        self,
        documents: list[str],
        metadatas: list[dict[str, Any]],
        ids: list[str],
    ) -> None:
        """添加文档到向量存储"""
        embeddings = self.embedding_service.embed(documents)
        self.collection.add(
            documents=documents,
            embeddings=embeddings,
            metadatas=metadatas,
            ids=ids,
        )

    def search(self, query: str, limit: int = 5) -> list[dict[str, Any]]:
        """搜索相似文档"""
        query_embedding = self.embedding_service.embed_query(query)

        results = self.collection.query(
            query_embeddings=[query_embedding],
            n_results=limit,
            include=["documents", "metadatas", "distances"],
        )

        if not results["documents"] or not results["documents"][0]:
            return []

        search_results = []
        for i, doc in enumerate(results["documents"][0]):
            metadata = results["metadatas"][0][i] if results["metadatas"] else {}
            distance = results["distances"][0][i] if results["distances"] else 0
            # Convert distance to similarity score (cosine distance -> similarity)
            score = 1 - distance

            search_results.append(
                {
                    "content": doc,
                    "title": metadata.get("title", ""),
                    "url": metadata.get("url", ""),
                    "score": score,
                }
            )

        return search_results

    def delete_all(self) -> None:
        """清空所有文档"""
        self.client.delete_collection(self.COLLECTION_NAME)
        self.collection = self.client.get_or_create_collection(
            name=self.COLLECTION_NAME,
            metadata={"hnsw:space": "cosine"},
        )

    def count(self) -> int:
        """返回文档数量"""
        return self.collection.count()


@lru_cache
def get_vector_store() -> VectorStore:
    settings = get_settings()
    return VectorStore(persist_dir=settings.chroma_persist_dir)
