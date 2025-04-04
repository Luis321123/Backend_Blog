from fastapi import APIRouter
from app.api.endpoints.debug import router as router_debug
from app.api.endpoints.bebida import router as router_bebidas
api_router = APIRouter()


api_router.include_router(router_bebidas, tags=["Bebidas"],
    responses={404: {"description": "Not found"}})

api_router.include_router(router_debug, tags=["Debug"],
    responses={404: {"description": "Not found"}})