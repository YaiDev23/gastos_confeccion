"""
Servicio de asistencia y trabajadores
Proporciona funciones para gestionar asistencias y trabajadores
"""

from datetime import datetime, date
from sqlalchemy import func
from sqlalchemy.exc import IntegrityError
from app.db.models import Worker
from app.db.models.assistence_model import Assistence
import pytz


def obtener_fecha_hora_bogota():
    """Obtiene la fecha y hora actual en zona horaria de Bogotá"""
    bogota_tz = pytz.timezone('America/Bogota')
    ahora = datetime.now(bogota_tz)
    return ahora


# ==================
# FUNCIONES DE ASISTENCIA
# ==================

def marcar_llegada(db, worker_id: int):
    """
    Marca la llegada de un trabajador
    
    Args:
        db: Sesión de base de datos
        worker_id: ID del trabajador
        
    Returns:
        dict: {"success": bool, "message": str, "data": dict}
    """
    try:
        # Obtener el trabajador
        worker = db.query(Worker).filter(Worker.id == worker_id).first()
        
        if not worker:
            return {
                "success": False,
                "error": "Trabajador no encontrado"
            }
        
        # Obtener la fecha de hoy en Bogotá
        ahora = obtener_fecha_hora_bogota()
        
        # Verificar si ya hay un registro de llegada hoy
        asistencia_hoy = db.query(Assistence).filter(
            Assistence.worker == worker.nombre,
            func.DATE(Assistence.arrival_time) == ahora.date()
        ).first()
        
        if asistencia_hoy:
            return {
                "success": False,
                "error": f"El trabajador {worker.nombre} ya fue marcado hoy"
            }
        
        # Crear nuevo registro de asistencia
        nueva_asistencia = Assistence(
            worker=worker.nombre,
            arrival_time=ahora
        )
        
        db.add(nueva_asistencia)
        db.commit()
        db.refresh(nueva_asistencia)
        
        return {
            "success": True,
            "message": f"Llegada marcada para {worker.nombre}",
            "data": {
                "id": nueva_asistencia.id_assistence,
                "worker": nueva_asistencia.worker,
                "arrival_time": nueva_asistencia.arrival_time.isoformat(),
                "fecha": nueva_asistencia.arrival_time.strftime("%d/%m/%Y"),
                "hora": nueva_asistencia.arrival_time.strftime("%H:%M:%S")
            }
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error al marcar llegada: {str(e)}"
        }


def marcar_llegada_por_reference_id(db, reference_id: str):
    """
    Marca la llegada de un trabajador usando el reference_id (código de barras)
    
    Args:
        db: Sesión de base de datos
        reference_id: Reference ID del trabajador (código de barras)
        
    Returns:
        dict: {"success": bool, "message": str, "data": dict}
    """
    try:
        # Obtener el trabajador por reference_id
        worker = db.query(Worker).filter(Worker.reference_id == reference_id).first()
        
        if not worker:
            return {
                "success": False,
                "error": f"No se encontró trabajador con código {reference_id}"
            }
        
        # Obtener la fecha de hoy en Bogotá
        ahora = obtener_fecha_hora_bogota()
        
        # Verificar si ya hay un registro de llegada hoy
        asistencia_hoy = db.query(Assistence).filter(
            Assistence.worker == worker.nombre,
            func.DATE(Assistence.arrival_time) == ahora.date()
        ).first()
        
        if asistencia_hoy:
            return {
                "success": False,
                "error": f"El trabajador {worker.nombre} ya fue marcado hoy"
            }
        
        # Crear nuevo registro de asistencia
        nueva_asistencia = Assistence(
            worker=worker.nombre,
            arrival_time=ahora
        )
        
        db.add(nueva_asistencia)
        db.commit()
        db.refresh(nueva_asistencia)
        
        return {
            "success": True,
            "message": f"✓ Bienvenida {worker.nombre}",
            "data": {
                "id": nueva_asistencia.id_assistence,
                "worker": f"{worker.nombre} {worker.apellido}",
                "arrival_time": nueva_asistencia.arrival_time.isoformat(),
                "fecha": nueva_asistencia.arrival_time.strftime("%d/%m/%Y"),
                "hora": nueva_asistencia.arrival_time.strftime("%H:%M:%S")
            }
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error al marcar llegada: {str(e)}"
        }


