from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse
from datetime import datetime
import pytz

from app.api.schemas.gastos_schema import GastoSchema
from app.api.schemas.assistence_schema import AsistenciaCreate, AsistenciaSalida, AsistenciaCodigoBarras
from app.db.connection import get_db
from app.service.assistence_service import (
    marcar_llegada, 
    marcar_llegada_por_reference_id,
    marcar_salida, 
    obtener_asistencias_hoy,
    obtener_trabajadores_activos
)

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


def obtener_fecha_hora_bogota():
    """Obtiene la fecha y hora actual en zona horaria de Bogotá"""
    bogota_tz = pytz.timezone('America/Bogota')
    ahora = datetime.now(bogota_tz)
    return ahora.strftime("%d/%m/%Y - %I:%M:%S %p")


# =====================
# VISTAS HTML
# =====================

@router.get("/", response_class=HTMLResponse)
async def mostrar_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})


@router.get("/marcar-asistencia", response_class=HTMLResponse)
async def mostrar_marcar_asistencia(request: Request):
    """Muestra la página para marcar llegada"""
    return templates.TemplateResponse("assistence/marcar_asistencia.html", {"request": request})


@router.get("/marcar-salida", response_class=HTMLResponse)
async def mostrar_marcar_salida(request: Request):
    """Muestra la página para marcar salida"""
    db = get_db()
    if db is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "No se pudo conectar a la base de datos"
        })
    
    try:
        resultado = obtener_asistencias_hoy(db)
        asistencias = resultado["data"] if resultado["success"] else []
        
        # Filtrar solo asistencias sin salida registrada
        asistencias_sin_salida = [
            a for a in asistencias if a["departure_time"] is None
        ]
        
        fecha_hora_bogota = obtener_fecha_hora_bogota()
        
        return templates.TemplateResponse("marcar_salida.html", {
            "request": request,
            "asistencias": asistencias_sin_salida,
            "fecha_hora_bogota": fecha_hora_bogota
        })
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.get("/resumen-asistencia", response_class=HTMLResponse)
async def mostrar_resumen_asistencia(request: Request):
    """Muestra el resumen de asistencias del día"""
    db = get_db()
    if db is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "No se pudo conectar a la base de datos"
        })
    
    try:
        resultado = obtener_asistencias_hoy(db)
        asistencias = resultado["data"] if resultado["success"] else []
        
        fecha_hora_bogota = obtener_fecha_hora_bogota()
        
        return templates.TemplateResponse("resumen_asistencia.html", {
            "request": request,
            "asistencias": asistencias,
            "fecha_hora_bogota": fecha_hora_bogota
        })
    finally:
        from app.db.connection import close_connection
        close_connection(db)


# =====================
# ENDPOINTS API
# =====================


@router.post("/api/marcar-llegada", response_class=JSONResponse)
async def api_marcar_llegada(asistencia: AsistenciaCreate):
    """
    Marca la llegada de un trabajador.
    
    Parámetros:
    - worker_id: ID del trabajador
    """
    db = get_db()
    if db is None:
        return JSONResponse(
            status_code=500,
            content={"error": "No se pudo conectar a la base de datos"}
        )
    
    try:
        resultado = marcar_llegada(db, asistencia.worker_id)
        if resultado["success"]:
            return JSONResponse(status_code=200, content=resultado)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": resultado["error"]}
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.post("/api/marcar-llegada-codigo", response_class=JSONResponse)
async def api_marcar_llegada_codigo(asistencia: AsistenciaCodigoBarras):
    """
    Marca la llegada de un trabajador usando el reference_id (código de barras).
    
    Parámetros:
    - reference_id: Reference ID del trabajador (código de barras)
    """
    db = get_db()
    if db is None:
        return JSONResponse(
            status_code=500,
            content={"error": "No se pudo conectar a la base de datos"}
        )
    
    try:
        resultado = marcar_llegada_por_reference_id(db, asistencia.reference_id)
        if resultado["success"]:
            return JSONResponse(status_code=200, content=resultado)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": resultado["error"]}
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.post("/api/marcar-salida", response_class=JSONResponse)
async def api_marcar_salida(asistencia: AsistenciaSalida):
    """
    Marca la salida de un trabajador.
    
    Parámetros:
    - assistence_id: ID del registro de asistencia
    """
    db = get_db()
    if db is None:
        return JSONResponse(
            status_code=500,
            content={"error": "No se pudo conectar a la base de datos"}
        )
    
    try:
        resultado = marcar_salida(db, asistencia.id_assistence)
        if resultado["success"]:
            return JSONResponse(status_code=200, content=resultado)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": resultado["error"]}
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.get("/api/asistencias-hoy", response_class=JSONResponse)
async def api_obtener_asistencias_hoy():
    """Obtiene todas las asistencias del día actual"""
    db = get_db()
    if db is None:
        return JSONResponse(
            status_code=500,
            content={"error": "No se pudo conectar a la base de datos"}
        )
    
    try:
        resultado = obtener_asistencias_hoy(db)
        if resultado["success"]:
            return JSONResponse(status_code=200, content=resultado)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": resultado["error"]}
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.get("/api/trabajadores", response_class=JSONResponse)
async def api_obtener_trabajadores():
    """Obtiene la lista de trabajadores activos"""
    db = get_db()
    if db is None:
        return JSONResponse(
            status_code=500,
            content={"error": "No se pudo conectar a la base de datos"}
        )
    
    try:
        resultado = obtener_trabajadores_activos(db)
        if resultado["success"]:
            return JSONResponse(status_code=200, content=resultado)
        else:
            return JSONResponse(
                status_code=400,
                content={"error": resultado["error"]}
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)
