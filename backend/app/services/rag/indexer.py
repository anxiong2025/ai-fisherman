import hashlib
from pathlib import Path
from typing import Any

from bs4 import BeautifulSoup

from app.services.rag.vector_store import VectorStore, get_vector_store


class ContentIndexer:
    """网站内容索引器"""

    def __init__(self, vector_store: VectorStore | None = None):
        self.vector_store = vector_store or get_vector_store()

    def _generate_id(self, content: str, url: str) -> str:
        """生成文档 ID"""
        return hashlib.md5(f"{url}:{content[:100]}".encode()).hexdigest()

    def _chunk_text(self, text: str, chunk_size: int = 500, overlap: int = 50) -> list[str]:
        """将文本分割成块"""
        if len(text) <= chunk_size:
            return [text]

        chunks = []
        start = 0
        while start < len(text):
            end = start + chunk_size
            chunk = text[start:end]
            chunks.append(chunk.strip())
            start = end - overlap

        return [c for c in chunks if c]

    def index_html_file(self, file_path: Path, base_url: str = "") -> int:
        """索引单个 HTML 文件"""
        with open(file_path, encoding="utf-8") as f:
            html_content = f.read()

        soup = BeautifulSoup(html_content, "lxml")

        # 提取标题
        title = ""
        if soup.title:
            title = soup.title.string or ""
        elif soup.find("h1"):
            title = soup.find("h1").get_text(strip=True)

        # 提取正文内容（移除脚本和样式）
        for script in soup(["script", "style", "nav", "footer", "header"]):
            script.decompose()

        # 尝试找主要内容区域
        main_content = soup.find("main") or soup.find("article") or soup.find("body")
        if main_content:
            text = main_content.get_text(separator="\n", strip=True)
        else:
            text = soup.get_text(separator="\n", strip=True)

        # 清理文本
        lines = [line.strip() for line in text.split("\n") if line.strip()]
        text = "\n".join(lines)

        if not text:
            return 0

        # 构建 URL
        url = base_url + "/" + file_path.name if base_url else file_path.name

        # 分块并索引
        chunks = self._chunk_text(text)

        documents = []
        metadatas: list[dict[str, Any]] = []
        ids = []

        for i, chunk in enumerate(chunks):
            doc_id = self._generate_id(chunk, f"{url}#{i}")
            documents.append(chunk)
            metadatas.append({"title": title, "url": url, "chunk_index": i})
            ids.append(doc_id)

        if documents:
            self.vector_store.add_documents(
                documents=documents,
                metadatas=metadatas,
                ids=ids,
            )

        return len(documents)

    def index_directory(self, directory: Path, base_url: str = "") -> dict[str, int]:
        """索引目录下的所有 HTML 文件"""
        stats = {"files": 0, "chunks": 0}

        html_files = list(directory.glob("**/*.html"))

        for html_file in html_files:
            chunks_count = self.index_html_file(html_file, base_url)
            stats["files"] += 1
            stats["chunks"] += chunks_count

        return stats

    def reindex_all(self, directory: Path, base_url: str = "") -> dict[str, int]:
        """重新索引所有内容"""
        self.vector_store.delete_all()
        return self.index_directory(directory, base_url)
