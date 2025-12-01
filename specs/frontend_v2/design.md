# 技术方案设计

## 1. 架构概述

本项目为静态网站（HTML/CSS/JS），将通过引入 **腾讯云开发 (CloudBase) Web SDK** 来赋予动态能力。

*   **前端框架**：原生 HTML/JS (保持现有架构，不引入 Vue/React 以降低复杂度)。
*   **后端服务**：CloudBase 云函数 (用于支付、AI 对话等敏感逻辑，本次暂不涉及复杂后端，主要利用 SDK 直接访问数据库)。
*   **数据库**：CloudBase NoSQL 数据库。
*   **存储**：CloudBase 云存储 (用于文章封面图等)。
*   **认证**：CloudBase Auth (GitHub/Google 登录)。

## 2. 详细设计

### 2.1 用户登录 (Auth)

*   **SDK 集成**：在 `index.html` 及所有页面引入 `cloudbase-js-sdk`。
*   **登录流程**：
    1.  用户点击导航栏"登录"。
    2.  调用 `auth.signInWithProvider('github')` 或 `google`。
    3.  登录成功后，SDK 自动持久化登录态。
    4.  页面加载时检查 `auth.getCurrentUser()`，若存在则显示头像/昵称，隐藏登录按钮。
*   **UI 变更**：
    *   修改 `nav` 区域，增加登录/用户信息组件。

### 2.2 数据库设计 (Database)

需要创建以下集合 (Collections)：

#### `articles` (文章)
| 字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `_id` | String | 自动生成 |
| `title` | String | 标题 |
| `content` | String | Markdown 内容 |
| `coverUrl` | String | 封面图 URL |
| `category` | String | 分类 |
| `tags` | Array | 标签列表 |
| `createdAt` | Date | 创建时间 |
| `updatedAt` | Date | 更新时间 |
| `authorId` | String | 作者 OpenID |

#### `courses` (课程)
| 字段 | 类型 | 描述 |
| :--- | :--- | :--- |
| `_id` | String | 自动生成 |
| `title` | String | 标题 |
| `description` | String | 描述 |
| `price` | Number | 价格 (分) |
| `status` | String | 状态 (active/inactive) |

### 2.3 后台管理 (Admin)

*   **入口**：`/admin.html` (新建页面)。
*   **权限控制**：页面加载时检查 `auth.currentUser`。为了简单起见，前端硬编码管理员 UID 列表 (或在数据库 `users` 表中标记 role)，非管理员跳转回首页。
*   **功能模块**：
    *   **文章发布**：
        *   左侧输入框：标题、分类、标签。
        *   中间文本域：Markdown 源码输入。
        *   右侧预览：实时渲染 HTML。
        *   提交按钮：调用 `db.collection('articles').add()`。
    *   **课程管理**：
        *   列表展示现有课程。
        *   简单的表单用于添加/编辑课程。

### 2.4 Markdown 渲染

*   **库选型**：`marked.js` (轻量、成熟)。
*   **代码高亮**：`highlight.js`。
*   **实现**：
    *   文章详情页 (`article.html`) 从 URL 参数获取文章 ID。
    *   调用 `db.collection('articles').doc(id).get()`。
    *   使用 `marked.parse(content)` 将 Markdown 转为 HTML 插入页面。

### 2.5 支付与 AI (预留)

*   **支付**：
    *   课程页 "立即购买" 按钮绑定点击事件。
    *   事件处理函数 `handlePurchase()` 中 `console.log('调用微信支付...')` 并弹出 `alert('支付功能开发中')`。
*   **AI 聊天**：
    *   右下角悬浮按钮 (FAB)。
    *   点击展开聊天框 (HTML/CSS 实现)。
    *   发送消息时，前端模拟回复："这是 AI 助手的模拟回复 (站内检索功能开发中)"。

## 3. 安全性

*   **数据库权限 (ACL)**：
    *   `articles`: `read: true` (所有人可读), `write: false` (仅管理员可写，需配置安全规则)。
    *   `courses`: 同上。
*   **前端验证**：虽然前端验证不可靠，但作为第一道防线，需检查登录态。

## 4. 依赖库

*   `cloudbase-js-sdk` (CDN 引入)
*   `marked` (CDN 引入)
*   `highlight.js` (CDN 引入)
