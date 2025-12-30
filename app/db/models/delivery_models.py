from sqlalchemy import Column, Integer, String, Date
from app.db.models.base import Base
from datetime import date


class DeliveredPieces(Base):
    __tablename__ = "delivered_pieces"

    id_delivery = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String(100), nullable=False)
    date = Column(Date, nullable=False)
    lot = Column(String(50), nullable=True)
    type = Column(String(50), nullable=True)
    color = Column(String(50), nullable=True)
    annotation = Column(String(500), nullable=True)
    
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

    def __repr__(self):
        return f"<DeliveredPieces(id_delivery={self.id_delivery}, owner={self.owner}, date={self.date})>"
