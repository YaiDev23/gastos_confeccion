from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.connection import get_db
from app.api.schemas.user_schema import UserCreate, UserUpdate, UserResponse, UserLogin, FactoryLogin
from app.service.user_service import UserService
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/users", response_model=list[UserResponse])
async def get_all_users(db: Session = Depends(get_db)):
    """Obtener todos los usuarios"""
    users = UserService.obtener_todos_usuarios(db)
    return users


@router.get("/users/active", response_model=list[UserResponse])
async def get_active_users(db: Session = Depends(get_db)):
    """Obtener todos los usuarios activos"""
    users = UserService.obtener_usuarios_activos(db)
    return users


@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int, db: Session = Depends(get_db)):
    """Obtener un usuario por ID"""
    user = UserService.obtener_usuario(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/users", response_model=UserResponse)
async def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """Crear un nuevo usuario"""
    try:
        logger.info(f"Creando usuario: {user.username}")
        result = UserService.crear_usuario(db, user)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result["data"]
    except Exception as e:
        logger.error(f"Error al crear usuario: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.put("/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: int, user: UserUpdate, db: Session = Depends(get_db)):
    """Actualizar un usuario existente"""
    try:
        logger.info(f"Actualizando usuario con ID: {user_id}")
        result = UserService.actualizar_usuario(db, user_id, user)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return result["data"]
    except Exception as e:
        logger.error(f"Error al actualizar usuario: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: Session = Depends(get_db)):
    """Eliminar un usuario (marcarlo como inactivo)"""
    try:
        logger.info(f"Eliminando usuario con ID: {user_id}")
        result = UserService.eliminar_usuario(db, user_id)
        
        if not result["success"]:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {"message": result["message"], "id_user": user_id}
    except Exception as e:
        logger.error(f"Error al eliminar usuario: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/users/login")
async def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """Verificar credenciales de usuario (login)"""
    try:
        logger.info(f"Intento de login para usuario: {credentials.username}")
        result = UserService.verificar_credenciales(db, credentials)
        
        if not result["success"]:
            raise HTTPException(status_code=401, detail=result["error"])
        
        user = result["data"]
        return {
            "success": True,
            "data": {
                "id_user": user.id_user,
                "username": user.username,
                "rol": user.rol,
                "estado": user.estado
            }
        }
    except Exception as e:
        logger.error(f"Error en login: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))


@router.get("/users/username/{username}", response_model=UserResponse)
async def get_user_by_username(username: str, db: Session = Depends(get_db)):
    """Obtener un usuario por su nombre de usuario"""
    user = UserService.obtener_usuario_por_username(db, username)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return user


@router.post("/factory/login")
async def factory_login(credentials: FactoryLogin, db: Session = Depends(get_db)):
    """Verificar acceso de taller por número de documento"""
    try:
        logger.info(f"Intento de login para taller con documento: {credentials.document}")
        result = UserService.verificar_taller_por_documento(db, credentials.document)
        
        if not result["success"]:
            raise HTTPException(status_code=401, detail=result["error"])
        
        factory_data = result["data"]
        return {
            "success": True,
            "data": factory_data
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en login de taller: {str(e)}", exc_info=True)
        raise HTTPException(status_code=400, detail=str(e))
