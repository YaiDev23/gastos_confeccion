from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from datetime import datetime
import io
import json

from app.api.schemas.gastos_schema import GastoSchema

from app.db.connection import get_db
from app.service.assistence_service import (
    marcar_llegada, 
    marcar_salida, 
    obtener_asistencias_hoy,
    obtener_trabajadores_activos
)
import pytz

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()
gastos_fijos = GastoSchema.gastos_fijos
arriendo = GastoSchema.arriendo

@router.get("/", response_class=HTMLResponse)
async def mostrar_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@router.get("/calculos", response_class=HTMLResponse)
async def mostrar_calculos_menu(request: Request):
    return templates.TemplateResponse("calculos_menu.html", {"request": request})

@router.get("/agregar-trabajador", response_class=HTMLResponse)
async def mostrar_agregar_trabajador(request: Request):
    return templates.TemplateResponse("agregar_trabajador.html", {"request": request})

@router.get("/trabajadores", response_class=HTMLResponse)
async def mostrar_lista_trabajadores(request: Request):
    return templates.TemplateResponse("lista_trabajadores.html", {"request": request})

@router.get("/editar-trabajador", response_class=HTMLResponse)
async def mostrar_editar_trabajador(request: Request):
    return templates.TemplateResponse("editar_trabajador.html", {"request": request})

@router.get("/produccion", response_class=HTMLResponse)
async def mostrar_produccion(request: Request):
    return templates.TemplateResponse("produccion.html", {"request": request})

@router.get("/costo-operacion", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("calcular_ costo_operacion.html", {"request": request})

@router.get("/punto-equilibrio", response_class=HTMLResponse)
async def mostrar_punto_equilibrio(request: Request):
    return templates.TemplateResponse("punto_equilibrio.html", {"request": request})

@router.get("/justicia-pago", response_class=HTMLResponse)
async def mostrar_justicia_pago(request: Request):
    return templates.TemplateResponse("justicia_pago.html", {"request": request})



#===============================DELIVERY TEMPLATES ENDPOINTS=================================#
@router.get("/menu_entrega", response_class=HTMLResponse)
async def mostrar_menu_entrega(request: Request):
    return templates.TemplateResponse("delivery/menu_entrega.html", {"request": request})


@router.get("/entrega_corte", response_class=HTMLResponse)
async def mostrar_entrega_corte(request: Request):
    return templates.TemplateResponse("delivery/agregar_entrega.html", {"request": request})

@router.get("/consultar_entrega", response_class=HTMLResponse)
async def mostrar_consultar_entrega(request: Request):
    return templates.TemplateResponse("delivery/consultar_entrega.html", {"request": request})