from sqlalchemy import Column, Integer, String
from app.db.models.base import Base


class Factory(Base):
    """Modelo para fábricas"""
    __tablename__ = "factories"
    
    id_factory = Column(Integer, primary_key=True, autoincrement=True)
    owner = Column(String(100), nullable=False)

    def __repr__(self):
        return f"<Factory(id_factory={self.id_factory}, owner='{self.owner}')>"
