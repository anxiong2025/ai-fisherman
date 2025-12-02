from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import admin, articles, auth, chat, health, search
from app.core.config import get_settings
from app.core.database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    # Startup: initialize database
    await init_db()
    yield
    # Shutdown: cleanup if needed


def create_app() -> FastAPI:
    settings = get_settings()

    app = FastAPI(
        title=settings.app_name,
        version="0.1.0",
        lifespan=lifespan,
    )

    # CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Routes
    app.include_router(health.router, tags=["health"])
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(articles.router, prefix="/api/articles", tags=["articles"])
    app.include_router(search.router, prefix="/api/search", tags=["search"])
    app.include_router(chat.router, prefix="/api/chat", tags=["chat"])
    app.include_router(admin.router, prefix="/api/admin", tags=["admin"])

    return app


app = create_app()