def marcar_salida(db, assistence_id: int):
    """
    Marca la salida de un trabajador
    
    Args:
        db: Sesión de base de datos
        assistence_id: ID del registro de asistencia
        
    Returns:
        dict: {"success": bool, "message": str, "data": dict}
    """
    try:
        # Obtener la asistencia
        asistencia = db.query(Assistence).filter(Assistence.id_assistence == assistence_id).first()
        
        if not asistencia:
            return {
                "success": False,
                "error": "Registro de asistencia no encontrado"
            }
        
        if asistencia.departure_time:
            return {
                "success": False,
                "error": f"El trabajador {asistencia.worker} ya tiene hora de salida registrada"
            }
        
        # Obtener la fecha y hora actual en Bogotá
        ahora = obtener_fecha_hora_bogota()
        
        # Actualizar la hora de salida
        asistencia.departure_time = ahora
        
        db.commit()
        db.refresh(asistencia)
        
        # Calcular tiempo trabajado
        tiempo_trabajado = asistencia.departure_time - asistencia.arrival_time
        horas = tiempo_trabajado.total_seconds() / 3600
        
        return {
            "success": True,
            "message": f"Salida marcada para {asistencia.worker}",
            "data": {
                "id": asistencia.id_assistence,
                "worker": asistencia.worker,
                "arrival_time": asistencia.arrival_time.isoformat(),
                "departure_time": asistencia.departure_time.isoformat(),
                "fecha": asistencia.arrival_time.strftime("%d/%m/%Y"),
                "hora_llegada": asistencia.arrival_time.strftime("%H:%M:%S"),
                "hora_salida": asistencia.departure_time.strftime("%H:%M:%S"),
                "horas_trabajadas": round(horas, 2)
            }
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error al marcar salida: {str(e)}"
        }


def obtener_asistencias_hoy(db):
    """
    Obtiene las asistencias de hoy
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        dict: {"success": bool, "data": list}
    """
    try:
        # Obtener la fecha de hoy en Bogotá
        ahora = obtener_fecha_hora_bogota()
        hoy = ahora.date()
        
        # Obtener todas las asistencias de hoy
        asistencias = db.query(Assistence).filter(
            func.DATE(Assistence.arrival_time) == hoy
        ).all()
        
        datos = []
        for asistencia in asistencias:
            tiempo_trabajado = None
            horas_trabajadas = None
            
            if asistencia.departure_time:
                tiempo_trabajado = asistencia.departure_time - asistencia.arrival_time
                horas_trabajadas = round(tiempo_trabajado.total_seconds() / 3600, 2)
            
            datos.append({
                "id_assistence": asistencia.id_assistence,
                "worker": asistencia.worker,
                "arrival_time": asistencia.arrival_time.isoformat(),
                "departure_time": asistencia.departure_time.isoformat() if asistencia.departure_time else None,
                "hora_llegada": asistencia.arrival_time.strftime("%H:%M:%S"),
                "hora_salida": asistencia.departure_time.strftime("%H:%M:%S") if asistencia.departure_time else "---",
                "horas_trabajadas": horas_trabajadas,
                "estado": "Salió" if asistencia.departure_time else "Presente"
            })
        
        return {
            "success": True,
            "data": datos,
            "total": len(datos),
            "fecha": hoy.strftime("%d/%m/%Y")
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error al obtener asistencias: {str(e)}",
            "data": []
        }


# ==================
# FUNCIONES DE TRABAJADORES
# ==================

def obtener_trabajadores_activos(db):
    """
    Obtiene todos los trabajadores activos
    
    Args:
        db: Sesión de base de datos
        
    Returns:
        dict: {"success": bool, "data": list}
    """
    try:
        trabajadores = db.query(Worker).filter(Worker.activo == True).all()
        
        datos = []
        for trabajador in trabajadores:
            datos.append({
                "id": trabajador.id,
                "nombre": trabajador.nombre,
                "apellido": trabajador.apellido,
                "cedula": trabajador.cedula,
                "email": trabajador.email,
                "telefono": trabajador.telefono,
                "cargo": trabajador.cargo,
                "salario": trabajador.salario,
                "activo": trabajador.activo
            })
        
        return {
            "success": True,
            "data": datos,
            "total": len(datos)
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error al obtener trabajadores: {str(e)}",
            "data": []
        }


