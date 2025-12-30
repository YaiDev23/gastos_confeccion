from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from app.db.models.user_model import User
from app.api.schemas.user_schema import UserCreate, UserUpdate, UserLogin
from typing import Optional, List, Dict, Any


class UserService:
    """Servicio para gestionar operaciones de usuarios"""
    
    @staticmethod
    def crear_usuario(db: Session, user_data: UserCreate) -> Dict[str, Any]:
        """
        Crea un nuevo usuario en la base de datos
        """
        try:
            nuevo_usuario = User(
                username=user_data.username,
                psw=user_data.psw,
                rol=user_data.rol,
                estado=user_data.estado
            )
            
            db.add(nuevo_usuario)
            db.commit()
            db.refresh(nuevo_usuario)
            
            return {
                "success": True,
                "data": nuevo_usuario
            }
        except IntegrityError as e:
            db.rollback()
            return {
                "success": False,
                "error": "El nombre de usuario ya existe"
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def obtener_usuario(db: Session, usuario_id: int) -> Optional[User]:
        """
        Obtiene un usuario por su ID
        """
        return db.query(User).filter(User.id_user == usuario_id).first()
    
    @staticmethod
    def obtener_usuario_por_username(db: Session, username: str) -> Optional[User]:
        """
        Obtiene un usuario por su nombre de usuario
        """
        return db.query(User).filter(User.username == username).first()
    
    @staticmethod
    def obtener_todos_usuarios(db: Session) -> List[User]:
        """
        Obtiene todos los usuarios
        """
        return db.query(User).all()
    
    @staticmethod
    def obtener_usuarios_activos(db: Session) -> List[User]:
        """
        Obtiene todos los usuarios activos
        """
        return db.query(User).filter(User.estado == 'activo').all()
    
    @staticmethod
    def actualizar_usuario(db: Session, usuario_id: int, user_data: UserUpdate) -> Dict[str, Any]:
        """
        Actualiza un usuario existente
        """
        try:
            usuario = db.query(User).filter(User.id_user == usuario_id).first()
            
            if not usuario:
                return {
                    "success": False,
                    "error": "Usuario no encontrado"
                }
            
            # Actualizar solo los campos que se proporcionan
            if user_data.username is not None:
                usuario.username = user_data.username
            if user_data.psw is not None:
                usuario.psw = user_data.psw
            if user_data.rol is not None:
                usuario.rol = user_data.rol
            if user_data.estado is not None:
                usuario.estado = user_data.estado
            
            db.commit()
            db.refresh(usuario)
            
            return {
                "success": True,
                "data": usuario
            }
        except IntegrityError:
            db.rollback()
            return {
                "success": False,
                "error": "El nombre de usuario ya existe"
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def eliminar_usuario(db: Session, usuario_id: int) -> Dict[str, Any]:
        """
        Elimina un usuario (lo marca como inactivo)
        """
        try:
            usuario = db.query(User).filter(User.id_user == usuario_id).first()
            
            if not usuario:
                return {
                    "success": False,
                    "error": "Usuario no encontrado"
                }
            
            # Cambiar estado a inactivo en lugar de eliminar
            usuario.estado = 'inactivo'
            db.commit()
            
            return {
                "success": True,
                "message": "Usuario desactivado correctamente"
            }
        except Exception as e:
            db.rollback()
            return {
                "success": False,
                "error": str(e)
            }
    
    @staticmethod
    def verificar_credenciales(db: Session, user_data: UserLogin) -> Dict[str, Any]:
        """
        Verifica las credenciales de un usuario (login)
        """
        usuario = db.query(User).filter(
            User.username == user_data.username,
            User.estado == 'activo'
        ).first()
        
        if not usuario:
            return {
                "success": False,
                "error": "Usuario o contraseña incorrectos"
            }
        
        # Comparar contraseña (en producción usar bcrypt)
        if usuario.psw != user_data.psw:
            return {
                "success": False,
                "error": "Usuario o contraseña incorrectos"
            }
        
        return {
            "success": True,
            "data": usuario
        }
