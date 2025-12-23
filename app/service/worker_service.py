from sqlalchemy.orm import Session
from app.db.base import Worker
from datetime import datetime


def crear_trabajador(
    db: Session,
    nombre: str,
    apellido: str,
    cedula: str,
    cargo: str,
    salario: float,
    email: str = None,
    telefono: str = None
) -> dict:
    """
    Crea un nuevo trabajador en la base de datos.
    
    Args:
        db: Sesión de SQLAlchemy
        nombre: Nombre del trabajador
        apellido: Apellido del trabajador
        cedula: Cédula única del trabajador
        cargo: Cargo del trabajador
        salario: Salario del trabajador
        email: Email del trabajador (opcional)
        telefono: Teléfono del trabajador (opcional)
    
    Returns:
        dict: Información del trabajador creado
        
    Raises:
        ValueError: Si la cédula ya existe
        Exception: Cualquier otro error de base de datos
    """
    try:
        # Verificar si la cédula ya existe
        trabajador_existente = db.query(Worker).filter(Worker.cedula == cedula).first()
        if trabajador_existente:
            return {
                "success": False,
                "error": f"Ya existe un trabajador con la cédula {cedula}",
                "data": None
            }
        
        # Crear nuevo trabajador
        nuevo_trabajador = Worker(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            email=email,
            telefono=telefono,
            cargo=cargo,
            salario=salario,
            activo=True,
            fecha_ingreso=datetime.utcnow(),
            fecha_creacion=datetime.utcnow()
        )
        
        # Agregar a la sesión y confirmar
        db.add(nuevo_trabajador)
        db.commit()
        db.refresh(nuevo_trabajador)
        
        return {
            "success": True,
            "error": None,
            "data": {
                "id": nuevo_trabajador.id,
                "nombre": nuevo_trabajador.nombre,
                "apellido": nuevo_trabajador.apellido,
                "cedula": nuevo_trabajador.cedula,
                "email": nuevo_trabajador.email,
                "telefono": nuevo_trabajador.telefono,
                "cargo": nuevo_trabajador.cargo,
                "salario": nuevo_trabajador.salario,
                "activo": nuevo_trabajador.activo,
                "fecha_ingreso": nuevo_trabajador.fecha_ingreso.isoformat(),
                "fecha_creacion": nuevo_trabajador.fecha_creacion.isoformat()
            }
        }
    
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error al crear trabajador: {str(e)}",
            "data": None
        }


def obtener_trabajador(db: Session, trabajador_id: int) -> dict:
    """Obtiene un trabajador por ID"""
    try:
        trabajador = db.query(Worker).filter(Worker.id == trabajador_id).first()
        if not trabajador:
            return {"success": False, "error": "Trabajador no encontrado", "data": None}
        
        return {
            "success": True,
            "error": None,
            "data": {
                "id": trabajador.id,
                "nombre": trabajador.nombre,
                "apellido": trabajador.apellido,
                "cedula": trabajador.cedula,
                "email": trabajador.email,
                "telefono": trabajador.telefono,
                "cargo": trabajador.cargo,
                "salario": trabajador.salario,
                "activo": trabajador.activo,
                "fecha_ingreso": trabajador.fecha_ingreso.isoformat(),
                "fecha_creacion": trabajador.fecha_creacion.isoformat()
            }
        }
    except Exception as e:
        return {"success": False, "error": str(e), "data": None}


def listar_trabajadores(db: Session) -> dict:
    """Lista todos los trabajadores activos"""
    try:
        trabajadores = db.query(Worker).filter(Worker.activo == True).all()
        
        datos = [
            {
                "id": t.id,
                "nombre": t.nombre,
                "apellido": t.apellido,
                "cedula": t.cedula,
                "email": t.email,
                "telefono": t.telefono,
                "cargo": t.cargo,
                "salario": t.salario
            }
            for t in trabajadores
        ]
        
        return {
            "success": True,
            "error": None,
            "data": datos,
            "cantidad": len(datos)
        }
    except Exception as e:
        return {"success": False, "error": str(e), "data": None, "cantidad": 0}


def actualizar_trabajador(db: Session, trabajador_id: int, **kwargs) -> dict:
    """Actualiza un trabajador existente"""
    try:
        trabajador = db.query(Worker).filter(Worker.id == trabajador_id).first()
        if not trabajador:
            return {"success": False, "error": "Trabajador no encontrado", "data": None}
        
        # Actualizar solo los campos proporcionados
        campos_permitidos = ["nombre", "apellido", "email", "telefono", "cargo", "salario", "activo"]
        for campo, valor in kwargs.items():
            if campo in campos_permitidos and valor is not None:
                setattr(trabajador, campo, valor)
        
        db.commit()
        db.refresh(trabajador)
        
        return {
            "success": True,
            "error": None,
            "data": {
                "id": trabajador.id,
                "nombre": trabajador.nombre,
                "apellido": trabajador.apellido,
                "cedula": trabajador.cedula,
                "email": trabajador.email,
                "telefono": trabajador.telefono,
                "cargo": trabajador.cargo,
                "salario": trabajador.salario
            }
        }
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e), "data": None}


def eliminar_trabajador(db: Session, trabajador_id: int) -> dict:
    """Elimina (desactiva) un trabajador"""
    try:
        trabajador = db.query(Worker).filter(Worker.id == trabajador_id).first()
        if not trabajador:
            return {"success": False, "error": "Trabajador no encontrado"}
        
        # Desactivar en lugar de eliminar
        trabajador.activo = False
        db.commit()
        
        return {"success": True, "error": None}
    except Exception as e:
        db.rollback()
        return {"success": False, "error": str(e)}
