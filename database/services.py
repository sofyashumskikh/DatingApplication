from _operator import or_, and_

from . import schemas

import database as dbase
import datetime as dtime

#from typing import Listgit
from typing import List

import uuid #для токена
import bcrypt # для токена
from typing import Optional

# TODO: Маша: Провести все валидации перед вызовом методов
# TODO: Проверить что работает from_orm

#------------------------------------------

#Регистрация

def hash_password(password: str) -> str: #!Надо проверить, что работает #Хэшируем пароль
    salt = bcrypt.gensalt()  # Генерируем соль
    password_hash = bcrypt.hashpw(password.encode('utf-8'), salt)  # Хэшируем пароль
    return password_hash.decode('utf-8')  # Возвращаем строковое представление хэша


def create_user(user: schemas.User, db: "Session") -> Optional[int]:
    existing_user = db.query(dbase.m.User).filter(dbase.m.User.email == user.email).first()
    if existing_user: # проверка, что юзера с таким емаил нет
        return None
    new_user = dbase.m.User(email=user.email, password_hash=hash_password(user.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)  # Обновляем объект, чтобы получить ID после добавления
    return new_user.id # возвращаем id

def create_token(user_id: int, db: "Session") -> Optional[str]:
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.user_id == user_id).first()
    if token_record:
        return None
    token = str(uuid.uuid4())
    new_token = dbase.m.Token(user_id=user_id, token=token, update_at=dtime.datetime.now(dtime.timezone.utc))
    db.add(new_token)
    db.commit()
    db.refresh(new_token)
    return token


#-------------------------------------------------
#Авторизация
def verify_password_by_email(email: str, entered_password: str, db: "Session") -> Optional[int]: # !Надо проверить, что работает # Сравнение введённого пароля с хэшом из базы данных
    user_record = db.query(dbase.m.User).filter(dbase.m.User.email == email).first()    # Ищем пользователя по email

    if user_record:
        if bcrypt.checkpw(entered_password.encode('utf-8'), user_record.password_hash.encode('utf-8')):  # !Надо проверить, что работает # Сравниваем введённый пароль с хэшом из базы данных
            return user_record.id  # Если пароль верен, возвращаем user_id

    return None  # Если пользователь не найден или пароль неверен


def update_token(user_id: int, db: "Session") -> Optional[str]: #апдейтим время токена
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.user_id == user_id).first()
    if not token_record:
        return None
    delete_user_tokens(user_id, db)
    actual_token=create_token(user_id, db)
    # if actual_token == None:
    #     return None
    return actual_token  # Возвращаем токен, если обновление прошло успешно

#------------------------------------------

#Редактирование профиля
def is_token_valid(token: str, db: "Session") -> Optional[bool]: #проверять перед любым действием
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.token == token).first()
    if not token_record : # проверка существования токена
        return None

    current_time = dtime.datetime.now(dtime.timezone.utc)   # проверка срока годности токена
    expiration_time = token_record.update_at + dtime.timedelta(hours=24)
    if current_time > expiration_time:
        return False
    return True

def get_user_id_by_token(token: str, db: "Session") -> Optional[int]:
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.token == token).first()
    if token_record:
        return token_record.user_id
    return None #токен не найден

def create_or_update_profile(profile: schemas.Profile, db: "Session") -> bool:
    """if not is_token_valid(profile.token, db):
        return False""" #мне кажется можно убрать птмч этого нет в других методах и я проверяю сама это
    db_profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile.id).first()
    country_id = get_or_create_country(profile.country_name, db)
    city_id = get_or_create_city(profile.city_name, db)

    if not db_profile:
        new_profile = dbase.m.Profile(
            user_id=get_user_id_by_token(profile.token, db),
            name=profile.name,
            surname=profile.surname,
            country_id=country_id,
            city_id=city_id,
            gender=profile.gender,
            age=profile.age,
            about_me=profile.about_me,
            active=profile.active,
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
    db_profile.active = profile.active

    db.commit()
    db.refresh(db_profile)
    return True


def get_profile_by_token(token: str, db: "Session") -> Optional[schemas.Profile]:
    user_id = get_user_id_by_token(token, db)
    if not user_id:
        return None

    profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id == user_id).first()
    return schemas.Profile.from_orm(profile) if profile else None

#Города и страны
async def get_or_create_country(country_name: str, db: "Sesfsion") -> int:
    existing_country = db.query(dbase.m.Country).filter(dbase.m.Country.country_name == country_name).first()
    if existing_country:
        return existing_country.id

    new_country = dbase.m.Country(country_name=country_name)
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country.id

