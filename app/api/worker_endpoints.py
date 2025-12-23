from fastapi import APIRouter, Request, Form, HTTPException, status


from app.db.connection import get_db
from app.service.worker_service import WorkerService

from app.api.schemas.worker_schema import (
    WorkerCreate, WorkerUpdate, WorkerResponse, WorkerListResponse,
    WorkerCrudResponse, WorkerListCrudResponse
)
router = APIRouter()

# =====================
# ENDPOINTS DE TRABAJADORES
# =====================

@router.post("/trabajadores/crear", response_model=WorkerCrudResponse, status_code=status.HTTP_201_CREATED)
async def crear_nuevo_trabajador(worker: WorkerCreate):
    """
    Crea un nuevo trabajador en la base de datos.
    
    Parámetros:
    - nombre: Nombre del trabajador
    - apellido: Apellido del trabajador
    - cedula: Cédula del trabajador (única)
    - cargo: Cargo del trabajador
    - salario: Salario del trabajador
    - email: Email del trabajador (opcional)
    - telefono: Teléfono del trabajador (opcional)
    """
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = WorkerService.crear_trabajador(db, worker)
        
        if resultado["success"]:
            return WorkerCrudResponse(
                success=True,
                message="Trabajador creado exitosamente",
                data=WorkerResponse.from_orm(resultado["data"])
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultado.get("error", "Error al crear trabajador")
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.get("/trabajadores", response_model=WorkerListCrudResponse)
async def obtener_lista_trabajadores():
    """Obtiene la lista de todos los trabajadores activos"""
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = WorkerService.obtener_lista_trabajadores(db)
        if resultado["success"]:
            trabajadores = [WorkerListResponse.from_orm(t) for t in resultado["data"]]
            return WorkerListCrudResponse(
                success=True,
                message="Trabajadores obtenidos exitosamente",
                data=trabajadores,
                total=len(trabajadores)
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=resultado.get("error", "Error al obtener trabajadores")
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.get("/trabajadores/{trabajador_id}", response_model=WorkerCrudResponse)
async def obtener_info_trabajador(trabajador_id: int):
    """Obtiene la información de un trabajador específico"""
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = WorkerService.obtener_trabajador(db, trabajador_id)
        
        if resultado["success"]:
            return WorkerCrudResponse(
                success=True,
                message="Trabajador obtenido exitosamente",
                data=WorkerResponse.from_orm(resultado["data"])
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resultado.get("error", "Trabajador no encontrado")
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.put("/trabajadores/{trabajador_id}", response_model=WorkerCrudResponse)
async def actualizar_info_trabajador(
    trabajador_id: int,
    worker: WorkerUpdate
):
    """Actualiza la información de un trabajador"""
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = WorkerService.actualizar_trabajador(db, trabajador_id, worker)
        
        if resultado["success"]:
            return WorkerCrudResponse(
                success=True,
                message="Trabajador actualizado exitosamente",
                data=WorkerResponse.from_orm(resultado["data"])
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resultado.get("error", "Trabajador no encontrado")
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.delete("/trabajadores/{trabajador_id}", response_model=WorkerCrudResponse)
async def eliminar_info_trabajador(trabajador_id: int):
    """Elimina (desactiva) un trabajador"""
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = WorkerService.eliminar_trabajador(db, trabajador_id)
        
        if resultado["success"]:
            return WorkerCrudResponse(
                success=True,
                message="Trabajador eliminado exitosamente",
                data=None
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=resultado.get("error", "Trabajador no encontrado")
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)
