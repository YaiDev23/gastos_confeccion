from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.api.schemas.factory_schema import FactoryCreate, FactoryUpdate, FactoryResponse
from app.service.factory_service import FactoryService

router = APIRouter(tags=["Factories"])



@router.get("/factories", response_model=list[FactoryResponse])
async def get_factories(db: Session = Depends(get_db)):
    """Obtener todos los talleres"""
    try:
        factories = FactoryService.get_all_deliveries(db)
        return factories
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/factory", response_model=FactoryResponse)
async def create_factory(factory: FactoryCreate, db: Session = Depends(get_db)):
    """Crear un nuevo taller"""
    try:
        new_factory = FactoryService.create_delivery(db, factory)
        return new_factory
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/factories/{factory_id}", response_model=FactoryResponse)
async def get_factory(factory_id: int, db: Session = Depends(get_db)):
    """Obtener un taller por ID"""
    try:
        factory = FactoryService.get_delivery_by_id(db, factory_id)
        if not factory:
            raise HTTPException(status_code=404, detail="Taller no encontrado")
        return factory
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/factories/{factory_id}", response_model=FactoryResponse)
async def update_factory(factory_id: int, factory: FactoryUpdate, db: Session = Depends(get_db)):
    """Actualizar un taller"""
    try:
        updated_factory = FactoryService.update_delivery(db, factory_id, factory)
        if not updated_factory:
            raise HTTPException(status_code=404, detail="Taller no encontrado")
        return updated_factory
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/factories/{factory_id}")
async def delete_factory(factory_id: int, db: Session = Depends(get_db)):
    """Eliminar un taller"""
    try:
        success = FactoryService.delete_delivery(db, factory_id)
        if not success:
            raise HTTPException(status_code=404, detail="Taller no encontrado")
        return {"message": "Taller eliminado correctamente", "id_factory": factory_id}
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))