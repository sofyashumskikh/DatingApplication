from _operator import or_, and_
import datetime
from . import schemas
from . import session as dbase
from typing import List
import uuid #для токена
import bcrypt # для токена
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
from sqlalchemy import func
from fastapi import UploadFile
from routes import routes
import os

#------------------------------------------

#Регистрация

def hash_password(password: str) -> str: #!Надо проверить, что работает #Хэшируем пароль
    salt = bcrypt.gensalt()  # Генерируем соль
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)  # Хэшируем пароль
    return password_hash.decode('utf-8')  # Возвращаем строковое представление хэша


def create_user(user: schemas.User, db: Session) -> Optional[int]:
    existing_user = db.query(dbase.m.User).filter(dbase.m.User.email == user.email).first()
    if existing_user: # проверка, что юзера с таким емаил нет
        return None
    new_user = dbase.m.User(email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Обновляем объект, чтобы получить ID после добавления
    return new_user.id # возвращаем id

def create_token(user_id : int, db: Session) -> Optional[schemas.Token]:
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.user_id == user_id).first()
    if token_record:
        return None
    token = str(uuid.uuid4())
    new_token = dbase.m.Token(user_id=user_id, token=token, update_at=datetime.datetime.now())
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return schemas.Token.from_orm(new_token)


#-------------------------------------------------
#Авторизация
def verify_password_by_email(email: str, entered_password: str, db: Session) -> Optional[int]: # !Надо проверить, что работает # Сравнение введённого пароля с хэшом из базы данных
    user_record = db.query(dbase.m.User).filter(dbase.m.User.email == email).first()    # Ищем пользователя по email

    if user_record:
        if bcrypt.checkpw(entered_password.encode('utf-8'), user_record.password_hash.encode('utf-8')):  # !Надо проверить, что работает # Сравниваем введённый пароль с хэшом из базы данных
            return user_record.id  # Если пароль верен, возвращаем user_id

    return None  # Если пользователь не найден или пароль неверен


def update_token(user_id: int, db: Session) -> Optional[schemas.Token]: #апдейтим время токена
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.user_id == user_id).first()
    if not token_record:
        return None
    delete_user_token(user_id, db)
    actual_token=create_token(user_id, db)
    return actual_token  # Возвращаем токен, если обновление прошло успешно

def get_role(token: str, db: Session) -> Optional[str]: #проверять перед любым действием
    user = get_user_by_token(token, db)
    if not user:
        return None
    return user.role

#------------------------------------------

#Редактирование профиля
def is_token_valid(token: str, db: Session) -> Optional[bool]: #проверять перед любым действием
    if not token:
        return None
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.token == token).first()
    if not token_record : # проверка существования токена
        return None

    current_time = datetime.datetime.now()  # naive datetime (без временной зоны)
    expiration_time = token_record.update_at + datetime.timedelta(hours=24)
    return current_time <= expiration_time

def get_moderated_by_token(token: str, db: Session) -> Optional[bool]:
    user = get_user_by_token(token, db)
    if not user:
        return None
    return user.moderated

def get_active_by_token(token: str, db: Session) -> Optional[bool]:
    user = get_user_by_token(token, db)
    if not user:
        return None
    return user.active

def get_user_by_token(token: str, db: Session) -> Optional[dbase.m.User]:
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.token == token).first()
    if not token_record:
        return None
    return db.query(dbase.m.User).filter(dbase.m.User.id == token_record.user_id).first()

def get_user_by_id(user_id: int, db: Session) -> Optional[dbase.m.User]:
    return db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()

