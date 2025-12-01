# 贡献指南 | Contributing Guide

感谢你考虑为 AI Fisherman 做出贡献！

Thank you for considering contributing to AI Fisherman!

## 🌍 语言 | Language

- 代码注释和 commit 信息请使用英文
- Issue 和 PR 描述可使用中文或英文

## 🚀 开发流程 | Development Workflow

### 1. Fork 仓库

点击右上角的 Fork 按钮，将仓库复制到你的账户下。

### 2. 克隆到本地

```bash
git clone https://github.com/your-username/ai-fisherman.git
cd ai-fisherman
```

### 3. 创建分支

```bash
git checkout -b feature/your-feature-name
# 或
git checkout -b fix/your-bug-fix
```

### 4. 安装依赖

```bash
cd vue-app
pnpm install
```

### 5. 开发

```bash
pnpm dev
```

### 6. 提交更改

```bash
git add .
git commit -m "feat: add new feature"
```

### 7. 推送并创建 PR

```bash
git push origin feature/your-feature-name
```

然后在 GitHub 上创建 Pull Request。

## 📝 Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/) 规范：

| 类型 | 说明 |
|------|------|
| `feat` | 新功能 |
| `fix` | Bug 修复 |
| `docs` | 文档更新 |
| `style` | 代码格式（不影响功能） |
| `refactor` | 重构 |
| `perf` | 性能优化 |
| `test` | 测试相关 |
| `chore` | 构建/工具相关 |

示例：
```
feat: add dark mode support
fix: resolve login redirect issue
docs: update README installation steps
```

## 🎨 代码规范

### Vue 组件

- 使用 `<script setup>` 语法
- 组件名使用 PascalCase
- Props 和 Emits 需要类型声明

```vue
<script setup lang="ts">
interface Props {
  title: string
  count?: number
}

const props = withDefaults(defineProps<Props>(), {
  count: 0
})

const emit = defineEmits<{
  update: [value: string]
}>()
</script>
```

### TypeScript

- 避免使用 `any`
- 为所有函数参数和返回值添加类型
- 使用 `interface` 而非 `type`（除非需要联合类型）

### CSS

- 使用 CSS 变量进行主题配置
- 遵循 BEM 命名规范
- 优先使用 `scoped` 样式

```css
/* Good */
.card__header {}
.card__header--active {}

/* Avoid */
.cardHeader {}
.card-header-active {}
```

## 🐛 报告 Bug

创建 Issue 时请包含：

1. **问题描述** - 清晰描述遇到的问题
2. **复现步骤** - 详细的复现步骤
3. **预期行为** - 你期望发生什么
4. **实际行为** - 实际发生了什么
5. **环境信息** - 浏览器、操作系统、Node 版本等
6. **截图** - 如果适用的话

## 💡 功能建议

欢迎提出新功能建议！创建 Issue 时请说明：

1. **功能描述** - 你想要什么功能
2. **使用场景** - 为什么需要这个功能
3. **可能的实现方式** - 如果有想法的话

## 📋 Pull Request 检查清单

- [ ] 代码符合项目规范
- [ ] 添加了必要的注释
- [ ] 更新了相关文档
- [ ] 本地测试通过
- [ ] Commit 信息符合规范

## 🙏 感谢

感谢所有贡献者让这个项目变得更好！

---

如有任何问题，欢迎在 Issue 中讨论。