def crear_trabajador(db, nombre: str, apellido: str, cedula: str, cargo: str, 
                     salario: float, email: str = None, telefono: str = None):
    """
    Crea un nuevo trabajador
    
    Args:
        db: Sesión de base de datos
        nombre: Nombre del trabajador
        apellido: Apellido del trabajador
        cedula: Cédula del trabajador (única)
        cargo: Cargo del trabajador
        salario: Salario del trabajador
        email: Email del trabajador (opcional)
        telefono: Teléfono del trabajador (opcional)
        
    Returns:
        dict: {"success": bool, "message": str, "data": dict}
    """
    try:
        # Verificar si el trabajador ya existe
        existe = db.query(Worker).filter(Worker.cedula == cedula).first()
        
        if existe:
            return {
                "success": False,
                "error": f"Ya existe un trabajador con cédula {cedula}"
            }
        
        # Crear nuevo trabajador
        nuevo_trabajador = Worker(
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            cargo=cargo,
            salario=salario,
            email=email,
            telefono=telefono,
            activo=True
        )
        
        db.add(nuevo_trabajador)
        db.commit()
        db.refresh(nuevo_trabajador)
        
        return {
            "success": True,
            "message": f"Trabajador {nombre} {apellido} creado exitosamente",
            "data": {
                "id": nuevo_trabajador.id,
                "nombre": nuevo_trabajador.nombre,
                "apellido": nuevo_trabajador.apellido,
                "cedula": nuevo_trabajador.cedula,
                "email": nuevo_trabajador.email,
                "telefono": nuevo_trabajador.telefono,
                "cargo": nuevo_trabajador.cargo,
                "salario": nuevo_trabajador.salario,
                "activo": nuevo_trabajador.activo
            }
        }
    except IntegrityError as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error de integridad: {str(e)}"
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error al crear trabajador: {str(e)}"
        }


def obtener_trabajador(db, trabajador_id: int):
    """
    Obtiene la información de un trabajador específico
    
    Args:
        db: Sesión de base de datos
        trabajador_id: ID del trabajador
        
    Returns:
        dict: {"success": bool, "data": dict}
    """
    try:
        trabajador = db.query(Worker).filter(Worker.id == trabajador_id).first()
        
        if not trabajador:
            return {
                "success": False,
                "error": "Trabajador no encontrado"
            }
        
        return {
            "success": True,
            "data": {
                "id": trabajador.id,
                "nombre": trabajador.nombre,
                "apellido": trabajador.apellido,
                "cedula": trabajador.cedula,
                "email": trabajador.email,
                "telefono": trabajador.telefono,
                "cargo": trabajador.cargo,
                "salario": trabajador.salario,
                "activo": trabajador.activo
            }
        }
    except Exception as e:
        return {
            "success": False,
            "error": f"Error al obtener trabajador: {str(e)}"
        }


def actualizar_trabajador(db, trabajador_id: int, **kwargs):
    """
    Actualiza la información de un trabajador
    
    Args:
        db: Sesión de base de datos
        trabajador_id: ID del trabajador
        **kwargs: Campos a actualizar (nombre, apellido, cargo, salario, email, telefono, activo)
        
    Returns:
        dict: {"success": bool, "message": str, "data": dict}
    """
    try:
        trabajador = db.query(Worker).filter(Worker.id == trabajador_id).first()
        
        if not trabajador:
            return {
                "success": False,
                "error": "Trabajador no encontrado"
            }
        
        # Actualizar solo los campos proporcionados
        campos_permitidos = ['nombre', 'apellido', 'cargo', 'salario', 'email', 'telefono', 'activo']
        for campo, valor in kwargs.items():
            if campo in campos_permitidos and valor is not None:
                setattr(trabajador, campo, valor)
        
        db.commit()
        db.refresh(trabajador)
        
        return {
            "success": True,
            "message": f"Trabajador actualizado exitosamente",
            "data": {
                "id": trabajador.id,
                "nombre": trabajador.nombre,
                "apellido": trabajador.apellido,
                "cedula": trabajador.cedula,
                "email": trabajador.email,
                "telefono": trabajador.telefono,
                "cargo": trabajador.cargo,
                "salario": trabajador.salario,
                "activo": trabajador.activo
            }
        }
    except IntegrityError as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error de integridad: {str(e)}"
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error al actualizar trabajador: {str(e)}"
        }


def eliminar_trabajador(db, trabajador_id: int):
    """
    Elimina (desactiva) un trabajador
    
    Args:
        db: Sesión de base de datos
        trabajador_id: ID del trabajador
        
    Returns:
        dict: {"success": bool, "message": str}
    """
    try:
        trabajador = db.query(Worker).filter(Worker.id == trabajador_id).first()
        
        if not trabajador:
            return {
                "success": False,
                "error": "Trabajador no encontrado"
            }
        
        # Desactivar en lugar de eliminar
        trabajador.activo = False
        
        db.commit()
        
        return {
            "success": True,
            "message": f"Trabajador desactivado exitosamente"
        }
    except Exception as e:
        db.rollback()
        return {
            "success": False,
            "error": f"Error al eliminar trabajador: {str(e)}"
        }
