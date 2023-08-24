from fastapi import APIRouter, Depends

from translation_server.api import route_translation, messages

api_router = APIRouter()

api_router.include_router(route_translation.router, prefix="/translate", tags=["translator"])

@api_router.get("/")
def get_default_site():
    usage = messages.message_howto
    return usage