def create_or_update_profile(token: str, profile: schemas.Profile, db: Session) -> bool:
    user = get_user_by_token(token, db)
    if not user:
        return False
    db_profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id == user.id).first()
    country_id = get_or_create_country(profile.country_name, db)
    city_id = get_or_create_city(profile.city_name, db)

    if not db_profile:
        new_profile = dbase.m.Profile(
            user_id=user.id,
            name=profile.name,
            surname=profile.surname,
            country_id=country_id,
            city_id=city_id,
            gender=profile.gender,
            age=profile.age,
            about_me=profile.about_me,
            nickname_tg=profile.nickname_tg
        )

        db.add(new_profile)
        db.commit()
        db.refresh(new_profile)
        return True


    db_profile.name = profile.name
    db_profile.surname = profile.surname
    db_profile.country_id = country_id
    db_profile.city_id = city_id
    db_profile.gender = profile.gender
    db_profile.age = profile.age
    db_profile.about_me = profile.about_me
    db_profile.nickname_tg = profile.nickname_tg

    db.commit()
    db.refresh(db_profile)
    return True


def get_profile_by_token(token: str, db: Session) -> Optional[schemas.Profile]:
    user = get_user_by_token(token, db)
    if not user:
        return None
    profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id == user.id).first()
    if not profile:
        return None
    profile_schema = schemas.Profile.from_orm(profile)
    profile_schema.active = user.active
    profile_schema.country_name = get_country(profile.country_id, db)
    profile_schema.city_name = get_city(profile.city_id, db)
    return profile_schema

#Города и страны
def get_or_create_country(country_name: str, db: Session) -> int:
    existing_country = db.query(dbase.m.Country).filter(dbase.m.Country.country_name == country_name).first()
    if existing_country:
        return existing_country.id

    new_country = dbase.m.Country(country_name=country_name)
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country.id

def get_or_create_city(city_name: str, db: Session) -> int:
    existing_city = db.query(dbase.m.City).filter(dbase.m.City.city_name == city_name).first()
    if existing_city:
        return existing_city.id

    new_city = dbase.m.City(city_name=city_name)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city.id

def get_country (country_id: int, db: Session) -> Optional[str]:
    country = db.query(dbase.m.Country).filter(dbase.m.Country.id == country_id).first()
    if not country:
        return None
    return country.country_name

def get_city(city_id: int, db: Session) -> Optional[str]:
    city = db.query(dbase.m.City).filter(dbase.m.City.id == city_id).first()
    if not city:
        return None
    return  city.city_name

#Фото
def save_file(photo: UploadFile) -> Optional[str]:
    # Генерируем уникальное имя файла
    file_extension = photo.filename.split(".")[-1]
    unique_filename = f"{uuid.uuid4().hex}.{file_extension}"
    file_path = os.path.join(routes.UPLOAD_DIRECTORY, unique_filename)

    # Сохраняем файл
    try:
        os.makedirs(routes.UPLOAD_DIRECTORY, exist_ok=True)
        with open(file_path, "wb") as f:
            f.write(photo.file.read())
    except Exception as e:
        return None

    # Формируем URL для файла
    return f"{routes.BASE_URL}{routes.UPLOAD_DIRECTORY}{unique_filename}"

def create_photo(token: str, url: str, db: Session) -> Optional[schemas.Photo]:
    profile = get_profile_by_token(token, db)
    if not profile:
        return None

    new_photo = dbase.m.Photo(profile_id = profile.id, photo_url=url)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return schemas.Photo.from_orm(new_photo)


def delete_photo(photo_id: int, db: Session) -> bool:
    db_photo = db.query(dbase.m.Photo).filter(dbase.m.Photo.id == photo_id).first()
    photo_name = db_photo.photo_url.split("/")[-1]
    os.remove(f"{routes.UPLOAD_DIRECTORY}{photo_name}")

    db.query(dbase.m.Photo).filter(dbase.m.Photo.id == photo_id).delete()  # Удаляем фото
    db.commit()  # Применяем изменения в базе
    return True

def get_photos(profile_id: int, db: Session) -> List[schemas.Photo]:
    photos = db.query(dbase.m.Photo).filter(dbase.m.Photo.profile_id == profile_id).all()
    return [schemas.Photo.from_orm(photo) for photo in photos]

#------------------------------------------

