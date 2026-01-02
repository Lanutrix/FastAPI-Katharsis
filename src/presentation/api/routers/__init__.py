"""API routers."""

from src.presentation.api.routers.auth import router as auth_router
from src.presentation.api.routers.math import router as math_router

__all__ = ["auth_router", "math_router"]

