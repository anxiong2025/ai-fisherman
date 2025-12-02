#!/bin/bash
# AI Fisherman Deployment Script
# Usage: ./deploy.sh [backend|frontend|all]

set -e

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Configuration
PROJECT_DIR="/var/www/ai-fisherman"
FRONTEND_DIST="/var/www/html/ai-fisherman"
BACKEND_SERVICE="ai-fisherman-backend"

log_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

log_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running as appropriate user
check_permissions() {
    if [ "$EUID" -eq 0 ]; then
        log_warn "Running as root. Some commands will be adjusted."
    fi
}

# Deploy backend
deploy_backend() {
    log_info "Deploying backend..."

    cd "$PROJECT_DIR/backend"

    # Pull latest code
    log_info "Pulling latest code..."
    git pull origin main

    # Sync dependencies
    log_info "Syncing Python dependencies..."
    uv sync --frozen

    # Run database migrations if any
    # uv run alembic upgrade head

    # Restart service
    log_info "Restarting backend service..."
    sudo systemctl restart "$BACKEND_SERVICE"

    # Wait and check status
    sleep 3
    if sudo systemctl is-active --quiet "$BACKEND_SERVICE"; then
        log_info "Backend deployed successfully!"
    else
        log_error "Backend failed to start. Check logs with: sudo journalctl -u $BACKEND_SERVICE -n 50"
        exit 1
    fi
}

# Deploy frontend
deploy_frontend() {
    log_info "Deploying frontend..."

    cd "$PROJECT_DIR/vue-app"

    # Pull latest code (if not already done)
    log_info "Pulling latest code..."
    git pull origin main 2>/dev/null || true

    # Install dependencies
    log_info "Installing npm dependencies..."
    npm ci

    # Build
    log_info "Building frontend..."
    npm run build

    # Copy to nginx directory
    log_info "Copying to web directory..."
    sudo rm -rf "$FRONTEND_DIST"/*
    sudo cp -r dist/* "$FRONTEND_DIST"/
    sudo chown -R www-data:www-data "$FRONTEND_DIST"

    log_info "Frontend deployed successfully!"
}

# Full deployment
deploy_all() {
    log_info "Starting full deployment..."

    cd "$PROJECT_DIR"
    git pull origin main

    deploy_backend
    deploy_frontend

    # Reload nginx just in case
    sudo nginx -t && sudo systemctl reload nginx

    log_info "Full deployment completed!"
}

# Health check
health_check() {
    log_info "Running health checks..."

    # Check backend
    if curl -s -o /dev/null -w "%{http_code}" http://localhost:8000/health | grep -q "200"; then
        log_info "Backend: OK"
    else
        log_error "Backend: FAILED"
    fi

    # Check nginx
    if sudo systemctl is-active --quiet nginx; then
        log_info "Nginx: OK"
    else
        log_error "Nginx: FAILED"
    fi

    # Check frontend files
    if [ -f "$FRONTEND_DIST/index.html" ]; then
        log_info "Frontend files: OK"
    else
        log_error "Frontend files: MISSING"
    fi
}

# Show usage
usage() {
    echo "AI Fisherman Deployment Script"
    echo ""
    echo "Usage: $0 [command]"
    echo ""
    echo "Commands:"
    echo "  backend   Deploy backend only"
    echo "  frontend  Deploy frontend only"
    echo "  all       Deploy both backend and frontend"
    echo "  health    Run health checks"
    echo "  logs      Show backend logs"
    echo "  status    Show service status"
    echo ""
}

# Main
check_permissions

case "${1:-all}" in
    backend)
        deploy_backend
        ;;
    frontend)
        deploy_frontend
        ;;
    all)
        deploy_all
        ;;
    health)
        health_check
        ;;
    logs)
        sudo journalctl -u "$BACKEND_SERVICE" -f
        ;;
    status)
        sudo systemctl status "$BACKEND_SERVICE"
        sudo systemctl status nginx
        ;;
    *)
        usage
        exit 1
        ;;
esac
