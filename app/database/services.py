from _operator import or_, and_
import dtime
from . import schemas
from . import session as dbase
from typing import List
import uuid #для токена
import bcrypt # для токена
from sqlalchemy.exc import SQLAlchemyError
from typing import Optional
from sqlalchemy import func

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

def create_token(user_id : int, db: "Session") -> Optional[str]:
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
    delete_user_token(user_id, db)
    actual_token=create_token(user_id, db)
    # if actual_token == None:
    #     return None
    return actual_token  # Возвращаем токен, если обновление прошло успешно

def get_role (token: str, db: "Session") -> Optional[str]: #проверять перед любым действием
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id == get_user_id_by_token(token, db)).first()
    if not user_record:
        return None

    return user_record.role


#------------------------------------------

#Редактирование профиля
def is_token_valid(token: str, db: "Session") -> Optional[bool]: #проверять перед любым действием
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.token == token).first()
    if not token_record : # проверка существования токена
        return None

    current_time = dtime.datetime.now(dtime.timezone.utc)   #проверка срока годности токена
    expiration_time = token_record.update_at + dtime.timedelta(hours=24)
    if current_time > expiration_time:
        return False
    return True

# def profile_is_moderated (token: str , db: "Session") -> bool: #проверять перед любым действием
#     return get_profile_by_token(token, db).moderated
#def profile_is_active (token: str , db: "Session") -> bool:
    #return get_profile_by_token(token, db).active


def get_user_id_by_token(token: str, db: "Session") -> Optional[int]:
    token_record = db.query(dbase.m.Token).filter(dbase.m.Token.token == token).first()
    if token_record:
        return token_record.user_id
    return None #токен не найден

def create_or_update_profile(profile: schemas.Profile, db: "Session") -> bool:
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


def get_profile_by_token(token: str, db: "Session") -> Optional[schemas.Profile]:
    user_id = get_user_id_by_token(token, db)
    if not user_id:
        return None

    profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id == user_id).first()
    return schemas.Profile.from_orm(profile) if profile else None

#Города и страны
def get_or_create_country(country_name: str, db: "Sesfsion") -> int:
    existing_country = db.query(dbase.m.Country).filter(dbase.m.Country.country_name == country_name).first()
    if existing_country:
        return existing_country.id

    new_country = dbase.m.Country(country_name=country_name)
    db.add(new_country)
    db.commit()
    db.refresh(new_country)
    return new_country.id

def get_or_create_city(city_name: str, db: "Session") -> int:
    existing_city = db.query(dbase.m.City).filter(dbase.m.City.city_name == city_name).first()
    if existing_city:
        return existing_city.id

    new_city = dbase.m.City(city_name=city_name)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return new_city.id

#Фото
def create_photo(photo: schemas.Photo, db: "Session") -> bool: #в сземе Ф
    profile = get_profile_by_token(photo.token, db)
    if not profile:
        return False

    new_photo = dbase.m.Photo(profile_id = profile.id, photo_url=photo.photo_url)
    db.add(new_photo)
    db.commit()
    db.refresh(new_photo)
    return True

def delete_photo(photo_id: int, db: "Session") -> bool:
    db.query(dbase.m.Photo).filter(dbase.m.Photo.id == photo_id).delete()  # Удаляем фото
    db.commit()  # Применяем изменения в базе
    return True

def get_photos(profile_id: int, db: "Session") -> List[schemas.Photo]:
    photos = db.query(dbase.m.Photo).filter(dbase.m.Photo.profile_id == profile_id).all()
    return [schemas.Photo.from_orm(photo) for photo in photos]

#------------------------------------------

# Претенденты на симпатию
def get_all_profiles(token: str, db: "Session") -> List[schemas.Profile]: # фильтрация по активности
    my_user_id= get_user_id_by_token(token,db)
    profiles = (db.query(dbase.m.Profile).filter(dbase.m.Profile.active == True, dbase.m.Profile.user_id != my_user_id).all())
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
#Логика для жалоб
def create_complaint (complaint: schemas.Complaint, db: "Session") -> bool: #пользователь написал жалобу
    # TODO: Проверить что профиль существует с таким id и вернуть false если нет

    new_complaint = dbase.m.Complaint(
        profile_id_to = complaint.profile_id_to,
        letter= complaint.letter,
        added_at = dtime.datetime.now(dtime.timezone.utc)
    )

    db.add(new_complaint)
    db.commit()
    db.refresh(new_complaint)
    return True

