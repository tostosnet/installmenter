
from app.models import GuarantorDB
from datetime import date, datetime
from typing import List, Optional
from pydantic import BaseModel, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: str
    role: str
    expire: datetime


class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostResponse(BaseModel):
    title: str
    content: str
    created_date: datetime
    owner_id: int

    class Config:
        orm_mode = True


class PostModel(PostBase):
    pass


class MngCreate(BaseModel):
    surname: str
    first_name: str
    email: EmailStr
    password: str


class MngCreateResponse(BaseModel):
    id: int
    surname: str
    first_name: str
    email: EmailStr
    created_date: datetime

    class Config:
        orm_mode = True


class MngGetResponse(MngCreateResponse):
    pass


class ClientGrtCreate(BaseModel):
    surname: str
    first_name: str
    last_name: str = ""
    email: EmailStr
    phone_number: str
    phone_number_2: str = ""
    street: str
    city: str
    state: str
    photo: str
    id_type: str
    id_number: str
    id_issue_date: date
    id_expiry_date: Optional[str] = None
    id_photo: str = ""
    signature_photo: str = ""
    form_photo: str = ""



class GuarantorCreate(ClientGrtCreate):
    client_id: str = ""


class ClientCreate(ClientGrtCreate):
    id: str = ""
    password: str = ""
    manager_id: int = 0
    grt1: GuarantorCreate = None
    grt2: GuarantorCreate = None


class GrtCreateResponse(ClientGrtCreate):
    id: int
    client_id: int
    created_date: datetime

    class Config:
        orm_mode = True


class GrtGetResponse(GrtCreateResponse):
    pass


class ClientCreateResponse(ClientGrtCreate):
    id: int
    manager_id: int
    created_date: datetime
    guarantors: Optional[List[GrtGetResponse]] = []
    
    class Config:
        orm_mode = True


class ClientGetResponse(ClientCreateResponse):
    pass


class User(ClientCreateResponse):
    pass
