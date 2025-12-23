from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models.worker_model import Worker
from app.api.schemas.worker_schema import WorkerCreate, WorkerUpdate
from typing import Optional, List, Dict, Any


class WorkerService:
    """Servicio para gestionar operaciones de trabajadores"""
    
    @staticmethod
    def crear_trabajador(db: Session, worker_data: WorkerCreate) -> Dict[str, Any]:
        """
        Crea un nuevo trabajador en la base de datos
        """
        try:
            nuevo_trabajador = Worker(
                nombre=worker_data.nombre,
                apellido=worker_data.apellido or "",
                cedula=worker_data.cedula,
                cargo=worker_data.cargo,
                salario=float(worker_data.salario),
                email=worker_data.email,
                telefono=worker_data.telefono
            )
            
            db.add(nuevo_trabajador)
            db.commit()
            db.refresh(nuevo_trabajador)
            
            return {
                "success": True,
                "data": nuevo_trabajador
            }
        except IntegrityError as e:
            db.rollback()
            return {
                "success": False,
                "error": "La cédula ya existe en el sistema"
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def obtener_trabajador(db: Session, trabajador_id: int) -> Dict[str, Any]:
        """
        Obtiene la información de un trabajador específico
        """
        trabajador = db.query(Worker).filter(
            Worker.id == trabajador_id,
            Worker.activo == True
        ).first()
        
        if not trabajador:
            return {
                "success": False,
                "error": "Trabajador no encontrado"
            }
        
        return {
            "success": True,
            "data": trabajador
        }
    
    @staticmethod
    def obtener_lista_trabajadores(db: Session) -> Dict[str, Any]:
        """
        Obtiene la lista de todos los trabajadores activos
        """
        try:
            trabajadores = db.query(Worker).filter(Worker.activo == True).all()
            
            return {
                "success": True,
                "data": trabajadores
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def actualizar_trabajador(db: Session, trabajador_id: int, worker_data: WorkerUpdate) -> Dict[str, Any]:
        """
        Actualiza la información de un trabajador
        """
        try:
            trabajador = db.query(Worker).filter(
                Worker.id == trabajador_id,
                Worker.activo == True
            ).first()
            
            if not trabajador:
                return {
                    "success": False,
                    "error": "Trabajador no encontrado"
                }
            
            # Actualizar solo los campos proporcionados
            update_data = worker_data.dict(exclude_unset=True)
            for field, value in update_data.items():
                if value is not None:
                    if field == "salario":
                        setattr(trabajador, field, float(value))
                    else:
                        setattr(trabajador, field, value)
            
            db.commit()
            db.refresh(trabajador)
            
            return {
                "success": True,
                "data": trabajador
            }
        except IntegrityError as e:
            db.rollback()
            return {
                "success": False,
                "error": "Error de integridad: la cédula puede estar duplicada"
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def eliminar_trabajador(db: Session, trabajador_id: int) -> Dict[str, Any]:
        """
        Elimina (desactiva) un trabajador
        """
        try:
            trabajador = db.query(Worker).filter(
                Worker.id == trabajador_id,
                Worker.activo == True
            ).first()
            
            if not trabajador:
                return {
                    "success": False,
                    "error": "Trabajador no encontrado"
                }
            
            trabajador.activo = False
            db.commit()
            
            return {
                "success": True,
                "data": trabajador
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
