# AI Fisherman

> A modern AI technology blog platform with Apple-style design

English | [中文](./README.zh.md)

## Features

- Apple-style UI - Clean, elegant design with smooth animations
- 3D Particle Background - Golden spiral mathematical visualization
- Internationalization - Chinese/English bilingual support
- Dark Mode - Light/Dark/System theme support
- Smart Search - RAG-based content retrieval
- AI Assistant - Multi-LLM support (OpenAI, Anthropic, Gemini)
- OAuth Login - GitHub / Google quick login
- Responsive Design - Perfect mobile adaptation

## Tech Stack

### Frontend

| Technology | Version | Description |
|------------|---------|-------------|
| Vue | 3.5 | Progressive JavaScript Framework |
| TypeScript | 5.9 | Type Safety |
| Vite | 7.x | Next Generation Frontend Tooling |
| Vue Router | 4.x | Official Router |
| Pinia | 3.x | State Management |
| vue-i18n | 9.x | Internationalization |
| Three.js | 0.181 | 3D Graphics |

### Backend

| Technology | Version | Description |
|------------|---------|-------------|
| FastAPI | 0.115+ | Modern Python Web Framework |
| SQLAlchemy | 2.0 | ORM |
| ChromaDB | 0.5+ | Vector Database |
| Sentence Transformers | 3.3+ | Embeddings |

## Project Structure

```
ai-fisherman/
├── vue-app/                 # Frontend Vue Application
│   ├── src/
│   │   ├── api/            # API client
│   │   ├── assets/         # Static Assets
│   │   ├── components/     # Reusable Components
│   │   ├── locales/        # i18n Files
│   │   ├── router/         # Router Config
│   │   ├── stores/         # Pinia Stores
│   │   ├── types/          # TypeScript Types
│   │   └── views/          # Page Components
│   └── package.json
├── backend/                 # Backend FastAPI Service
│   ├── app/
│   │   ├── api/            # API Routes
│   │   ├── core/           # Core Config
│   │   ├── models/         # Database Models
│   │   ├── schemas/        # Pydantic Schemas
│   │   └── services/       # Business Logic
│   └── pyproject.toml
└── README.md
```

---

## Quick Start (Development)

### Requirements

- Node.js >= 18
- Python >= 3.11
- uv (recommended) or pip

### 1. Clone Repository

```bash
git clone https://github.com/your-username/ai-fisherman.git
cd ai-fisherman
```

### 2. Backend Setup

```bash
cd backend

# Create virtual environment and install dependencies
uv sync

# Copy environment config
cp .env.example .env

# Edit .env and configure your settings
# Important: Change SECRET_KEY for production!

# Start backend server
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### 3. Frontend Setup

```bash
cd vue-app

# Install dependencies
npm install

# Copy environment config
cp .env.example .env.local

# Edit .env.local
# Set VITE_API_BASE=http://localhost:8000/api

# Start frontend dev server
npm run dev
```

Visit http://localhost:3000

---

## Production Deployment (Tencent Cloud)

### Architecture

```
                    ┌─────────────┐
                    │   Nginx     │
                    │  (Port 80)  │
                    └──────┬──────┘
                           │
           ┌───────────────┼───────────────┐
           │               │               │
           ▼               ▼               │
    ┌─────────────┐ ┌─────────────┐        │
    │  Frontend   │ │   Backend   │        │
    │   (Static)  │ │  (Port 8000)│        │
    └─────────────┘ └─────────────┘        │
                                           │
                                    ┌──────┴──────┐
                                    │   SQLite    │
                                    │   ChromaDB  │
                                    └─────────────┘
```

### Server Requirements

- Ubuntu 22.04 LTS (recommended)
- 2 vCPU, 4GB RAM minimum
- 40GB SSD

### 1. Server Initial Setup

```bash
# Update system
sudo apt update && sudo apt upgrade -y

# Install basic tools
sudo apt install -y git curl wget nginx

# Install Node.js 20
curl -fsSL https://deb.nodesource.com/setup_20.x | sudo -E bash -
sudo apt install -y nodejs

# Install Python 3.11+
sudo apt install -y python3.11 python3.11-venv python3-pip

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
source $HOME/.local/bin/env
```

### 2. Clone and Setup Project

```bash
# Create app directory
sudo mkdir -p /var/www/ai-fisherman
sudo chown $USER:$USER /var/www/ai-fisherman

