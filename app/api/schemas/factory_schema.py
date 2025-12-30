from pydantic import BaseModel, Field
from typing import Optional


class FactoryCreate(BaseModel):
    """Schema para crear una nueva fábrica"""
    owner: str = Field(..., min_length=1, max_length=100, description="Propietario de la fábrica")

    class Config:
        json_schema_extra = {
            "example": {
                "owner": "Juan Pérez"
            }
        }


class FactoryUpdate(BaseModel):
    """Schema para actualizar una fábrica"""
    owner: Optional[str] = Field(None, min_length=1, max_length=100, description="Propietario de la fábrica")

    class Config:
        json_schema_extra = {
            "example": {
                "owner": "Juan Pérez"
            }
        }


class FactoryResponse(BaseModel):
    """Schema para respuesta de fábrica"""
    id_factory: int = Field(..., description="ID de la fábrica")
    owner: str = Field(..., description="Propietario de la fábrica")

    class Config:
        from_attributes = True
        json_schema_extra = {
            "example": {
                "id_factory": 1,
                "owner": "Juan Pérez"
            }
        }
