from fastapi import APIRouter, Depends
from app.api.endpoints.debug import router as router_debug
from app.api.endpoints.post import router as router_post
from app.controllers.authentication import jwtBearer

api_router = APIRouter()

api_router.include_router(router_post, tags=["post"],
    responses={404: {"description": "Not found"}})

api_router.include_router(router_debug, tags=["Debug"],
    responses={404: {"description": "Not found"}},
     dependencies=[Depends(jwtBearer())])