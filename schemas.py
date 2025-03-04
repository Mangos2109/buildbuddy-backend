from pydantic import BaseModel, EmailStr
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True  # For Pydantic v2

class TokenResponse(BaseModel):
    access_token: str
    token_type: str

class BuildCreate(BaseModel):
    name: str
    processors: str
    gpus: str
    ram: str
    motherboards: str
    storage: str
    psu: str
    total_price: float

class BuildResponse(BuildCreate):
    id: int

    class Config:
        from_attributes = True  # For Pydantic v2

class BuildsList(BaseModel):
    builds: List[BuildResponse]
