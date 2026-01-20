from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class AsistenciaBase(BaseModel):
    worker: str
    arrival_time: datetime
    departure_time: Optional[datetime] = None


class AsistenciaCreate(BaseModel):
    worker_id: int


class AsistenciaCodigoBarras(BaseModel):
    reference_id: str


class AsistenciaSalida(BaseModel):
    id_assistence: int


class AsistenciaResponse(BaseModel):
    id_assistence: int
    worker: str
    arrival_time: datetime
    departure_time: Optional[datetime]
    
    class Config:
        from_attributes = True