# Претенденты на симпатию
def get_all_profiles(token: str, db: Session) -> Optional[List[schemas.Profile]]: # фильтрация по активности
    my_user = get_user_by_token(token, db)
    if not my_user:
        return None
    users = db.query(dbase.m.User).filter(dbase.m.User.active == True, dbase.m.User.id != my_user.id).all()
    user_ids = [user.id for user in users]
    profiles = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id.in_(user_ids)).all()

    profiles_schemas = []
    for profile in profiles:
        profile_schema = schemas.Profile.from_orm(profile)
        profile_schema.active = True
        profile_schema.country_name = get_country(profile.country_id, db)
        profile_schema.city_name = get_city(profile.city_id, db)
        profile_schema.nickname_tg = None
        profiles_schemas.append(profile_schema)
    return profiles_schemas

# лайк
def create_likes(token: str, like: schemas.Like, db: Session) -> bool:
    user = get_user_by_token(token, db)
    if not user:
        return False

    existing_like = db.query(dbase.m.Like).filter(
        and_(dbase.m.Like.user_id_from == user.id, dbase.m.Like.user_id_to == like.user_id_to)
    ).first()
    if existing_like:
        return True #лайк уже существует

    new_like = dbase.m.Like(user_id_from=user.id, user_id_to=like.user_id_to)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return True

def get_match(token: str, db: Session) -> List[schemas.Profile]:
    # Получаем ID текущего пользователя
    user = get_user_by_token(token, db)

    # Получаем все профили, которым пользователь поставил лайк
    likes_from_user = db.query(dbase.m.Like).filter(dbase.m.Like.user_id_from == user.id).all()
    user_ids_to = set(l.user_id_to for l in likes_from_user)

    # Получаем все профили, которые поставили лайк текущему пользователю
    likes_to_user = db.query(dbase.m.Like).filter(dbase.m.Like.user_id_to == user.id).all()
    user_ids_from = set(l.user_id_from for l in likes_to_user)

    user_ids_match = user_ids_to.intersection(user_ids_from)
    profiles_match = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id.in_(user_ids_match)).all()

    profile_schemas = []
    for profile in profiles_match:
        profile_schema = schemas.Profile.from_orm(profile)
        profile_schema.active = True
        profile_schema.country_name = get_country(profile.country_id, db)
        profile_schema.city_name = get_city(profile.city_id, db)

        if get_user_by_id(profile.user_id, db).active:
            profile_schemas.append(profile_schema)

    return profile_schemas
#_________________________________________________________
#Логика для жалоб
def create_complaint (complaint: schemas.Complaint, db: Session) -> bool:
    profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id== complaint.profile_id_to).first()
    if not profile:
        return False

    new_complaint = dbase.m.Complaint(
        profile_id_to = complaint.profile_id_to,
        letter= complaint.letter,
        added_at = datetime.datetime.now()
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    return True

#_________________________________________________________
#Для работы с уведомлениями от модератора

def notification_viewed (token: str, db: Session) -> Optional[bool]:
    user= get_user_by_token(token, db)
    if user is None:
        return None

    user.moderated = False
    return True
# _________________________________________________________
#Удаление юзера

def delete_user_token(user_id: int, db: Session) -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id== user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.Token).filter(dbase.m.Token.user_id == user_id).delete()
    return True

def delete_user_profile(profile_id: int, db: Session) -> bool:
    profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).first()
    if not profile:
        return False
    db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).delete()
    return True

def delete_user_photos(profile_id: int, db: Session) -> bool:
    profile_record = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).first()
    if not profile_record:
        return False
    db_photos = db.query(dbase.m.Photo).filter(dbase.m.Photo.profile_id == profile_id).all()
    for db_photo in db_photos:
        photo_name = db_photo.photo_url.split("/")[-1]
        os.remove(f"{routes.UPLOAD_DIRECTORY}{photo_name}")
    db.query(dbase.m.Photo).filter(dbase.m.Photo.profile_id == profile_id).delete()
    return True

def delete_user_likes(user_id: int, db: Session) -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.Like).filter(
        or_(dbase.m.Like.user_id_from == user_id, dbase.m.Like.user_id_to == user_id)
    ).delete()
    return True

