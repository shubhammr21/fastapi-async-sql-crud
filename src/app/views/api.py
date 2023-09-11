from fastapi import APIRouter

from app.views import notes, ping

api_router = APIRouter()

api_router.include_router(ping.router, prefix="/ping", tags=["ping"])
api_router.include_router(notes.router, prefix="/notes", tags=["notes"])
