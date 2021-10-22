import json

from fastapi import APIRouter
from src.database.conn import SQLAlchemy

router = APIRouter()


@router.post('/register')
async def register(user_id, user_pw):
    """
    user_id: `str(45)`\n
    user_pw: `str`
    """
    db = SQLAlchemy()
    db.user_register(user_id, user_pw, 1)
    return None


@router.post('/login')
async def login(user_id, user_pw):
    """
    user_id: `str(45)`\n
    user_pw: `str`
    """
    db = SQLAlchemy()
    (msg, auth_level) = db.user_login(user_id, user_pw)
    ret = json.dumps({'msg': msg,
                      'authority_level': auth_level})
    return ret
