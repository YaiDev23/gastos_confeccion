from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.api.schemas.delivery_schemas import DeliveredPiecesCreate, DeliveredPiecesResponse
from app.service.delivery_service import DeliveryService

router = APIRouter()


@router.get("/deliveries")
async def get_deliveries(db: Session = Depends(get_db)):
    """Obtener todas las entregas"""
    deliveries = DeliveryService.get_all_deliveries(db)
    return deliveries


@router.post("/deliveries", response_model=DeliveredPiecesResponse)
async def create_delivery(delivery: DeliveredPiecesCreate, db: Session = Depends(get_db)):
    """Crear una nueva entrega"""
    try:
        new_delivery = DeliveryService.create_delivery(db, delivery)
        return new_delivery
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/deliveries/{delivery_id}", response_model=DeliveredPiecesResponse)
async def get_delivery(delivery_id: int, db: Session = Depends(get_db)):
    """Obtener una entrega por ID"""
    delivery = DeliveryService.get_delivery_by_id(db, delivery_id)
    if not delivery:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return delivery


@router.delete("/deliveries/{delivery_id}")
async def delete_delivery(delivery_id: int, db: Session = Depends(get_db)):
    """Eliminar una entrega"""
    success = DeliveryService.delete_delivery(db, delivery_id)
    if not success:
        raise HTTPException(status_code=404, detail="Entrega no encontrada")
    return {"message": "Entrega eliminada correctamente", "id_delivery": delivery_id}