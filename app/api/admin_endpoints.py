from fastapi import APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
import os

# Configurar templates
templates = Jinja2Templates(directory="app/templates")

router = APIRouter()


@router.get("/admin/usuarios", response_class=HTMLResponse)
async def admin_usuarios_lista(request: Request):
    """Mostrar la lista de usuarios para administración"""
    return templates.TemplateResponse("admin/usuarios_lista.html", {"request": request})


@router.get("/admin/usuarios/nuevo", response_class=HTMLResponse)
async def admin_usuarios_nuevo(request: Request):
    """Mostrar formulario para crear un nuevo usuario"""
    return templates.TemplateResponse("admin/usuarios_crear.html", {"request": request})


@router.get("/admin/usuarios/editar/{user_id}", response_class=HTMLResponse)
async def admin_usuarios_editar(request: Request, user_id: int):
    """Mostrar formulario para editar un usuario"""
    return templates.TemplateResponse("admin/usuarios_editar.html", {"request": request, "user_id": user_id})
