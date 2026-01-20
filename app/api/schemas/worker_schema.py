from pydantic import BaseModel, Field, validator
from typing import Optional, List
from datetime import datetime


class WorkerCreate(BaseModel):
    """Schema para crear un nuevo trabajador"""
    nombre: str = Field(..., min_length=1, max_length=100, description="Nombre del trabajador")
    apellido: Optional[str] = Field(None, max_length=100, description="Apellido del trabajador")
    cedula: str = Field(..., min_length=1, max_length=20, description="Cédula del trabajador (única)")
    cargo: str = Field(..., min_length=1, max_length=100, description="Cargo del trabajador")
    salario: float = Field(..., gt=0, description="Salario del trabajador")
    email: Optional[str] = Field(None, max_length=100, description="Email del trabajador")
    telefono: Optional[str] = Field(None, max_length=20, description="Teléfono del trabajador")

    @validator('email')
    def validate_email(cls, v):
        """Valida el formato del email si se proporciona"""
        if v and '@' not in v:
            raise ValueError('Email inválido')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan",
                "apellido": "Pérez",
                "cedula": "1234567890",
                "cargo": "operaria",
                "salario": 56000.0,
                "email": "juan@example.com",
                "telefono": "3001234567"
            }
        }


class WorkerUpdate(BaseModel):
    """Schema para actualizar un trabajador"""
    nombre: Optional[str] = Field(None, min_length=1, max_length=100)
    apellido: Optional[str] = Field(None, max_length=100)
    cargo: Optional[str] = Field(None, min_length=1, max_length=100)
    salario: Optional[float] = Field(None, gt=0)
    email: Optional[str] = Field(None, max_length=100)
    telefono: Optional[str] = Field(None, max_length=20)
    activo: Optional[bool] = None
    reference_id: Optional[str] = Field(None, max_length=50)

    @validator('email')
    def validate_email(cls, v):
        """Valida el formato del email si se proporciona"""
        if v and '@' not in v:
            raise ValueError('Email inválido')
        return v

    class Config:
        json_schema_extra = {
            "example": {
                "nombre": "Juan",
                "cargo": "operaria",
                "salario": 58000.0
            }
        }


class WorkerResponse(BaseModel):
    """Schema para la respuesta de un trabajador individual"""
    id: int = Field(..., description="ID del trabajador")
    nombre: str = Field(..., description="Nombre del trabajador")
    apellido: Optional[str] = Field(None, description="Apellido del trabajador")
    cedula: str = Field(..., description="Cédula del trabajador")
    cargo: str = Field(..., description="Cargo del trabajador")
    salario: float = Field(..., description="Salario del trabajador")
    email: Optional[str] = Field(None, description="Email del trabajador")
    telefono: Optional[str] = Field(None, description="Teléfono del trabajador")
    activo: Optional[bool] = Field(True, description="Estado del trabajador")
    

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Juan",
                "apellido": "Pérez",
                "cedula": "1234567890",
                "cargo": "operaria",
                "salario": 56000.0,
                "email": "juan@example.com",
                "telefono": "3001234567",
                "activo": True,
            }
        }


class WorkerListResponse(BaseModel):
    """Schema para la respuesta de un trabajador en lista"""
    id: int = Field(..., description="ID del trabajador")
    nombre: str = Field(..., description="Nombre del trabajador")
    apellido: Optional[str] = Field(None, description="Apellido del trabajador")
    cedula: str = Field(..., description="Cédula del trabajador")
    cargo: str = Field(..., description="Cargo del trabajador")
    salario: Optional[float] = Field(None, description="Salario del trabajador")
    email: Optional[str] = Field(None, description="Email del trabajador")
    telefono: Optional[str] = Field(None, description="Teléfono del trabajador")
    activo: Optional[bool] = Field(True, description="Estado del trabajador")

    class Config:
        from_attributes = True


class WorkerCrudResponse(BaseModel):
    """Schema para la respuesta de operaciones CRUD (singular)"""
    success: bool = Field(..., description="Indicador de éxito de la operación")
    message: str = Field(..., description="Mensaje descriptivo de la operación")
    data: Optional[WorkerResponse] = Field(None, description="Datos del trabajador")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Trabajador creado exitosamente",
                "data": {
                    "id": 1,
                    "nombre": "Juan",
                    "apellido": "Pérez",
                    "cedula": "1234567890",
                    "cargo": "operaria",
                    "salario": 56000.0,
                    "email": "juan@example.com",
                    "telefono": "3001234567",
                    "activo": True,
                    "reference_id": 1232131231
                    
                }
            }
        }


class WorkerListCrudResponse(BaseModel):
    """Schema para la respuesta de operaciones CRUD (lista)"""
    success: bool = Field(..., description="Indicador de éxito de la operación")
    message: str = Field(..., description="Mensaje descriptivo de la operación")
    data: List[WorkerListResponse] = Field(..., description="Lista de trabajadores")
    total: int = Field(..., description="Número total de trabajadores")

    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "message": "Trabajadores obtenidos exitosamente",
                "data": [
                    {
                        "id": 1,
                        "nombre": "Juan",
                        "apellido": "Pérez",
                        "cedula": "1234567890",
                        "cargo": "operaria",
                        "salario": 56000.0,
                        "email": "juan@example.com",
                        "telefono": "3001234567",
                        "activo": True
                    }
                ],
                "total": 1
            }
        }
