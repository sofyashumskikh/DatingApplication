from fastapi import APIRouter, Header, Depends, HTTPException, status, Response, Request, Body, UploadFile, File
from typing import List
from database import schemas, services, session
from sqlalchemy.orm import Session
from database import services

# Инициализация роутера
router = APIRouter()

BASE_PORT = 7000
BASE_URL = f"http://localhost:{BASE_PORT}"
UPLOAD_DIRECTORY = "/photos/"

def update_headers(token: str, db: Session, response: Response):
    role = services.get_role(token, db)
    moderated = services.get_moderated_by_token(token, db)
    active = services.get_active_by_token(token, db)

    response.headers["X-Active"] = str(active)
    response.headers["X-Moderated"] = str(moderated)
    response.headers["X-Role"] = role

#-------------ВХОД РЕГИСТРАЦИЯ---------------------
@router.post(
    "/api/register",
    response_model=schemas.Token,
    responses={
        400: {"description": "User with this email already exists"},
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
                },
        }},
    summary="зарегистрироваться"
)
def register_user(user: schemas.User, response: Response, db: Session = Depends(session.get_db_session)):
    new_user_id = services.create_user(user, db)
    if new_user_id is None:
        raise HTTPException(status_code=400, detail="User with this email already exists")
    token = services.create_token(new_user_id, db)
    if not token:
        raise HTTPException(status_code=500, detail="Failed to create token")
    update_headers(token.token, db, response)
    return token


@router.post(
    "/api/login",
    response_model=schemas.Token,
    responses={
        400: {"detail": "Invalid email pr password"},
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
            },
        }},
    summary="залогиниться"
)
def login_user(user: schemas.User, response: Response, db: Session = Depends(session.get_db_session)):
    user_id = services.verify_password_by_email(user.email, user.password, db)
    if user_id is None:
        raise HTTPException(status_code=400, detail="Invalid email pr password")
    token = services.update_token(user_id, db)
    if token is None:
        raise HTTPException(status_code=500, detail="Failed to create token")
    update_headers(token.token, db, response)
    return token