async def get_or_create_city(city_name: str, db: "Session") -> int:
    existing_city = db.query(dbase.m.City).filter(dbase.m.City.city_name == city_name).first()
    if existing_city:
        return existing_city.id

    new_city = dbase.m.City(city_name=city_name)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city.id

#Фото
async def create_photo(photo: schemas.Photo, db: "Session") -> bool: #в сземе Ф
    profile = get_profile_by_token(photo.token, db)
    if not profile:
        return False

    new_photo = dbase.m.Photo(profile_id = profile.id, photo_url=photo.photo_url)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return True

async def delete_photo(photo_id: int, db: "Session") -> bool:
    db.query(dbase.m.Photo).filter(dbase.m.Photo.id == photo_id).delete()  # Удаляем фото
    db.commit()  # Применяем изменения в базе
    return True

async def get_photos(profile_id: int, db: "Session") -> List[schemas.Photo]:
    photos = db.query(dbase.m.Photo).filter(dbase.m.Photo.profile_id == profile_id).all()
    return [schemas.Photo.from_orm(photo) for photo in photos]

#------------------------------------------

# Претенденты на симпатию
def get_all_profiles(token: str, db: "Session") -> List[schemas.Profile]: # фильтрация по паcсивам
    my_user_id= get_user_id_by_token(token,db)
    profiles = (db.query(dbase.m.Profile).filter(dbase.m.Profile.active == True, dbase.m.Profile.id != my_user_id).all())
    profiles_schemas = [schemas.Profile.from_orm(profile) for profile in profiles]
    for profile in profiles_schemas:
        profile.nickname_tg = None #не показываем тг ник при просмотре профилей (показываем только при метче)
    return profiles_schemas

# лайк
def create_likes(like: schemas.Like, db: "Session") -> bool:
    existing_like = db.query(dbase.m.Like).filter(
        and_(dbase.m.Like.user_id_from == get_user_id_by_token(like.token, db), dbase.m.Like.user_id_to == like.user_id_to)
    ).first()
    if existing_like:
        return False #лайк уже существует
    new_like = dbase.m.Like(user_from_id=get_user_id_by_token(like.token, db), user_to_id=like.user_id_to)
    db.add(new_like)
    db.commit()
    db.refresh(new_like)
    return True


def get_match(token: str, db: "Session") -> List[schemas.Profile]:
    # Получаем ID текущего пользователя
    user_id = get_user_id_by_token(token, db)

    # Получаем все профили, которым пользователь поставил лайк
    likes_from = db.query(dbase.m.Like).filter(
        dbase.m.Like.user_id_from == user_id
    ).all()

    # Получаем все профили, которые поставили лайк текущему пользователю
    likes_to = db.query(dbase.m.Like).filter(
        dbase.m.Like.user_id_to == user_id
    ).all()

    user_ids_to = set(l.user_id_to for l in likes_from)
    user_ids_from = set(l.user_id_from for l in likes_to)

    user_ids_match = user_ids_to.intersection(user_ids_from)
    profiles_match = db.query(dbase.m.Profile).filter(
        dbase.m.Profile.user_id in user_ids_match
    ).all()

    return [schemas.Profile.from_orm(profile) for profile in profiles_match]


#_________________________________________________________
#Удаление юзера

async def delete_user_tokens(user_id: int, db: "Session") -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id== user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.Token).filter(dbase.m.Token.user_id == user_id).delete()
    db.commit()
    return True

def delete_user_profile(profile_id: int, db: "Session") -> bool:
    profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).first()
    if not profile:
        return False
    db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).delete()
    db.commit()
    return True

def delete_user_photos(profile_id: int, db: "Session") -> bool:
    profile_record = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).first()
    if not profile_record:
        return False
    db.query(dbase.m.Photo).filter(dbase.m.Photo.profile_id == profile_id).delete()
    db.commit()
    return True

def delete_user_likes(user_id: int, db: "Session") -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.Like).filter(
        or_(dbase.m.Like.user_id_from == user_id, dbase.m.Like.user_id_to == user_id)
    ).delete()
    db.commit()
    return True

def delete_user(user_id: int, db: "Session") -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.User).filter(dbase.m.User.id == user_id).delete()
    db.commit()
    return True


def delete_user_fully(user_id: int, db: "Session") -> bool:
    user = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
    profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id == user_id).first()
    if user is None:
        return False
    if profile is None:
        return False
    delete_user_tokens(user_id, db)
    delete_user_likes(user_id, db)
    if profile:
        delete_user_photos(profile.id, db)
        delete_user_profile(profile.id, db)
    delete_user(user_id, db)

    return True

