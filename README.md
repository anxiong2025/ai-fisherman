# AI Fisherman

![Preview](frontend/src/assets/images/preview.gif)

## 核心亮点

**RAG 智能问答** - 基于 ChromaDB 向量数据库 + Embedding 模型实现语义检索，支持 OpenAI / Anthropic / Gemini 多 LLM 流式对话

**3D 粒子特效** - Three.js 实现黄金螺旋数学可视化背景

**OAuth 登录** - GitHub / Google 一键登录

## 技术架构

### 前端
- Vue 3.5 + TypeScript 5.9 + Vite 7
- Tailwind CSS 4 + shadcn-vue
- Three.js 0.181 3D 渲染
- Pinia 3 状态管理 + vue-i18n 9 国际化

### 后端
- Python 3.12+ + FastAPI 0.115 + SQLAlchemy 2.0 + SQLite
- ChromaDB 0.5 向量数据库
- Sentence-Transformers 3.3 / Gemini Embedding
- 多 LLM 支持 (OpenAI / Anthropic / Gemini)

## 快速启动

### 后端

需要先安装 [uv](https://docs.astral.sh/uv/) 包管理工具:

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

然后启动后端:

```bash
cd backend
uv sync                       # 安装依赖并创建虚拟环境
cp .env.example .env          # 配置 API Key
source .venv/bin/activate     # 激活虚拟环境
uvicorn app.main:app --reload --port 8000
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
