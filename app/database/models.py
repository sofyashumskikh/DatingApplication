from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime, ARRAY
from sqlalchemy.orm import declarative_base

Base = declarative_base()

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(36), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    update_at = Column(DateTime, nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)
    role = Column(String(10), default="user")
    moderated = Column(Boolean, default=False)
    active = Column(Boolean, default=True)

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    name = Column(String(50))
    surname = Column(String(50))
    country_id = Column(Integer, ForeignKey('countries.id'))
    horoscope_id = Column(Integer, ForeignKey('horoscopes.id'))
    city_id = Column(Integer, ForeignKey('cities.id'))
    gender = Column(Boolean)
    age = Column(Integer)
    nickname_tg = Column(String(64))
    about_me = Column(String(300))

class City(Base):
    __tablename__ = 'cities'

    id = Column(Integer, primary_key=True, autoincrement=True)
    city_name = Column(String(50), nullable=False)

class Country(Base):
    __tablename__ = 'countries'

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_name = Column(String(50), nullable=False)

class Like(Base):
    __tablename__ = 'likes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id_from = Column(Integer, ForeignKey('users.id'))
    user_id_to = Column(Integer, ForeignKey('users.id'))

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('profiles.id'))
    photo_url = Column(String(150))

class Complaint(Base):
    __tablename__ = 'complaints'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id_to = Column(Integer, ForeignKey('profiles.id'), nullable=False)
    letter = Column(String(300), nullable=False)
    added_at = Column(DateTime, nullable=False)

class Horoscope(Base):
    __tablename__ = 'horoscopes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    horoscope = Column(String(30), nullable=False)

class UserFilterHistory(Base):
    __tablename__ = 'user_filter_history'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, nullable=False)
    age = Column(ARRAY(Integer), nullable=True)
    gender = Column(ARRAY(Boolean), nullable=True)
    horoscope_id = Column(ARRAY(Integer), nullable=True)
    city_id = Column(ARRAY(Integer), nullable=True)
    country_id = Column(ARRAY(Integer), nullable=True)
    added_at = Column(DateTime, nullable=False)


