from datetime import datetime
import pydantic as pd
from typing import Optional, List

class BaseSchema(pd.BaseModel):
    id : int

class Token(pd.BaseModel):
    token: str

    class Config:
        from_attributes = True

class User(pd.BaseModel):
    email : str
    password: str

    class Config:
        from_attributes = True

class Profile(BaseSchema):
    user_id: int
    name: str
    surname: str
    country_name: Optional[str] = None
    city_name: Optional[str] = None
    gender: bool
    age: int
    horoscope: Optional[str] = None
    active: Optional[bool] = None
    about_me: Optional[str] = None
    nickname_tg: Optional[str] = None
    complaints_count: Optional[int] = None

    class Config:
        from_attributes = True

class Photo(BaseSchema):
    photo_url: str

    class Config:
        from_attributes = True

class Like(pd.BaseModel):
    user_id_to: int

    class Config:
        from_attributes = True

class Complaint(BaseSchema):
    profile_id_to: int
    letter: str
    added_at: datetime

    class Config:
        from_attributes = True

class Horoscope(BaseSchema):
    horoscope: str

    class Config:
        from_attributes = True

class UserFilterHistory(pd.BaseModel):
    age: Optional[List[int]] = None
    gender: Optional[List[bool]] = None
    horoscope: Optional[List[str]] = None
    city_name: Optional[List[str]] = None
    country_name: Optional[List[str]] = None

    class Config:
        from_attributes = True