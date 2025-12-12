from app.routes.auth import router as auth_router
from app.routes.users import router as users_router
from app.routes.calculations import router as calculations_router
from app.routes.analytics import router as analytics_router

__all__ = ["auth_router", "users_router", "calculations_router", "analytics_router"]