from fastapi import APIRouter, status
from fastapi.responses import JSONResponse
from pydantic import BaseModel

router = APIRouter()


class Message(BaseModel):
    message: str


@router.get("", summary="Health status", responses={404: {"model": Message}})
async def pong():
    return JSONResponse({"ping": "pong"}, status_code=status.HTTP_200_OK)
