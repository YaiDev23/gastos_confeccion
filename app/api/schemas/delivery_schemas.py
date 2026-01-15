from pydantic import BaseModel
from datetime import date, datetime
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
    status: str = "active"


class DeliveredPiecesCreate(DeliveredPiecesBase):
    modified_by: Optional[str] = None


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
    modified_by: Optional[str] = None


class DeliveredPiecesResponse(DeliveredPiecesBase):
    id_delivery: int
    modification_date: Optional[datetime] = None
    modified_by: Optional[str] = None
    
    class Config:
        from_attributes = True
