from fastapi import APIRouter, Header, Depends, HTTPException, status, Response
from typing import List
from database import schemas, services
from database.database import get_db_session
from sqlalchemy.orm import Session


# Инициализация роутера
router = APIRouter()

# Главная страница
@router.get("/")
async def home():
    return {"message": "HOME"}


@router.post("/api/register", response_model=schemas.BaseSchema)
def register_user(user: schemas.User, db: Session = Depends(get_db_session)):
    new_user_id = services.create_user(user, db)
    if new_user_id is None:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    # Создание токена для нового пользователя
    token = services.create_token(new_user_id, db)
    if not token:
        raise HTTPException(status_code=500, detail="Failed to create token")
    # Возвращаем id и token
    return {"id": new_user_id, "token": token}


@router.post("/api/login", response_model=schemas.BaseSchema)
def login_user(user: schemas.User, db: Session = Depends(get_db_session)):
    user_id = services.verify_password_by_email(user.email, user.password, db)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid email pr password")
    token = services.update_token_update_at(user_id, db)
    if token is None:
        raise HTTPException(status_code=500, detail="Failed to create token")
    return {"id": user_id, "token": token}


@router.get("/api/users", response_model=List[schemas.Profile])
def get_users(authorization: str = Header(...), db: Session = Depends(get_db_session)): #TODO: как света сделает подключить метод из сервисов
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"

    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    

@router.post("/api/profile", response_class=Response) 
def post_profile( new_profile: schemas.Profile,
                 authorization: str = Header(...),
                db: Session = Depends(get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"

    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profile = services.get_profile_by_token(token, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    services.create_or_update_profile(new_profile, db)
    
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/api/profile", response_model=schemas.Profile)
def get_profile(authorization: str = Header(...), db: Session = Depends(get_db_session)): 
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"

    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profile = services.get_profile_by_token(token, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


@router.put("/api/profile", response_class=Response)
def update_profile(new_profile: schemas.Profile,
                    authorization: str = Header(...),
                    db: Session = Depends(get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profile = services.get_profile_by_token(token, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    services.create_or_update_profile(new_profile, db)
    
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/api/profile_photo", response_model=List[schemas.Photo])
def get_photos(authorization: str = Header(...), db: Session = Depends(get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    id = services.get_user_id_by_token(token, db)
    if not id:
        raise HTTPException(status_code=404, detail="Profile not found")
    photos = services.get_photos(id, db)
    return photos


@router.get("/api/photo", response_model=List[schemas.Photo])
def get_photos(profile: schemas.Profile,
               authorization: str = Header(...), db: Session = Depends(get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    id = profile.user_id 
    photos = services.get_photos(id, db)
    return photos


@router.post("/api/photo",  response_class=Response)
def add_photo(photo: schemas.Photo, authorization: str = Header(...),
               db: Session = Depends(get_db_session)):  #TODO: как света исправит метод доделать
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    services.create_photo(photo, db)
    
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/api/like", response_class=Response)
def create_like(like: schemas.Like, authorization: str = Header(...), db: Session = Depends(get_db_session)): #TODO: как света исправит метод доделать
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    

    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/api/like", response_model=List[schemas.Profile])
def get_matches(authorization: str = Header(...), db: Session = Depends(get_db_session)): #TODO: как света исправит метод доделать
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
