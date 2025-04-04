from fastapi import APIRouter
from app.api.endpoints.debug import router as router_debug
from app.api.endpoints.posts import router as router_posts
from app.api.endpoints.health import router as router_health

api_router = APIRouter()

api_router.include_router(router_debug, tags=["Debug"],
    responses={404: {"description": "Not found"}})


api_router.include_router(router_posts, tags=["Posts"], 
    responses={404: {"description": "Not found"}})

api_router.include_router(router_health, tags=["Health Check"],
    responses={404: {"description": "Not found"}})