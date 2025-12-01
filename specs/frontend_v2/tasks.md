# 实施计划

- [ ] 1. 环境与依赖配置
  - [ ] 1.1 在所有 HTML 页面引入 `cloudbase-js-sdk`, `marked.js`, `highlight.js` CDN 链接。
  - [ ] 1.2 在 `js/main.js` 中初始化 CloudBase App (使用 `env-placeholder`，待用户替换)。
  - _需求: 1, 3_

- [ ] 2. 用户登录功能
  - [ ] 2.1 修改 `index.html` 导航栏，添加登录按钮和用户信息容器。
  - [ ] 2.2 在 `js/main.js` 实现 `loginWithGithub()`, `loginWithGoogle()`, `logout()`。
  - [ ] 2.3 实现 `checkLoginState()`，页面加载时更新导航栏状态（显示头像/昵称）。
  - _需求: 1_

- [ ] 3. 后台管理页面 (Admin)
  - [ ] 3.1 创建 `admin.html`，包含文章发布表单和课程管理列表。
  - [ ] 3.2 实现权限检查：非管理员访问重定向回首页 (前端简单模拟)。
  - [ ] 3.3 实现文章发布逻辑：获取表单数据 -> 调用 `db.collection('articles').add()`。
  - [ ] 3.4 实现 Markdown 实时预览功能。
  - _需求: 2, 3_

- [ ] 4. 文章详情页改造
  - [ ] 4.1 创建/修改 `article.html`，支持通过 URL 参数 `?id=xxx` 加载文章。
  - [ ] 4.2 实现文章加载逻辑：`db.collection('articles').doc(id).get()`。
  - [ ] 4.3 使用 `marked.js` 渲染 Markdown 内容，并应用 `highlight.js` 高亮代码。
  - _需求: 3_

- [ ] 5. 支付与 AI 助手 (UI)
  - [ ] 5.1 在课程详情页添加"购买"按钮，点击弹出"功能开发中"提示。
  - [ ] 5.2 添加右下角悬浮 AI 聊天图标。
  - [ ] 5.3 实现聊天窗口的展开/收起及简单的消息发送 UI (不接真实 API)。
  - _需求: 4, 5_