# Clone repository
cd /var/www/ai-fisherman
git clone https://github.com/your-username/ai-fisherman.git .
```

### 3. Backend Deployment

```bash
cd /var/www/ai-fisherman/backend

# Create virtual environment
uv sync --frozen

# Create production .env
cat > .env << 'EOF'
# Production Config
DEBUG=false

# CORS - Your domain
CORS_ORIGINS=["https://yourdomain.com","https://www.yourdomain.com"]

# Vector Store
CHROMA_PERSIST_DIR=./data/chroma
EMBEDDING_MODEL=sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2

# LLM Provider: openai, anthropic, or gemini
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
GEMINI_MODEL=gemini-2.0-flash-exp

# Database
DATABASE_URL=sqlite+aiosqlite:///./data/app.db

# JWT - CHANGE THIS!
SECRET_KEY=your-very-long-random-secret-key-at-least-32-chars
JWT_ALGORITHM=HS256
JWT_EXPIRE_MINUTES=10080

# OAuth (optional)
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret

# Frontend URL
FRONTEND_URL=https://yourdomain.com
EOF

# Create data directory
mkdir -p data

# Test backend runs
uv run uvicorn app.main:app --host 0.0.0.0 --port 8000
# Ctrl+C to stop
```

### 4. Backend Systemd Service

```bash
# Create service file
sudo cat > /etc/systemd/system/ai-fisherman-backend.service << 'EOF'
[Unit]
Description=AI Fisherman Backend
After=network.target

[Service]
Type=simple
User=www-data
Group=www-data
WorkingDirectory=/var/www/ai-fisherman/backend
Environment="PATH=/var/www/ai-fisherman/backend/.venv/bin"
ExecStart=/var/www/ai-fisherman/backend/.venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF

# Fix permissions
sudo chown -R www-data:www-data /var/www/ai-fisherman/backend

# Start service
sudo systemctl daemon-reload
sudo systemctl enable ai-fisherman-backend
sudo systemctl start ai-fisherman-backend

# Check status
sudo systemctl status ai-fisherman-backend
```

### 5. Frontend Build

```bash
cd /var/www/ai-fisherman/vue-app

# Create production .env
cat > .env.production << 'EOF'
VITE_API_BASE=https://yourdomain.com/api
EOF

# Install dependencies and build
npm ci
npm run build

