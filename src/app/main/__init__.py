__all__ = [
    "create_app",
    "init_routers",
]

from .web import create_app
from .routers import init_routers
