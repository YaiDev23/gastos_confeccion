from pydantic import BaseModel
from datetime import date
from typing import Optional, Union


class DeliveredPiecesBase(BaseModel):
    owner: str
    date: date
    lot: Optional[str] = None
    type: Optional[str] = None
    color: Optional[str] = None
    annotation: Optional[str] = None
    type_fabric: Optional[str] = None
    rib: Optional[str] = None
    
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
    id_group: Optional[Union[int, str]] = None


class DeliveredPiecesCreate(DeliveredPiecesBase):
    pass


class DeliveredPiecesUpdate(BaseModel):
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


class DeliveredPiecesResponse(DeliveredPiecesBase):
    id_delivery: int
    
    class Config:
        from_attributes = True
