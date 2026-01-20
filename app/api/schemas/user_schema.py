from pydantic import BaseModel, Field, field_validator
from typing import Optional, Union
from enum import Enum


class EstadoEnum(str, Enum):
    activo = "activo"
    inactivo = "inactivo"


class UserBase(BaseModel):
    username: str = Field(..., min_length=1, max_length=100)
    rol: str = Field(..., min_length=1, max_length=50)
    estado: Union[int, str] = Field(default=1)  # 1 = activo, 0 = inactivo o strings


class UserCreate(UserBase):
    username: str = Field(..., min_length=1, max_length=100)
    psw: str = Field(..., min_length=1, max_length=255)
    email: Optional[str] = Field(None, max_length=255)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, max_length=100)
    psw: Optional[str] = Field(None, max_length=255)
    rol: Optional[str] = Field(None, max_length=50)
    estado: Optional[Union[int, str]] = None


class UserResponse(BaseModel):
    id_user: int
    username: str
    rol: str
    estado: Union[int, str]
    
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str = Field(..., min_length=1)
    psw: str = Field(..., min_length=1)


class FactoryLogin(BaseModel):
    """Schema para login de taller por documento"""
    document: str = Field(..., min_length=1, description="Número de documento del taller")
