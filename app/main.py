from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.logger import logger
from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.category import router as category_router
from app.routers.menu_item import router as menu_item_router
from app.routers.cart import router as cart_router
from app.routers.restaurant_table import router as restaurant_table_router
from app.routers.reservation import (router as reservation_router)
from app.routers.order import router as order_router
from app.routers.payment import router as payment_router
from app.routers.admin import (
    router as admin_router
)



app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG,
    description="Backend API for DineEase Restaurant Management System"
)

# -------------------------
# CORS Configuration
# -------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",   # React (Vite)
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(auth_router)
app.include_router(users_router)
app.include_router(category_router)
app.include_router(menu_item_router)
app.include_router(cart_router)
app.include_router(restaurant_table_router)
app.include_router(reservation_router)
app.include_router(order_router)
app.include_router(payment_router)
app.include_router(admin_router)
# -------------------------
# Root Endpoint
# -------------------------
@app.get("/")
def root():
    logger.info("Root endpoint accessed.")
    return {
        "message": "Welcome to DineEase API 🚀"
    }


# -------------------------
# Health Check
# -------------------------
@app.get("/health")
def health_check():
    logger.info("Health check endpoint accessed.")
    return {
        "status": "Healthy",
        "application": settings.APP_NAME,
        "version": settings.APP_VERSION
    }