from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from typing import List, Optional
from werkzeug.security import generate_password_hash, check_password_hash

from database import schemas, services
from sqlalchemy.orm import Session
from database.database import session_scope

# Для авторизации с JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Инициализация роутера
router = APIRouter()

# Главная страница
@router.get("/")
async def home():
    return {"message": "HOME"}
