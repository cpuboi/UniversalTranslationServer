from fastapi import APIRouter, Depends

from translation_server.api import route_translation


api_router = APIRouter()

api_router.include_router(route_translation.router, prefix="/translate", tags=["translator"])



