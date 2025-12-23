from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from datetime import datetime
from app.db.base import Base
import pytz


class Assistence(Base):
    """Modelo para asistencia de trabajadores"""
    __tablename__ = "assistence"
    
    id_assistence = Column(Integer, primary_key=True, autoincrement=True)
    worker = Column(String(100), nullable=False)
    arrival_time = Column(DateTime, nullable=False)
    departure_time = Column(DateTime, nullable=True)
    fecha_creacion = Column(DateTime, default=lambda: datetime.now(pytz.timezone('America/Bogota')))
    
    def __repr__(self):
        return f"<Assistence(id={self.id_assistence}, worker='{self.worker}', arrival_time='{self.arrival_time}')>"
