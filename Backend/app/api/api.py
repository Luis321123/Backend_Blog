from fastapi import APIRouter
from app.api.endpoints.debug import router as router_debug

api_router = APIRouter()

api_router.include_router(router_debug, tags=["Debug"],
    responses={404: {"description": "Not found"}})