from sqlalchemy import Column, Integer, String, Boolean, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Token(Base):
    __tablename__ = 'tokens'

    id = Column(Integer, primary_key=True, autoincrement=True)
    token = Column(String(36), nullable=False)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    update_at = Column(DateTime, nullable=False)

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(256), nullable=False)

    tokens = relationship('Token', backref='user')
    profile = relationship('Profile', backref='user', uselist=False)
    likes_from = relationship('Like', foreign_keys='Like.user_from_id', back_populates='user_from')
    likes_to = relationship('Like', foreign_keys='Like.user_to_id', back_populates='user_to')

class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('user.id'))
    name = Column(String(50))
    surname = Column(String(50))
    country_id = Column(Integer, ForeignKey('country.id'))
    city_id = Column(Integer, ForeignKey('city.id'))
    gender = Column(Boolean)
    age = Column(Integer)
    nickname_tg = Column(String(64))
    about_me = Column(String(300))
    active = Column(Boolean, default=True)

    photos = relationship('Photo', backref='profile')
    country = relationship('Country')
    city = relationship('City')

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
    user_from_id = Column(Integer, ForeignKey('user.id'))
    user_to_id = Column(Integer, ForeignKey('user.id'))

    user_from = relationship('User', foreign_keys=[user_from_id], back_populates='likes_from')
    user_to = relationship('User', foreign_keys=[user_to_id], back_populates='likes_to')

class Photo(Base):
    __tablename__ = 'photos'

    id = Column(Integer, primary_key=True, autoincrement=True)
    profile_id = Column(Integer, ForeignKey('profile.id'))
    photo_url = Column(String(150))
