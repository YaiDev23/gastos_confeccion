from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class EstadoEnum(str, Enum):
    activo = "activo"
    inactivo = "inactivo"


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    rol: str = Field(..., min_length=1, max_length=50)
    estado: EstadoEnum = EstadoEnum.activo


class UserCreate(UserBase):
    psw: str = Field(..., min_length=1, max_length=255)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=100)
    psw: Optional[str] = Field(None, max_length=255)
    rol: Optional[str] = Field(None, max_length=50)
    estado: Optional[EstadoEnum] = None


class UserResponse(UserBase):
    id_user: int
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    psw: str = Field(..., min_length=1)
