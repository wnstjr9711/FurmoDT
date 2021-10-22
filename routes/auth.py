import json

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from src.database.conn import SQLAlchemy

router = APIRouter()


@router.post('/register')
async def register(user_id, user_pw, authority_level):
    """
    user_id: `str(45)`\n
    user_pw: `str`
    """
    db = SQLAlchemy()
    success = db.user_register(user_id, user_pw, authority_level)
    return JSONResponse(status_code=200 if success else 400)


@router.post('/login')
async def login(user_id, user_pw):
    """
    user_id: `str(45)`\n
    user_pw: `str`
    """
    db = SQLAlchemy()
    msg, auth_level = db.user_login(user_id, user_pw)
    ret = {'msg': msg,
           'authority_level': auth_level}
    return JSONResponse(ret)
