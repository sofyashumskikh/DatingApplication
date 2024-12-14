import datetime as _dt
import pydantic as pd

class BaseSchema(pd.BaseModel):
    id : int
    token: str

class Token(pd.BaseModel):
    token: str

    class Config:
        orm_mode = True

class User(pd.BaseModel):
    # id: int
    email : str
    password: str
    # password_hash : str

    class Config:
        orm_mode = True

class Profile(BaseSchema):
    name: str
    surname: str
    country_name: str
    city_name: str
    gender: bool
    age: int
    active: bool
    about_me: str
    nickname_tg: str

    class Config:
        orm_mode = True

class Photo(BaseSchema):
    # profile_id: int
    photo_url: str

    class Config:
        orm_mode = True

class Like(BaseSchema):
    # user_from_id: int
    user_id_to: int

    class Config:
        orm_mode = True
