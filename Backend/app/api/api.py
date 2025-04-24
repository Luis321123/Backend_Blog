from fastapi import APIRouter, Depends
from app.api.endpoints.debug import router as router_debug
from app.api.endpoints.user import router as router_user
from app.api.endpoints.auth import router as router_auth
from app.api.deps import get_current_user, get_current_admin

api_router = APIRouter()


api_router.include_router(router_debug, tags=["Debug"],
    responses={404: {"description": "Not found"}})

api_router.include_router(router_user, tags=["User"],
    responses={404: {"description": "Not found"}})

api_router.include_router(router_auth, tags=["Auth"],
    responses={404: {"description": "Not found"}})