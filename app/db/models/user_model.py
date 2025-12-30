from sqlalchemy import Column, Integer, String, Enum
from app.db.models.base import Base


class User(Base):
    """Modelo para usuarios"""
    __tablename__ = "users"
    
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    psw = Column(String(255), nullable=False)
    rol = Column(String(50), nullable=False)
    estado = Column(Enum('activo', 'inactivo'), default='activo', nullable=False)

    def __repr__(self):
        return f"<User(id_user={self.id_user}, username='{self.username}', rol='{self.rol}', estado='{self.estado}')>"
