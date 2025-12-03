# AI Fisherman

![Preview](./preview.png)

## 核心亮点

**RAG 智能问答** - 基于 ChromaDB 向量数据库 + Embedding 模型实现语义检索，支持 OpenAI / Anthropic / Gemini 多 LLM 流式对话

**3D 粒子特效** - Three.js 实现黄金螺旋数学可视化背景

**OAuth 登录** - GitHub / Google 一键登录

## 技术架构

### 前端
- Vue 3.5 + TypeScript 5.9 + Vite 7
- Tailwind CSS 4 + shadcn-vue
- Three.js 3D 渲染
- Pinia 状态管理 + vue-i18n 国际化

### 后端
- FastAPI + SQLAlchemy 2.0 + SQLite
- ChromaDB 向量数据库
- Sentence-Transformers / Gemini Embedding
- 多 LLM 支持 (OpenAI / Anthropic / Gemini)

## 快速启动

### 后端

```bash
cd backend
uv sync
cp .env.example .env  # 配置 API Key
uv run uvicorn app.main:app --reload --port 8000
```

### 前端

```bash
cd vue-app
npm install
npm run dev
```

访问 http://localhost:3000

## RAG 实现原理

```
用户提问 → Embedding 向量化 → ChromaDB 语义检索 → 构建上下文 → LLM 生成回答
```

1. **索引阶段**: 文章内容通过 Embedding 模型转为向量，存入 ChromaDB
2. **检索阶段**: 用户问题向量化后，检索最相似的 Top-K 文档
3. **生成阶段**: 检索结果作为上下文，LLM 基于上下文生成回答

## License

MIT
