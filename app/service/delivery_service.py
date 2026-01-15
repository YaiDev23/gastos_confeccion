from sqlalchemy.orm import Session
from app.db.models.delivery_models import DeliveredPieces
from app.api.schemas.delivery_schemas import DeliveredPiecesCreate, DeliveredPiecesUpdate
from datetime import datetime
import pytz


class DeliveryService:
    # Zona horaria de Bogotá
    BOGOTA_TZ = pytz.timezone('America/Bogota')
    
    @staticmethod
    def get_bogota_time():
        """Obtener la fecha y hora actual en Bogotá"""
        return datetime.now(DeliveryService.BOGOTA_TZ).replace(tzinfo=None)
    
    @staticmethod
    def create_delivery(db: Session, delivery_data: DeliveredPiecesCreate) -> DeliveredPieces:
        """Crear una nueva entrega de piezas"""
        data_dict = delivery_data.model_dump()
        # Establecer valor por defecto de status
        if 'status' not in data_dict or data_dict['status'] is None:
            data_dict['status'] = 'active'
        # Registrar la fecha de modificación y usuario que creó
        data_dict['modification_date'] = DeliveryService.get_bogota_time()
        if 'modified_by' not in data_dict:
            data_dict['modified_by'] = 'system'
        
        db_delivery = DeliveredPieces(**data_dict)
        db.add(db_delivery)
        db.commit()
        db.refresh(db_delivery)
        return db_delivery
    
    @staticmethod
    def get_all_deliveries(db: Session):
        """Obtener todas las entregas activas"""
        return db.query(DeliveredPieces).filter(DeliveredPieces.status == 'active').all()
    
    @staticmethod
    def get_delivery_by_id(db: Session, delivery_id: int) -> DeliveredPieces:
        """Obtener una entrega por ID"""
        return db.query(DeliveredPieces).filter(DeliveredPieces.id_delivery == delivery_id).first()
    
    @staticmethod
    def update_delivery(db: Session, delivery_id: int, delivery_data: DeliveredPiecesUpdate) -> DeliveredPieces:
        """Actualizar una entrega con auditoría"""
        db_delivery = DeliveryService.get_delivery_by_id(db, delivery_id)
        if db_delivery:
            update_data = delivery_data.model_dump(exclude_none=True)
            # Registrar fecha de modificación en Bogotá
            update_data['modification_date'] = DeliveryService.get_bogota_time()
            # Si no se proporciona modified_by, usar 'system'
            if 'modified_by' not in update_data or update_data['modified_by'] is None:
                update_data['modified_by'] = 'system'
            
            for field, value in update_data.items():
                setattr(db_delivery, field, value)
            db.commit()
            db.refresh(db_delivery)
        return db_delivery
    
    @staticmethod
    def delete_delivery(db: Session, delivery_id: int, modified_by: str = None) -> bool:
        """Marcar una entrega como inactiva en lugar de eliminarla (soft delete)"""
        db_delivery = DeliveryService.get_delivery_by_id(db, delivery_id)
        if db_delivery:
            db_delivery.status = 'inactive'
            db_delivery.modification_date = DeliveryService.get_bogota_time()
            db_delivery.modified_by = modified_by or 'system'
            db.commit()
            return True
        return False
