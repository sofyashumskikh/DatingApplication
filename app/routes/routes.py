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
@router.post("/api/register", response_model=schemas.BaseSchema,
responses={400: {"description": "User with this email already exists"},
               500: {"description": "Failed to create token"},
200: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }},
summary="зарегистрироваться")
def register_user(user: schemas.User,response: Response, db: Session = Depends(session.get_db_session)):
    new_user_id = services.create_user(user, db)
    if new_user_id is None:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    token = services.create_token(new_user_id, db)
    if not token:
        raise HTTPException(status_code=500, detail="Failed to create token")
    role = services.get_role(token, db)
    response.headers["X-Active"] = "True"
    response.headers["X-Moderated"] = "False"
    response.headers["X-Role"] = role
    return {"id": new_user_id, "token": token,
            "role": role,
            "moderated": False,
            "active": True}


@router.post("/api/login", response_model=schemas.BaseSchema, 
               responses={400: {"detail": "Invalid email pr password"},
               500: {"detail": "Failed to create token"},
               200: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }},
                summary="залогиниться" )
def login_user(user: schemas.User,response: Response, db: Session = Depends(session.get_db_session)):
    user_id = services.verify_password_by_email(user.email, user.password, db)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid email pr password")
    token = services.update_token(user_id, db)
    if token is None:
        raise HTTPException(status_code=500, detail="Failed to create token")
    role = services.get_role(token, db)
    moderated = services.get_moderated_by_token(token, db)
    active=services.get_active_by_token(token, db)
    response.headers["X-Active"] = str(active)
    response.headers["X-Moderated"] = str(moderated)
    response.headers["X-Role"] = role
    return {"id": user_id, "token": token,
    "role": role,
    "moderated": moderated,
    "active": active}


