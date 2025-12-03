export default {
  // Navigation
  nav: {
    home: '首页',
    articles: '文章',
    projects: '项目',
    skills: '技能',
    courses: '课程',
    about: '关于',
    admin: '管理',
    login: '登录',
    logout: '退出',
    loginWithGithub: 'GitHub 登录',
    loginWithGoogle: 'Google 登录'
  },

  // Home page
  home: {
    hero: {
      prefix: '跟',
      title: '渔夫',
      subtitle: '一起出海，驾驭 AI 浪潮！',
      description: '探索 AI 前沿技术，掌握 Agent 开发技能，成为 AI 时代的创造者',
      cta: '开始学习'
    },
    featured: {
      title: '精选文章',
      viewAll: '查看全部'
    },
    courses: {
      title: '热门课程',
      viewAll: '查看全部'
    },
    projects: {
      title: '开源项目',
      viewAll: '查看全部'
    }
  },

  // Articles
  articles: {
    title: '文章',
    subtitle: '探索 AI 前沿技术与实践经验',
    categories: {
      all: '全部',
      'ai-news': 'AI 资讯',
      agents: 'Agents 开发',
      tutorial: '技术教程',
      tools: '工具推荐'
    },
    readTime: '{time} 分钟阅读',
    loadMore: '加载更多',
    relatedArticles: '相关文章'
  },

  // Courses
  courses: {
    title: 'AI 培训课程',
    subtitle: '系统学习 AI 开发技能，从入门到精通',
    popular: '热门',
    new: '新课',
    overview: '课程简介',
    curriculum: '课程大纲',
    instructor: '讲师介绍',
    whatYouWillLearn: '你将学到',
    includes: '课程包含',
    videoHours: '{hours} 小时视频',
    projects: '{count} 个实战项目',
    certificate: '结业证书',
    lifetime: '永久访问',
    community: '社群答疑',
    price: '价格',
    originalPrice: '原价',
    discount: '省 {percent}%',
    enroll: '立即报名',
    guarantee: '7 天无理由退款保障',
    cta: {
      title: '准备好开始学习了吗？',
      subtitle: '加入 1000+ 学员，一起掌握 AI 时代的核心技能',
      button: '立即报名'
    }
  },

  // Projects
  projects: {
    title: '开源项目',
    subtitle: '探索 AI 项目，从源码中学习',
    stars: 'Stars',
    viewGithub: '查看 GitHub',
    liveDemo: '在线演示'
  },

  // Skills
  skills: {
    title: '技术栈',
    subtitle: '我在 AI、编程语言和现代开发工具方面的专业技能',
    experience: {
      title: '经验亮点',
      ai: {
        title: 'AI 与大模型开发',
        desc: '使用 Claude、GPT、Gemini 构建生产级 AI 应用。擅长 RAG、提示工程和 AI 智能体开发。'
      },
      backend: {
        title: '后端工程',
        desc: '使用 FastAPI、Rust 构建高性能 API。PostgreSQL 数据库设计，向量数据库应用。'
      },
      data: {
        title: '数据与机器学习',
        desc: '数据处理、向量嵌入生成、语义搜索和机器学习模型部署。'
      }
    }
  },

  // About
  about: {
    title: '关于我',
    subtitle: 'AI 开发者 & 教育者',
    intro: '我是 Robert，一名热衷于 AI 并致力于帮助他人学习的软件工程师。',
    experience: '工作经历',
    skills: '技能',
    contact: '联系方式',
    social: '社交媒体'
  },

  // Auth
  auth: {
    login: '登录',
    logout: '退出',
    loginRequired: '请先登录',
    loginSuccess: '登录成功',
    logoutSuccess: '已退出登录'
  },

  // Payment
  payment: {
    title: '完成支付',
    courseInfo: '课程信息',
    paymentMethod: '支付方式',
    wechat: '微信支付',
    alipay: '支付宝',
    scanToPay: '扫码支付',
    processing: '处理中...',
    success: '支付成功！',
    failed: '支付失败，请重试'
  },

  // AI Chat
  chat: {
    title: 'AI 助手',
    placeholder: '问我关于网站的任何问题...',
    send: '发送',
    clear: '清空',
    close: '关闭',
    thinking: '思考中...',
    welcome: '你好！我可以帮你查找文章、课程，或回答关于 AI 开发的问题。有什么想了解的吗？'
  },

  // Common
  common: {
    loading: '加载中...',
    error: '发生错误',
    retry: '重试',
    save: '保存',
    cancel: '取消',
    delete: '删除',
    edit: '编辑',
    create: '创建',
    search: '搜索',
    filter: '筛选',
    sort: '排序',
    viewMore: '查看更多',
    backToTop: '返回顶部',
    copyright: '© 2025 渔夫 AI. 保留所有权利。'
  },

  // Theme
  theme: {
    light: '浅色',
    dark: '深色',
    system: '跟随系统'
  },

  // Language
  language: {
    en: 'English',
    zh: '中文'
  },

  // Footer
  footer: {
    explore: '探索',
    learn: '学习',
    about: '关于',
    contact: '联系',
    allArticles: '全部文章',
    allCourses: '全部课程',
    openSource: '开源项目',
    email: '联系邮箱',
    cooperation: '合作咨询'
  },

  // Admin
  admin: {
    dashboard: '仪表盘',
    articles: '文章管理',
    courses: '课程管理',
    users: '用户管理',
    orders: '订单管理',
    settings: '设置',
    stats: {
      totalArticles: '文章总数',
      totalCourses: '课程总数',
      totalUsers: '用户总数',
      totalRevenue: '总收入'
    },
    articleEditor: {
      title: '文章编辑器',
      newArticle: '新建文章',
      editArticle: '编辑文章',
      titlePlaceholder: '输入文章标题',
      excerptPlaceholder: '输入文章摘要',
      contentPlaceholder: '使用 Markdown 编写文章...',
      preview: '预览',
      publish: '发布',
      saveDraft: '保存草稿'
    }
  }
}