# Move dist to nginx directory
sudo mkdir -p /var/www/html/ai-fisherman
sudo cp -r dist/* /var/www/html/ai-fisherman/
sudo chown -R www-data:www-data /var/www/html/ai-fisherman
```

### 6. Nginx Configuration

```bash
sudo cat > /etc/nginx/sites-available/ai-fisherman << 'EOF'
server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    # Redirect HTTP to HTTPS (uncomment after SSL setup)
    # return 301 https://$server_name$request_uri;

    root /var/www/html/ai-fisherman;
    index index.html;

    # Frontend - Vue SPA
    location / {
        try_files $uri $uri/ /index.html;
    }

    # Backend API Proxy
    location /api/ {
        proxy_pass http://127.0.0.1:8000/api/;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_cache_bypass $http_upgrade;
    }

    # Health check endpoint
    location /health {
        proxy_pass http://127.0.0.1:8000/health;
    }

    # Static assets caching
    location ~* \.(js|css|png|jpg|jpeg|gif|ico|svg|woff|woff2)$ {
        expires 1y;
        add_header Cache-Control "public, immutable";
    }

    # Gzip
    gzip on;
    gzip_types text/plain text/css application/json application/javascript text/xml application/xml;
}
EOF

# Enable site
sudo ln -sf /etc/nginx/sites-available/ai-fisherman /etc/nginx/sites-enabled/
sudo rm -f /etc/nginx/sites-enabled/default

# Test and reload nginx
sudo nginx -t
sudo systemctl reload nginx
```

### 7. SSL Certificate (Let's Encrypt)

```bash
# Install certbot
sudo apt install -y certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal is configured automatically
```

### 8. Firewall Setup

```bash
# Allow HTTP, HTTPS, SSH
sudo ufw allow 22
sudo ufw allow 80
sudo ufw allow 443
sudo ufw enable
```

---

## Docker Deployment (Alternative)

Docker provides a simpler deployment method with containerized services.

### Requirements

- Docker >= 20.10
- Docker Compose >= 2.0

### 1. Quick Start with Docker

```bash
# Clone repository
git clone https://github.com/your-username/ai-fisherman.git
cd ai-fisherman

# Create .env file for secrets
cat > .env << 'EOF'
SECRET_KEY=your-very-long-random-secret-key-at-least-32-chars
LLM_PROVIDER=gemini
GEMINI_API_KEY=your-gemini-api-key
GITHUB_CLIENT_ID=your-github-client-id
GITHUB_CLIENT_SECRET=your-github-client-secret
GOOGLE_CLIENT_ID=your-google-client-id
GOOGLE_CLIENT_SECRET=your-google-client-secret
FRONTEND_URL=http://localhost
EOF

# Start services
docker compose up -d

# View logs
docker compose logs -f
```

Frontend: http://localhost:80
Backend API: http://localhost:8000

### 2. With Nginx Reverse Proxy

For a unified entry point with rate limiting and SSL support:

```bash
# Start with nginx proxy profile
docker compose --profile with-proxy up -d
```

Access via: http://localhost:8080

### 3. Production Configuration

Edit `docker-compose.yml` environment variables:

```yaml
environment:
  - CORS_ORIGINS=["https://yourdomain.com"]
  - FRONTEND_URL=https://yourdomain.com
```

For SSL, place certificates in `nginx/ssl/`:
- `fullchain.pem`
- `privkey.pem`

### 4. Docker Commands

```bash
# Start services
docker compose up -d

# Stop services
docker compose down

# View logs
docker compose logs -f backend
docker compose logs -f frontend

# Rebuild after code changes
docker compose up -d --build

# Clean up volumes (WARNING: deletes data)
docker compose down -v
```

### 5. Scaling (Optional)

```bash
# Scale backend (requires load balancer)
docker compose up -d --scale backend=3
```

---

## Maintenance Commands

### View Logs

```bash
# Backend logs
sudo journalctl -u ai-fisherman-backend -f

# Nginx access logs
sudo tail -f /var/log/nginx/access.log

# Nginx error logs
sudo tail -f /var/log/nginx/error.log
```

### Restart Services

```bash
# Restart backend
sudo systemctl restart ai-fisherman-backend

# Restart nginx
sudo systemctl restart nginx
```

### Update Deployment

```bash
cd /var/www/ai-fisherman

# Pull latest code
git pull origin main

# Update backend
cd backend
uv sync --frozen
sudo systemctl restart ai-fisherman-backend

# Update frontend
cd ../vue-app
npm ci
npm run build
sudo cp -r dist/* /var/www/html/ai-fisherman/
```

---

## Environment Variables Reference

### Backend (.env)

| Variable | Required | Description |
|----------|----------|-------------|
| `DEBUG` | Yes | Set to `false` in production |
| `CORS_ORIGINS` | Yes | Allowed frontend origins (JSON array) |
| `SECRET_KEY` | Yes | JWT signing key (min 32 chars) |
| `DATABASE_URL` | Yes | SQLite connection string |
| `LLM_PROVIDER` | Yes | `openai`, `anthropic`, or `gemini` |
| `GEMINI_API_KEY` | Conditional | Required if using Gemini |
| `OPENAI_API_KEY` | Conditional | Required if using OpenAI |
| `ANTHROPIC_API_KEY` | Conditional | Required if using Anthropic |
| `GITHUB_CLIENT_ID` | Optional | For GitHub OAuth |
| `GITHUB_CLIENT_SECRET` | Optional | For GitHub OAuth |
| `GOOGLE_CLIENT_ID` | Optional | For Google OAuth |
| `GOOGLE_CLIENT_SECRET` | Optional | For Google OAuth |
| `FRONTEND_URL` | Yes | Frontend URL for OAuth callbacks |

### Frontend (.env.production)

| Variable | Required | Description |
|----------|----------|-------------|
| `VITE_API_BASE` | Yes | Backend API URL |

---

## Troubleshooting

### Backend won't start

```bash
# Check logs
sudo journalctl -u ai-fisherman-backend -n 50

# Check permissions
ls -la /var/www/ai-fisherman/backend/data/

# Try running manually
cd /var/www/ai-fisherman/backend
sudo -u www-data .venv/bin/uvicorn app.main:app --host 127.0.0.1 --port 8000
```

### 502 Bad Gateway

```bash
# Check if backend is running
sudo systemctl status ai-fisherman-backend

# Check if port 8000 is listening
sudo ss -tlnp | grep 8000
```

### Frontend not loading

```bash
# Check nginx config
sudo nginx -t

# Check if files exist
ls -la /var/www/html/ai-fisherman/
```

---

## License

[MIT License](./LICENSE)
