from fastapi import APIRouter, Header, Depends, HTTPException, status, Response, Request, Body
from typing import List, Callable
from database import schemas, services, session
from sqlalchemy.orm import Session
from fastapi.responses import JSONResponse

# Инициализация роутера
router = APIRouter()



# Главная страница
"""@router.get("/")
async def home():
    return {"message": "HOME"}
"""

#-------------ВХОД РЕГИСТРАЦИЯ---------------------
@router.post("/api/register", response_model=schemas.BaseSchema)
def register_user(user: schemas.User, db: Session = Depends(session.get_db_session)):
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
def login_user(user: schemas.User, db: Session = Depends(session.get_db_session)):
    user_id = services.verify_password_by_email(user.email, user.password, db)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid email pr password")
    token = services.update_token(user_id, db)
    if token is None:
        raise HTTPException(status_code=500, detail="Failed to create token")
    return {"id": user_id, "token": token}


#--------------
@router.get("/api/users", response_model=List[schemas.Profile], responses={401: {"description": "Invalid token"}}, summary="получить всех юзеров для стр поиска" )
def get_users(authorization: str = Header(...), db: Session = Depends(session.get_db_session)): 
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profiles = services.get_all_profiles(token, db)
    return profiles

    

@router.post("/api/profile", response_class=Response, summary = "созд или обновить инфу о себе") 
def post_profile( new_profile: schemas.Profile,
                 authorization: str = Header(...),
                db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"

    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    """profile = services.get_profile_by_token(token, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")  хз зачем это написала"""
    services.create_or_update_profile(new_profile, db)
    
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/api/profile", response_model=schemas.Profile, summary="получить инфу о профиле для лк")
def get_profile(authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"

    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profile = services.get_profile_by_token(token, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile


"""@router.put("/api/profile", response_class=Response, summary="обновить инфу о юзере в лк")
def update_profile(new_profile: schemas.Profile,
                    authorization: str = Header(...),
                    db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    
    services.create_or_update_profile(new_profile, db)
    
    return Response(status_code=status.HTTP_201_CREATED)
"""

@router.get("/api/profile_photo", response_model=List[schemas.Photo], summary="получить свое фото на странице лк")
def get_photos(authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    id = services.get_user_id_by_token(token, db)
    photos = services.get_photos(id, db)
    return photos


@router.get("/api/photo", response_model=List[schemas.Photo], summary="получить фото юзера на странице поиска")
def get_photos( user_id: int = Body(..., embed=True),  # Получаем id в теле запроса
               authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    photos = services.get_photos(user_id, db)
    return photos


@router.post("/api/photo",  response_class=Response)
def add_photo(photo: schemas.Photo, authorization: str = Header(...),
               db: Session = Depends(session.get_db_session)):  #TODO: как света исправит метод доделать
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    services.create_photo(photo, db)
    
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/api/like", response_class=Response)
def create_like(like: schemas.Like, authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    does_exist = services.create_likes(like)
    if does_exist:
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content={"detail": "Like already exists"}
        )    
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/api/like", response_model=List[schemas.Profile])
def get_matches(authorization: str = Header(...), db: Session = Depends(session.get_db_session)): 
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    return services.get_match(token, db)
