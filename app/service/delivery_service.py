from sqlalchemy.orm import Session
from app.db.models.delivery_models import DeliveredPieces
from app.api.schemas.delivery_schemas import DeliveredPiecesCreate, DeliveredPiecesUpdate


class DeliveryService:
    @staticmethod
    def create_delivery(db: Session, delivery_data: DeliveredPiecesCreate) -> DeliveredPieces:
        """Crear una nueva entrega de piezas"""
        db_delivery = DeliveredPieces(**delivery_data.model_dump())
        db.add(db_delivery)
        db.commit()
        db.refresh(db_delivery)
        return db_delivery
    
    @staticmethod
    def get_all_deliveries(db: Session):
        """Obtener todas las entregas"""
        return db.query(DeliveredPieces).all()
    
    @staticmethod
    def get_delivery_by_id(db: Session, delivery_id: int) -> DeliveredPieces:
        """Obtener una entrega por ID"""
        return db.query(DeliveredPieces).filter(DeliveredPieces.id_delivery == delivery_id).first()
    
    @staticmethod
    def update_delivery(db: Session, delivery_id: int, delivery_data: DeliveredPiecesUpdate) -> DeliveredPieces:
        """Actualizar una entrega"""
        db_delivery = DeliveryService.get_delivery_by_id(db, delivery_id)
        if db_delivery:
            update_data = delivery_data.model_dump(exclude_none=True)
            for field, value in update_data.items():
                setattr(db_delivery, field, value)
            db.commit()
            db.refresh(db_delivery)
        return db_delivery
    
    @staticmethod
    def delete_delivery(db: Session, delivery_id: int) -> bool:
        """Eliminar una entrega"""
        db_delivery = DeliveryService.get_delivery_by_id(db, delivery_id)
        if db_delivery:
            db.delete(db_delivery)
            db.commit()
            return True
        return False
