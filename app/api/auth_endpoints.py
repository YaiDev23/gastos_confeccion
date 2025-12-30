from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from app.api.schemas.user_schema import UserLogin
from app.db.connection import get_db
from app.service.user_service import UserService

router = APIRouter()


@router.post("/auth/login")
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    """
    Endpoint para autenticar un usuario
    """
    result = UserService.verificar_credenciales(db, user_data)
    
    if result["success"]:
        usuario = result["data"]
        return {
            "success": True,
            "message": "Autenticación exitosa",
            "data": {
                "id_user": usuario.id_user,
                "username": usuario.username,
                "rol": usuario.rol,
                "estado": usuario.estado
            }
        }
    else:
        return JSONResponse(
            status_code=401,
            content={
                "success": False,
                "error": result.get("error", "Credenciales inválidas")
            }
        )


@router.post("/auth/logout")
async def logout():
    """
    Endpoint para cerrar sesión (se maneja en el cliente)
    """
    return {
        "success": True,
        "message": "Sesión cerrada correctamente"
    }
