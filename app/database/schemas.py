from datetime import datetime
import pydantic as pd
from typing import Optional

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
    active: Optional[bool] = None
    about_me: str
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