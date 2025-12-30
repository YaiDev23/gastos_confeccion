from sqlalchemy.orm import Session
from app.db.models.factory_model import Factory


class FactoryService:
    """Servicio para gestionar operaciones de fábricas/talleres"""

    @staticmethod
    def get_all_deliveries(db: Session):
        """Obtener todos los talleres"""
        try:
            factories = db.query(Factory).all()
            return factories
        except Exception as e:
            raise Exception(f"Error al obtener talleres: {str(e)}")

    @staticmethod
    def create_delivery(db: Session, factory_data):
        """Crear un nuevo taller"""
        try:
            new_factory = Factory(owner=factory_data.owner)
            db.add(new_factory)
            db.commit()
            db.refresh(new_factory)
            return new_factory
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al crear taller: {str(e)}")

    @staticmethod
    def get_delivery_by_id(db: Session, factory_id: int):
        """Obtener un taller por ID"""
        try:
            factory = db.query(Factory).filter(Factory.id_factory == factory_id).first()
            return factory
        except Exception as e:
            raise Exception(f"Error al obtener taller: {str(e)}")

    @staticmethod
    def delete_delivery(db: Session, factory_id: int) -> bool:
        """Eliminar un taller por ID"""
        try:
            factory = db.query(Factory).filter(Factory.id_factory == factory_id).first()
            if not factory:
                return False
            db.delete(factory)
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al eliminar taller: {str(e)}")

    @staticmethod
    def update_delivery(db: Session, factory_id: int, factory_data):
        """Actualizar un taller"""
        try:
            factory = db.query(Factory).filter(Factory.id_factory == factory_id).first()
            if not factory:
                return None
            if factory_data.owner:
                factory.owner = factory_data.owner
            db.commit()
            db.refresh(factory)
            return factory
        except Exception as e:
            db.rollback()
            raise Exception(f"Error al actualizar taller: {str(e)}")
