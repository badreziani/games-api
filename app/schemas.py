from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel

# User Section


class UserBase(BaseModel):
    fullname: str
    username: str
    password: str
    role: str


class UserCreate(UserBase):
    pass


class User(BaseModel):
    id: int
    fullname: str
    role: str

    class Config:
        orm_mode = True
# End User


# Diplome Section
class Diplome(BaseModel):
    id: int
    type: str
    filiere: str
    guichet: str
    rdv: str
    date_retrait: Optional[datetime] = None
    operator: Optional[User] = None

    class Config:
        orm_mode = True
# End Diplome


# Student Section
class StudentBase(BaseModel):
    cne: str


class StudentCreate(StudentBase):
    pass


class Student(BaseModel):
    id: int
    cne: str
    nom: str
    diplomes: List[Diplome] = []

    class Config:
        orm_mode = True
# End Student


class DiplomeOut(BaseModel):
    type: str
    filiere: str
    guichet: str
    rdv: str
    owner_id: int

    class Config:
        orm_mode = True


class DiplomeUpdate(BaseModel):
    id: int


class Auth(BaseModel):
    username: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str] = None