#_________________________________________________________
#Для работы с уведомлениями от модератора

def notification_viewed (token: str, db: "Session") -> bool:
    user_id = get_user_id_by_token(token, db)
    if user_id is None:
        return False
    db_profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id == user_id).first()
    if db_profile is None:
        return False

    db_profile.moderated = False
    return True
# _________________________________________________________
#Удаление юзера

def delete_user_token(user_id: int, db: "Session") -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id== user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.Token).filter(dbase.m.Token.user_id == user_id).delete()
    return True

def delete_user_profile(profile_id: int, db: "Session") -> bool:
    profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).first()
    if not profile:
        return False
    db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).delete()
    return True

def delete_user_photos(profile_id: int, db: "Session") -> bool:
    profile_record = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).first()
    if not profile_record:
        return False
    db.query(dbase.m.Photo).filter(dbase.m.Photo.profile_id == profile_id).delete()
    return True

def delete_user_likes(user_id: int, db: "Session") -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.Like).filter(
        or_(dbase.m.Like.user_id_from == user_id, dbase.m.Like.user_id_to == user_id)
    ).delete()
    return True

def delete_user(user_id: int, db: "Session") -> bool:
    user_record = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
    if not user_record:
        return False
    db.query(dbase.m.User).filter(dbase.m.User.id == user_id).delete()
    return True

def delete_user_fully(user_id: int, db: "Session") -> bool:
    try:
        with db.begin():  # начало транзакции
            user = db.query(dbase.m.User).filter(dbase.m.User.id == user_id).first()
            if user is None:
                return False

            delete_user_token(user_id, db)
            delete_user_likes(user_id, db)

            profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.user_id == user_id).first()
            if profile:
                delete_user_photos(profile.id, db)
                delete_user_profile(profile.id, db)

            delete_user(user_id, db)

        return True

    except SQLAlchemyError as e:
        db.rollback()
        return False

#__________________________________________________________
#Методы для модератора
# def get_user_id_by_profile_id (profile_id: int, db: "Session") -> int:
#     db_profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile_id).first()
#     return db_profile.user_id

def get_complaint_count(profile_id: int, db: "Session") -> int: #получение количества жалоб на пользователя
    complaint_count = db.query(func.count(dbase.m.Complaint.id)).filter(dbase.m.Complaint.profile_id == profile_id).scalar()
    return complaint_count

def get_all_profiles_by_moderator(db: "Session") -> List[schemas.Profile]: #получение списка для просмотра профилей
    profiles = db.query(dbase.m.Profile).filter(dbase.m.Profile.active == True).all()
    profiles_with_complaint_count = sorted(
        profiles,
        key=lambda profile: get_complaint_count(profile.id, db),
        reverse=True
    )
    return profiles_with_complaint_count

# TODO: метод чтобы получить жалобы по профилю

def delete_complaints_for_profile(profile_id: int, db: "Session") -> bool: #удаление списка жалоб после просмотра
    try:
        db.query(dbase.m.Complaint).filter(dbase.m.Complaint.profile_id == profile_id).delete()
        db.commit()
        return True

    except SQLAlchemyError as e:
        # В случае ошибки откатываем транзакцию
        db.rollback()
        return False

# TODO: методы чтобы вернуть moderated и active по токену

def update_profile_by_moderator(profile: schemas.Profile, db: "Session") -> int: #редактирование профиля
    db_profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == profile.id).first()

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
    db_profile.active = profile.active
    db_profile.moderated = True

    db.commit()
    db.refresh(db_profile)

def delete_photo_by_moderator(photo_id: int, db: "Session") -> bool:
    db_photo = db.query(dbase.m.Photo).filter(dbase.m.Photo.id == photo_id).first()
    if not db_photo:
        return False
    db_profile = db.query(dbase.m.Profile).filter(dbase.m.Profile.id == db_photo.profile_id).first()
    if not db_profile:
        return False
    db_profile.moderated = True
    db.query(dbase.m.Photo).filter(dbase.m.Photo.id == photo_id).delete()  # Удаляем фото
    db.commit()  # Применяем изменения в базе
    return True

