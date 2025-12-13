from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import declared_attr
from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean
from datetime import datetime

class CustomBase:
    @declared_attr
    def __tablename__(cls):
        return cls.__name__.lower()

Base = declarative_base(cls=CustomBase)

class Worker(Base):
    """Modelo para trabajadores"""
    __tablename__ = "workers"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    nombre = Column(String(100), nullable=False)
    apellido = Column(String(100), nullable=False)
    cedula = Column(String(20), unique=True, nullable=False)
    email = Column(String(120), unique=True, nullable=True)
    telefono = Column(String(20), nullable=True)
    cargo = Column(String(100), nullable=False)
    salario = Column(Float, nullable=False)
    activo = Column(Boolean, default=True)
    fecha_ingreso = Column(DateTime, default=datetime.utcnow)
    fecha_creacion = Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f"<Worker(id={self.id}, nombre='{self.nombre}', cedula='{self.cedula}')>"
