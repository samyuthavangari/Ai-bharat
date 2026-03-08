"""
JanSahay AI - FastAPI Application Entry Point
Main application with all middleware, routes, and lifecycle hooks.
"""

import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.gzip import GZipMiddleware
from app.config import get_settings
from app.middleware.rate_limiter import RateLimitMiddleware

settings = get_settings()

# Configure logging
logging.basicConfig(
    level=logging.DEBUG if settings.DEBUG else logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("jansahay")


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifecycle: startup and shutdown hooks."""
    logger.info(f"🚀 Starting {settings.APP_NAME} v{settings.APP_VERSION}")
    logger.info(f"   Environment: {settings.ENVIRONMENT}")
    logger.info(f"   Debug: {settings.DEBUG}")
    logger.info(f"   Supported Languages: {settings.SUPPORTED_LANGUAGES}")

    # Startup
    try:
        from app.database import init_db
        await init_db()
        logger.info("✅ Database initialized")
    except Exception as e:
        logger.warning(f"⚠️ Database init skipped: {e}")

    try:
        from app.redis_client import get_redis
        r = await get_redis()
        await r.ping()
        logger.info("✅ Redis connected")
    except Exception as e:
        logger.warning(f"⚠️ Redis connection skipped: {e}")

    logger.info("✅ JanSahay AI is ready!")
    yield

    # Shutdown
    logger.info("🛑 Shutting down JanSahay AI...")
    try:
        from app.database import close_db
        await close_db()
    except Exception:
        pass
    try:
        from app.redis_client import close_redis
        await close_redis()
    except Exception:
        pass
    logger.info("👋 Goodbye!")


# Create FastAPI app
app = FastAPI(
    title="JanSahay AI",
    description=(
        "Voice-First Multilingual AI Assistant for Government Scheme Access in India. "
        "Helps citizens discover schemes, check eligibility, and get application guidance "
        "in 6 Indian languages via text, voice, and WhatsApp."
    ),
    version=settings.APP_VERSION,
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan,
)

# =============================================================================
# Middleware (order matters: last added = first executed)
# =============================================================================

# GZip compression for low-bandwidth optimization
app.add_middleware(GZipMiddleware, minimum_size=500)

# Rate limiting
app.add_middleware(RateLimitMiddleware)

# CORS - allow all origins for development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-RateLimit-Limit", "X-RateLimit-Remaining"],
)

# =============================================================================
# Register API Routes
# =============================================================================

from app.api.v1 import users, schemes, eligibility, chat, voice, documents, analytics, whatsapp

app.include_router(users.router, prefix="/api/v1")
app.include_router(schemes.router, prefix="/api/v1")
app.include_router(eligibility.router, prefix="/api/v1")
app.include_router(chat.router, prefix="/api/v1")
app.include_router(voice.router, prefix="/api/v1")
app.include_router(documents.router, prefix="/api/v1")
app.include_router(analytics.router, prefix="/api/v1")
app.include_router(whatsapp.router, prefix="/api/v1")

# =============================================================================
# Health Check & Root
# =============================================================================

@app.get("/")
async def root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "running",
        "docs": "/docs",
        "languages": settings.SUPPORTED_LANGUAGES,
    }


@app.get("/health")
@app.get("/api/v1/health")
async def health():
    """Health check endpoint for load balancer and monitoring."""
    return {
        "status": "healthy",
        "version": settings.APP_VERSION,
        "services": {
            "api": "up",
            "database": "configured",
            "redis": "configured",
            "voice": "mock" if not settings.GOOGLE_CLOUD_PROJECT_ID else "live",
            "whatsapp": "mock" if not settings.TWILIO_ACCOUNT_SID else "live",
        },
    }


@app.get("/api/v1/languages")
async def supported_languages():
    """Get list of supported languages."""
    from app.services.language_service import get_supported_languages
    return {
        "success": True,
        "languages": get_supported_languages(),
        "default": settings.DEFAULT_LANGUAGE,
    }
