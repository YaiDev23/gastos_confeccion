from sqlalchemy import Column, Integer, String, Date, DateTime
from app.db.models.base import Base
from datetime import date, datetime


class DeliveredPieces(Base):
    __tablename__ = "delivered_pieces"

    id_delivery = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    lot = Column(String(50), nullable=True)
    type = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    annotation = Column(String(500), nullable=True)
    type_fabric = Column(String(100), nullable=True)
    rib = Column(String(100), nullable=True)
    
    # Size range 6-12 to 36-48
    sz6_12 = Column(Integer, default=0)
    sz12_18 = Column(Integer, default=0)
    sz18_24 = Column(Integer, default=0)
    sz24_36 = Column(Integer, default=0)
    sz36_48 = Column(Integer, default=0)
    
    # Individual sizes 2 to 18
    sz2 = Column(Integer, default=0)
    sz4 = Column(Integer, default=0)
    sz6 = Column(Integer, default=0)
    sz8 = Column(Integer, default=0)
    sz10 = Column(Integer, default=0)
    sz12 = Column(Integer, default=0)
    sz14 = Column(Integer, default=0)
    sz16 = Column(Integer, default=0)
    sz18 = Column(Integer, default=0)
    id_group = Column(String(50), nullable=True)
    
    # Audit fields
    modification_date = Column(DateTime, nullable=True)
    modified_by = Column(String(100), nullable=True)
    status = Column(String(20), default="active", nullable=False)

    def __repr__(self):
        return f"<DeliveredPieces(id_delivery={self.id_delivery}, owner={self.owner}, date={self.date}, status={self.status})>"
