from fastapi import HTTPException, status
from functools import wraps
from typing import List, Callable


class RolePermissions:
    """Definición de permisos por rol"""
    
    PERMISSIONS = {
        'super': {
            'ver_trabajadores': True,
            'agregar_trabajador': True,
            'editar_trabajador': True,
            'eliminar_trabajador': True,
            'gestionar_entregas': True,
            'ver_calculos': True,
            'crear_usuario': True,
            'eliminar_usuario': True
        },
        'admin': {
            'ver_trabajadores': False,
            'agregar_trabajador': True,
            'editar_trabajador': False,
            'eliminar_trabajador': False,
            'gestionar_entregas': True,
            'ver_calculos': False,
            'crear_usuario': False,
            'eliminar_usuario': False
        },
        'user': {
            'ver_trabajadores': False,
            'agregar_trabajador': False,
            'editar_trabajador': False,
            'eliminar_trabajador': False,
            'gestionar_entregas': False,
            'ver_calculos': False,
            'crear_usuario': False,
            'eliminar_usuario': False
        }
    }

    @staticmethod
    def check_permission(rol: str, permission: str) -> bool:
        """Verifica si un rol tiene permiso para una acción"""
        if rol not in RolePermissions.PERMISSIONS:
            return False
        return RolePermissions.PERMISSIONS[rol].get(permission, False)

    @staticmethod
    def require_roles(allowed_roles: List[str]):
        """Decorator para verificar que el usuario tenga uno de los roles permitidos"""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                # Obtener rol del contexto o parámetros
                rol = kwargs.get('user_rol')
                if not rol or rol not in allowed_roles:
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail="No tienes permisos para acceder a este recurso"
                    )
                return await func(*args, **kwargs)
            return wrapper
        return decorator

    @staticmethod
    def require_permission(permission: str):
        """Decorator para verificar un permiso específico"""
        def decorator(func: Callable):
            @wraps(func)
            async def wrapper(*args, **kwargs):
                rol = kwargs.get('user_rol')
                if not RolePermissions.check_permission(rol, permission):
                    raise HTTPException(
                        status_code=status.HTTP_403_FORBIDDEN,
                        detail=f"No tienes permiso para: {permission}"
                    )
                return await func(*args, **kwargs)
            return wrapper
        return decorator