#--------------
@router.get(
    "/api/profiles",
    response_model=List[schemas.Profile],
    responses={
        401: {"detail": "Invalid token"},
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
            },
        }},
    summary="получить все профили для страницы поиска (для юзеров и модераторов)"
)
def get_profiles(token: str, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")

    active = services.get_active_by_token(token, db)
    if not active:
        return []
    
    role = services.get_role(token, db)
    if role == "moderator":
        profiles = services.get_all_profiles_by_moderator(db)
    else:
        profiles = services.get_all_profiles(token, db)
    update_headers(token, db, response)
    return profiles if profiles else []

    

@router.post(
    "/api/profile",
    response_class=Response,
    responses={
        401: {"detail": "Invalid token"},
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
            },
        }},
    summary = "добавить или обновить информацию о себе (для юзера и модератора)"
)
def update_profile(new_profile: schemas.Profile, token: str, response: Response,db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    role = services.get_role(token, db)
    if role == "moderator":
        if not services.update_profile_by_moderator(new_profile, db):
            raise HTTPException(status_code=404, detail="Profile not found")
    else:    
        services.create_or_update_profile(token, new_profile, db)

    update_headers(token, db, response)
    response.status_code = 200
    return response

@router.get(
    "/api/profile",
    response_model=schemas.Profile,
    responses={
        401: {"detail": "Invalid token"},
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
            },
        }},
    summary="получить информацию о своем профиле для лк"
)
def get_profile(token: str, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    profile = services.get_profile_by_token(token, db)
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    update_headers(token, db, response)
    return profile

@router.get(
    "/api/profile_photo",
    response_model=List[schemas.Photo],
    responses={
        401: {"detail": "Invalid token"},
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
            },
        }},
    summary="получить свое фото на странице лк"
)
def get_photos(token: str, user_id: int, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user = services.get_user_by_id(user_id, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    photos = services.get_photos(user.id, db)
    update_headers(token, db, response)
    return photos

@router.post(
    "/api/photo",
    response_model=schemas.Photo,
    responses={
        400: {"detail": "Only JPEG and PNG files supported"},
        401: {"detail": "Invalid token"},
        500: {"detail": "No profile found"},
        501: {"detail": "Couldn't save photo"},
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
            },
        }},
    summary="загрузить фото в лк"
)
def add_photo(token: str, response: Response, photo: UploadFile = File(...), db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    if not photo or photo.content_type not in ["image/jpeg", "image/png"]:
        raise HTTPException(status_code=400, detail="Only JPEG and PNG files supported")

    url = services.save_file(photo)
    if not url:
        raise HTTPException(status_code=501, detail="Couldn't save photo")

    photo_schema = services.create_photo(token, url, db)
    if not photo_schema:
        raise HTTPException(status_code=500, detail="No profile found")
    update_headers(token, db, response)
    return photo_schema

@router.post(
    "/api/like",
    response_class=Response,
    responses={
        401: {"detail": "Invalid token"},
        404:{"detail": "User not found"},
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
            },
        }},
    summary="поставить лайк"
)
def create_like(like: schemas.Like, token: str, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    like_added = services.create_likes(token, like, db)
    if not like_added:
        raise HTTPException(status_code=404, detail="User not found")

    update_headers(token, db, response)
    response.status_code = 200
    return response


@router.get(
    "/api/match",
    response_model=List[schemas.Profile],
    responses = {
        401: {"detail": "Invalid token"},
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
            },
        }},
    summary="получить пользователей с которыми мэтч"
)
def get_matches(token: str, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    update_headers(token, db, response)
    return services.get_match(token, db)

#-----------------------------------------
@router.delete(
    "/api/user",
    response_class=Response,
    responses={
        401: {"detail": "Invalid token"},
        404: {"detail": "User not found"},
        500: {"detail": "Couldn't delete user"},
        200: { "description": "Успешный ответ"}
    },
    summary="удалить пользователя"
)
def delete_user(token: str, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")

    user = services.get_user_by_token(token, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    update_headers(token, db, response)
    if services.delete_user_fully(user.id, db):
        response.status_code = 200
        return response
    else:
        raise HTTPException(status_code=500, detail="Couldn't delete user")

@router.delete(
    "/api/photo",
    response_class=Response,
    responses={
        401: {"detail": "Invalid token"},
        404: {"detail": "Profile not found"},
        405: {"detail": "Access denied"},
        200: {"description": "Успешный ответ"}

    },
    summary="удалить фото (для юзера и модератора)"
)
def delete_photo(token: str, photo_id: int, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    role = services.get_role(token, db)

    if role == "moderator":
        services.delete_photo_by_moderator(photo_id, db)
    else:
        profile = services.get_profile_by_token(token, db)
        if not profile:
            raise HTTPException(status_code=404, detail="Profile not found")
        photo_ids = set(p.id for p in get_photos(profile.id, db))
        if photo_id in photo_ids:
            services.delete_photo(photo_id, db)
        else:
            raise HTTPException(status_code=405, detail="Access denied")

    update_headers(token, db, response)
    response.status_code = 200
    return response


@router.post(
    "/api/notification",
    response_class=Response,
    responses={
        401: {"detail": "Invalid token"},
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
            },
        },
        500:{"detail": "No profile or user id"}
    },
    summary="если юзер посмотрел уведомление о том что профиль был изменен модератором"
)
def view_notification(token: str, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not services.notification_viewed(token, db):
        raise HTTPException(status_code=500, detail="No profile or user found")
    
    update_headers(token, db, response)
    response.status_code = 200
    return response


@router.post(
    "/api/complaint",
    response_class=Response,
    responses={
        401: {"detail": "Invalid token"},
        500: {"detail": "No profile"},
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
            },
        }
    },
    summary="создать жалобу")
def create_complaint(complaint: schemas.Complaint, token: str, response: Response , db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    if not services.create_complaint(complaint, db):
        raise HTTPException(status_code=500, detail="No profile")

    update_headers(token, db, response)
    response.status_code = 200
    return response


@router.delete(
    "/api/complaint",
    response_class=Response,
    responses={
        401: {"detail": "Invalid token"},
        404: {"detail": "User not found"},
        405: {"detail": "Access denied"},
        500:{"detail": "Error"},
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
            },
        }
    },
            summary="жалобы просмотрены")
def delete_complaint(profile_id: int, token: str, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    user= services.get_user_by_token(token, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "moderator":
        raise HTTPException(status_code=405, detail="Access denied")

    if not services.delete_complaints_for_profile(profile_id, db):
        raise HTTPException(status_code=500, detail="Error")

    update_headers(token, db, response)
    response.status_code = 200
    return response



@router.get(
    "/api/complaint",
    response_model=List[schemas.Complaint],
    responses={
        401: {"detail": "Invalid token"},
        404: {"detail": "User not found"},
        405: {"detail": "Access denied"},
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
            },
        }
    },
    summary="получить список жалоб на юзера")
def get_complaint(profile_id: int, token: str, response: Response, db: Session = Depends(session.get_db_session)):
    authorized = services.is_token_valid(token, db)
    if not authorized:
        raise HTTPException(status_code=401, detail="Invalid token")
    user = services.get_user_by_token(token, db)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    if user.role != "moderator":
        raise HTTPException(status_code=405, detail="Access denied")

    complaints = services.get_list_of_complaint(profile_id, db)
    update_headers(token, db, response)
    return complaints