def delete_user(user_id: int, db: Session) -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.User).filter(dbase.m.User.id == user_id).delete()
    return True

def delete_user_fully(user_id: int, db: Session) -> bool:
    try:
        user = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
        if user is None:
            return False

        delete_user_token(user_id, db)
        delete_user_likes(user_id, db)

        profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id == user_id).first()
        if profile:
            delete_user_photos(profile.id, db)
            delete_user_profile(profile.id, db)
            delete_complaints_for_profile(profile.id, db)

        delete_user(user_id, db)
        return True

    except SQLAlchemyError as e:
        db.rollback()
        return False

#__________________________________________________________

def get_complaint_count(profile_id: int, db: Session) -> int: #получение количества жалоб на пользователя
    complaint_count = db.query(func.count(dbase.m.Complaint.id)).filter(dbase.m.Complaint.profile_id_to == profile_id).scalar()
    return complaint_count

def get_all_profiles_by_moderator(db: Session) -> List[schemas.Profile]:
    profiles = db.query(dbase.m.Profile).all()
    for profile in profiles:
        profile.complaints_count = get_complaint_count(profile.id, db)

    profiles_sorted = sorted(
        profiles,
        key=lambda p: p.complaints_count,
        reverse=True
    )
    profiles = []
    for profile in profiles_sorted:
        profile_schema = schemas.Profile.from_orm(profile)
        profile_schema.active = get_user_by_id(profile.user_id, db).active
        profile_schema.country_name = get_country(profile.country_id, db)
        profile_schema.city_name = get_city(profile.city_id, db)
        profiles.append(profile_schema)
    return profiles

def get_list_of_complaint(profile_id: int, db: Session) -> List[schemas.Complaint]:
    complaints = (
        db.query(dbase.m.Complaint)
        .filter(dbase.m.Complaint.profile_id_to == profile_id)
        .order_by(dbase.m.Complaint.added_at.desc())
        .all()
    )
    return [schemas.Complaint.from_orm(complaint) for complaint in complaints]


def delete_complaints_for_profile(profile_id: int, db: Session) -> bool: #удаление списка жалоб после просмотра
    try:
        db.query(dbase.m.Complaint).filter(dbase.m.Complaint.profile_id_to == profile_id).delete()
        db.commit()
        return True

    except SQLAlchemyError as e:
        # В случае ошибки откатываем транзакцию
        db.rollback()
        return False


def update_profile_by_moderator(profile: schemas.Profile, db: Session) -> bool: #редактирование профиля
    db_profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile.id).first()
    if not db_profile:
        return False

    country_id = get_or_create_country(profile.country_name, db)
    city_id = get_or_create_city(profile.city_name, db)

    db_profile.name = profile.name
    db_profile.surname = profile.surname
    db_profile.country_id = country_id
    db_profile.city_id = city_id
    db_profile.gender = profile.gender
    db_profile.age = profile.age
    db_profile.about_me = profile.about_me
    db_profile.nickname_tg = profile.nickname_tg

    db_user = db.query(dbase.m.User).filter(dbase.m.User.id == db_profile.user_id).first()
    db_user.active = profile.active
    db_user.moderated = True

    db.commit()
    db.refresh(db_profile)
    db.refresh(db_user)
    return True

def delete_photo_by_moderator(photo_id: int, db: Session) -> bool:
    db_photo = db.query(dbase.m.Photo).filter(dbase.m.Photo.id == photo_id).first()
    if not db_photo:
        return False
    photo_name = db_photo.photo_url.split("/")[-1]
    os.remove(f"{routes.UPLOAD_DIRECTORY}{photo_name}")

    db_profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == db_photo.profile_id).first()
    if not db_profile:
        return False
    user = db.query(dbase.m.User).filter(dbase.m.User.id == db_profile.user_id).first()
    if not user:
        return False
    user.moderated = True

    db.query(dbase.m.Photo).filter(dbase.m.Photo.id == photo_id).delete()  # Удаляем фото
    db.commit()  # Применяем изменения в базе
    return True