#--------------
@router.get("/api/users", response_model=List[schemas.Profile], 
            responses={401: {"detail": "Invalid token"},
                       200: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
            summary="получить всех юзеров для страницы поиска (для юзеров и модераторов )" )
def get_users( response: Response,authorization: str = Header(...), db: Session = Depends(session.get_db_session)): 
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    role = services.get_role(token, db)
    if role == "moderator":
        profiles =services.get_all_profiles_by_moderator(db)
    else:
        profiles = services.get_all_profiles(token, db)
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = role
    return profiles

    

@router.post("/api/profile", response_class=Response, 
            responses={401: {"detail": "Invalid token"},
                       201: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
             summary = "добавить или обновить информацию о себе (для юзера и модератора)") 
def post_profile( new_profile: schemas.Profile,response: Response,
                 authorization: str = Header(...),
                db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    role = services.get_role(token, db)
    if role == "moderator":
        services.update_profile_by_moderator(new_profile, db)
    else:    
        services.create_or_update_profile(new_profile, db)
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = role
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/api/profile", response_model=schemas.Profile,
            responses={401: {"detail": "Invalid token"},
                       404: {"detail": "Profile not found"},
                       200: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
             summary="получить информацию о своем профиле для лк")
def get_profile(response: Response,authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profile = services.get_profile_by_token(token, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = services.get_role(token, db)
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


@router.get("/api/profile_photo", response_model=List[schemas.Photo],
                      responses={401: {"detail": "Invalid token"},
                                 200: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
                        summary="получить свое фото на странице лк")
def get_photos(response: Response, authorization: str = Header(...),
                db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    id = services.get_user_id_by_token(token, db)
    photos = services.get_photos(id, db)

    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db)) 
    response.headers["X-Role"] = services.get_role(token, db)
    return photos


@router.get("/api/photo", response_model=List[schemas.Photo],                      
             responses={401: {"detail": "Invalid token"},
                        200: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
            summary="получить фото юзера на странице поиска")
def get_photos( response: Response,user_id: int = Body(..., embed=True),  # Получаем id в теле запроса
               authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    photos = services.get_photos(user_id, db)
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db)) 
    response.headers["X-Role"] = services.get_role(token, db)
    return photos


@router.post("/api/photo",  response_class=Response,                      
             responses={401: {"detail": "Invalid token"},
                        500: {"detail": "No profile"},
                        201: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
             summary="загрузить фото в лк")
def add_photo(photo: schemas.Photo,    response: Response ,authorization: str = Header(...),
               db: Session = Depends(session.get_db_session)):  
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if services.create_photo(photo, db):
        response.headers["X-Active"] = str(services.get_active_by_token(token, db))
        response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
        response.headers["X-Role"] = services.get_role(token, db)
        return Response(status_code=status.HTTP_201_CREATED)
    raise HTTPException(status_code=500, detail="No profile")


@router.post("/api/like", response_class=Response,                     
             responses={401: {"detail": "Invalid token"},
                        409:{"detail": "Like already exists"},
                        201: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
            summary="поставить лайк")
def create_like(like: schemas.Like,response: Response, authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    does_exist = services.create_likes(like)
    if does_exist:
        raise HTTPException(status_code=409, detail="Like already exists")
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = services.get_role(token, db)
    return Response(status_code=status.HTTP_201_CREATED)


@router.get("/api/like", response_model=List[schemas.Profile],
            responses = {401: {"detail": "Invalid token"},
            200: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }},
            summary="получить пользователей с которыми мэтч")
def get_matches( response: Response, authorization: str = Header(...), db: Session = Depends(session.get_db_session)): 
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = services.get_role(token, db)
    return services.get_match(token, db)

#-----------------------------------------
@router.delete("/api/profile", response_class=Response,                     
             responses={401: {"detail": "Invalid token"},
                        204: {
            "description": "Успешный ответ",
                          }}, 
            summary="удалить профиль")
def delete_user(response: Response, authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/api/photo", response_class=Response,                     
             responses={401: {"detail": "Invalid token"},
                        204: {
            "description": "Успешный ответ",
                          }}, 
            summary="удалить фото (для юзера и модератора)")
def delete_photo(photo:schemas.Photo, response: Response ,authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    role = services.get_role(token, db)
    if role == "moderator":
        services.delete_photo(photo.photo_url) #TODO: разобраться с функцией удаления
    else:    
        services.delete_photo(photo.photo_url) #TODO: разобраться с функцией удаления
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = role
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post("/api/notification", response_class=Response,                     
             responses={401: {"detail": "Invalid token"},
                        201: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               },
                          500:{"detail": "No profile or user id"}}, 
            summary="если юзер посмотрел уведомление о том что профиль был изменен модератором")
def view_notification(response: Response,authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not services.notification_viewed(token, db):
        raise HTTPException(status_code=500, detail="No profile or user id")
    
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = services.get_role(token, db)
    return Response(status_code=status.HTTP_201_CREATED)


@router.post("/api/complaint", response_class=Response,                     
             responses={401: {"detail": "Invalid token"},
                        500:{"detail": "No profile"},
                        201: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
            summary="создать жалобу")
def create_complaint(complaint: schemas.Complaint, response: Response ,authorization: str = Header(...), db: Session = Depends(session.get_db_session)
                ):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not services.create_complaint(complaint, db):
        raise HTTPException(status_code=500, detail="No profile")

        
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = services.get_role(token, db)
    return Response(status_code=status.HTTP_201_CREATED)   





@router.delete("/api/complaint", response_class=Response,                     
             responses={401: {"detail": "Invalid token"},
                        500:{"detail": "Error"},
                        204: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
            summary="жалобы просмотрены")
def delete_complaint(response: Response, user_id: int = Body(..., embed=True), authorization: str = Header(...), db: Session = Depends(session.get_db_session) ):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not services.delete_complaints_for_profile(user_id, db):
        raise HTTPException(status_code=500, detail="Error")
        
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = services.get_role(token, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)



@router.get("/api/complaint", response_model=schemas.Complaint,                     
             responses={401: {"detail": "Invalid token"},
                        204: {
            "description": "Успешный ответ",
            "headers": {
                "X-Active": {
                    "type": "boolean",
                },
                "X-Moderated": {
                    "type": "boolean",
                },
                "X-Role":{
                    "type": "string"
                }
            },               }}, 
            summary="получить список жалоб на юзера")
def get_complaint(response: Response, authorization: str = Header(...), db: Session = Depends(session.get_db_session)):
    token = authorization.split(" ")[1]  # Вытаскиваем токен после "Bearer"
    authorized = services.is_token_valid(token, db)
    if authorized==None or authorized==False:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    complaints = services.get_list_of_complaint()
    response.headers["X-Active"] = str(services.get_active_by_token(token, db))
    response.headers["X-Moderated"] = str(services.get_moderated_by_token(token, db))
    response.headers["X-Role"] = services.get_role(token, db)
    return Response(status_code=status.HTTP_204_NO_CONTENT)







