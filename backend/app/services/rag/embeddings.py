from functools import lru_cache

from sentence_transformers import SentenceTransformer

from app.core.config import get_settings


class EmbeddingService:
    """本地 Embedding 服务，使用 sentence-transformers"""

    def __init__(self, model_name: str):
        self.model = SentenceTransformer(model_name)

    def embed(self, texts: list[str]) -> list[list[float]]:
        """生成文本的向量表示"""
        embeddings = self.model.encode(texts, convert_to_numpy=True)
        return embeddings.tolist()

    def embed_query(self, query: str) -> list[float]:
        """生成查询的向量表示"""
        embedding = self.model.encode(query, convert_to_numpy=True)
        return embedding.tolist()


@lru_cache
def get_embedding_service() -> EmbeddingService:
    settings = get_settings()
    return EmbeddingService(model_name=settings.embedding_model)
