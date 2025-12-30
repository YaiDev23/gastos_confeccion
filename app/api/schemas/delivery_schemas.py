from pydantic import BaseModel
from datetime import date
from typing import Optional


class DeliveredPiecesBase(BaseModel):
    owner: str
    date: date
    lot: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None
    annotation: Optional[str] = None
    
    # Size range 6-12 to 36-48
    sz6_12: int = 0
    sz12_18: int = 0
    sz18_24: int = 0
    sz24_36: int = 0
    sz36_48: int = 0
    
    # Individual sizes 2 to 18
    sz2: int = 0
    sz4: int = 0
    sz6: int = 0
    sz8: int = 0
    sz10: int = 0
    sz12: int = 0
    sz14: int = 0
    sz16: int = 0
    sz18: int = 0


class DeliveredPiecesCreate(DeliveredPiecesBase):
    pass


class DeliveredPiecesUpdate(BaseModel):
    owner: Optional[str] = None
    date: Optional[date] = None
    lot: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None
    annotation: Optional[str] = None
    
    # Size range 6-12 to 36-48
    sz6_12: Optional[int] = None
    sz12_18: Optional[int] = None
    sz18_24: Optional[int] = None
    sz24_36: Optional[int] = None
    sz36_48: Optional[int] = None
    
    # Individual sizes 2 to 18
    sz2: Optional[int] = None
    sz4: Optional[int] = None
    sz6: Optional[int] = None
    sz8: Optional[int] = None
    sz10: Optional[int] = None
    sz12: Optional[int] = None
    sz14: Optional[int] = None
    sz16: Optional[int] = None
    sz18: Optional[int] = None


class DeliveredPiecesResponse(DeliveredPiecesBase):
    id_delivery: int
    
    class Config:
        from_attributes = True
