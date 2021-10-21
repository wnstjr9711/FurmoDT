from fastapi import APIRouter
from src.database.conn import SQLAlchemy
import bcrypt

router = APIRouter()


@router.post('/register')
async def register(user_id, user_pw):
    user = user_id, bcrypt.hashpw(user_pw.encode('utf-8'), bcrypt.gensalt())
    db = SQLAlchemy()
    db.register_user(*user, 1)
    return None


@router.post('/login')
async def login(client_id, client_password):
    return None
