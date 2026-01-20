from sqlalchemy import Column, Integer, String
from app.db.models.base import Base


class User(Base):
    """Modelo para usuarios"""
    __tablename__ = "users"
    
    id_user = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(100), nullable=False, unique=True)
    psw = Column(String(255), nullable=False)
    email = Column(String(255), nullable=True)
    rol = Column(String(50), nullable=False)
    estado = Column(Integer, default=1, nullable=False)  # 1 = activo, 0 = inactivo

    def __repr__(self):
        return f"<User(id_user={self.id_user}, username='{self.username}', rol='{self.rol}', estado={self.estado})>"
