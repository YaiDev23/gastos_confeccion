from sqlalchemy import Column, Integer, String, DateTime, Boolean, Numeric
from datetime import datetime
from app.db.models.base import Base

class Worker(Base):
    """Modelo para trabajadores"""
    __tablename__ = "workers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cedula = Column(String(20), nullable=False, unique=True)
    telefono = Column(String(20), nullable=True)
    cargo = Column(String(100), nullable=False)
    salario = Column(Numeric(10, 2), nullable=False)
    activo = Column(Boolean, default=True, nullable=False)
    fecha_creacion = Column(DateTime, default=datetime.now, nullable=False)
    email = Column(String(100), nullable=True)
    reference_id = Column(String(50), nullable=True)

    def __repr__(self):
        return f"<Worker(id={self.id}, nombre='{self.nombre}', apellido='{self.apellido}', cedula='{self.cedula}')>"
