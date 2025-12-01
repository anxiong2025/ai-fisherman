# 🎣 AI Fisherman

> A modern AI technology blog platform with Apple-style design

English | [中文](./README.md)

## ✨ Features

- 🎨 **Apple-style UI** - Clean, elegant design with smooth animations
- 🌍 **Internationalization** - Chinese/English bilingual support
- 🌙 **Dark Mode** - Light/Dark/System theme support
- 🔍 **Smart Search** - Vector-based content retrieval
- 🤖 **AI Assistant** - Integrated with Qwen AI for intelligent Q&A
- 📝 **Markdown Editor** - Article editing with live preview
- 🔐 **OAuth Login** - GitHub / Google quick login
- 💳 **Payment Integration** - WeChat Pay / Alipay
- 📱 **Responsive Design** - Perfect mobile adaptation

## 🖼️ Preview

![Home Preview](./images/preview-home.png)

## 🚀 Quick Start

### Requirements

- Node.js >= 18
- pnpm >= 8 (recommended) or npm >= 9

### Installation

```bash
# Clone the repository
git clone https://github.com/your-username/ai-fisherman.git
cd ai-fisherman

# Install frontend dependencies
cd vue-app
pnpm install

# Copy environment configuration
cp .env.example .env.local
```

### Development

```bash
# Start frontend dev server
pnpm dev
```

Visit http://localhost:5173

### Build

```bash
# Build for production
pnpm build

# Preview build
pnpm preview
```

## 📦 Tech Stack

### Frontend

| Technology | Version | Description |
|------------|---------|-------------|
| Vue | 3.5 | Progressive JavaScript Framework |
| TypeScript | 5.9 | Type Safety |
| Vite | 7.x | Next Generation Frontend Tooling |
| Vue Router | 4.x | Official Router |
| Pinia | 3.x | State Management |
| vue-i18n | 9.x | Internationalization |
| VueUse | 14.x | Composition API Utilities |

### Backend (Planned)

| Technology | Description |
|------------|-------------|
| Node.js + Express | API Service |
| Supabase | Database + Auth |
| Alibaba Qwen | AI Chat |
| OpenAI Embedding | Vector Search |

## 📁 Project Structure

```
ai-fisherman/
├── vue-app/                 # Frontend Vue Application
│   ├── src/
│   │   ├── assets/         # Static Assets
│   │   │   └── styles/     # Global Styles
│   │   ├── components/     # Reusable Components
│   │   ├── composables/    # Composition Functions
│   │   ├── data/           # Mock Data
│   │   ├── locales/        # i18n Files
│   │   ├── router/         # Router Config
│   │   ├── stores/         # Pinia Stores
│   │   ├── types/          # TypeScript Types
│   │   └── views/          # Page Components
│   ├── public/             # Public Assets
│   └── package.json
├── server/                  # Backend Service (Planned)
├── articles/               # Article Content
├── courses/                # Course Content
├── images/                 # Image Assets
└── README.md
```

## 🔧 Configuration

### Environment Variables

Configure in `vue-app/.env.local`:

```env
# API Configuration
VITE_API_BASE_URL=http://localhost:3000/api

# OAuth Configuration (Optional)
VITE_GITHUB_CLIENT_ID=your_github_client_id
VITE_GOOGLE_CLIENT_ID=your_google_client_id

# AI Configuration (Optional)
VITE_QWEN_API_KEY=your_qwen_api_key
```

## 🗺️ Roadmap

- [x] Basic Page Framework
- [x] Internationalization Support
- [x] Dark Mode
- [x] Apple-style UI
- [ ] Backend API Service
- [ ] OAuth Login Integration
- [ ] Smart Search Feature
- [ ] AI Assistant Integration
- [ ] Payment Features
- [ ] Admin Dashboard Enhancement

## 🤝 Contributing

Issues and Pull Requests are welcome!

See [Contributing Guide](./CONTRIBUTING.md) for details.

## 📄 License

[MIT License](./LICENSE)

## 🙏 Acknowledgements

- [Vue.js](https://vuejs.org/)
- [Vite](https://vitejs.dev/)
- [Apple Design Resources](https://developer.apple.com/design/)

---

If this project helps you, please give it a Star ⭐️
