from datetime import datetime, timedelta
from typing import Union
import jwt
from fastapi import HTTPException, Security
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from pydantic import BaseModel

# Секретный ключ для подписи токенов
SECRET_KEY = "your_secret_key"
ALGORITHM = "HS256"  # алгоритм для подписи токенов
ACCESS_TOKEN_EXPIRE_MINUTES = 30  # срок действия токена в минутах

# Секретный ключ и алгоритм могут быть настроены через переменные окружения в реальном проекте

# Настройка для пароля и безопасности
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2PasswordBearer позволяет работать с токенами через форму авторизации (например, через header)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Функция для создания токена
def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Функция для проверки токена
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload  # возвращаем данные из токена
    except jwt.ExpiredSignatureError:
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.JWTError:
        raise HTTPException(status_code=401, detail="Could not validate token")
    
# Функция для получения текущего пользователя
def get_current_user(token: str = Security(oauth2_scheme)):
    return verify_token(token)
