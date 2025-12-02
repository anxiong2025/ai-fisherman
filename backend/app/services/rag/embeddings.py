from abc import ABC, abstractmethod
from functools import lru_cache

import google.generativeai as genai

from app.core.config import get_settings


class EmbeddingService(ABC):
    """Embedding 服务基类"""

    @abstractmethod
    def embed(self, texts: list[str]) -> list[list[float]]:
        """生成文本的向量表示"""
        pass

    @abstractmethod
    def embed_query(self, query: str) -> list[float]:
        """生成查询的向量表示"""
        pass


class GeminiEmbeddingService(EmbeddingService):
    """Gemini Embedding 服务"""

    def __init__(self, api_key: str, model_name: str = "text-embedding-004"):
        genai.configure(api_key=api_key)
        self.model_name = f"models/{model_name}"

    def embed(self, texts: list[str]) -> list[list[float]]:
        result = genai.embed_content(
            model=self.model_name,
            content=texts,
            task_type="retrieval_document",
        )
        return result["embedding"]

    def embed_query(self, query: str) -> list[float]:
        result = genai.embed_content(
            model=self.model_name,
            content=query,
            task_type="retrieval_query",
        )
        return result["embedding"]


class LocalEmbeddingService(EmbeddingService):
    """本地 Embedding 服务，使用 sentence-transformers"""

    def __init__(self, model_name: str):
        from sentence_transformers import SentenceTransformer

        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding.tolist()


@lru_cache
def get_embedding_service() -> EmbeddingService:
    settings = get_settings()
    if settings.embedding_provider == "local":
        return LocalEmbeddingService(model_name=settings.embedding_model)
    else:  # gemini
        return GeminiEmbeddingService(api_key=settings.gemini_api_key)
