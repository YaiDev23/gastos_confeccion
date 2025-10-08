from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime
import pytz

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()

def obtener_fecha_hora_bogota():
    """Obtiene la fecha y hora actual en zona horaria de Bogotá"""
    bogota_tz = pytz.timezone('America/Bogota')
    ahora = datetime.now(bogota_tz)
    return ahora.strftime("%d/%m/%Y - %I:%M:%S %p")

@router.get("/", response_class=HTMLResponse)
async def mostrar_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@router.get("/costo-operacion", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("formulario.html", {"request": request})

@router.get("/punto-equilibrio", response_class=HTMLResponse)
async def mostrar_punto_equilibrio(request: Request):
    return templates.TemplateResponse("punto_equilibrio.html", {"request": request})

@router.post("/calcular", response_class=HTMLResponse)
async def calcular_costo(
    request: Request,
    cantidad_trabajadoras: int = Form(...),
    cantidad_practicantes: int = Form(...)
):
    # Datos base
    arriendo = 750000
    arriendo_diario = arriendo / 30

    salario = {
        'operaria': 64000,
        'aprendiz': 30000
    }

    gastos_fijos = {
        'gasolina': 10000,
        'hilos': 10000,
        'luz': 5000,
        'maquinas': 10000
    }

    # Cálculos
    costo_trabajadoras = cantidad_trabajadoras * salario['operaria']
    costo_practicantes = cantidad_practicantes * salario['aprendiz']
    gastos_fijos_total = sum(gastos_fijos.values())
    
    costo_operacion = (costo_trabajadoras + 
                      costo_practicantes + 
                      gastos_fijos_total + 
                      arriendo_diario)
    
    # Datos para el template
    datos = {
        'cantidad_trabajadoras': cantidad_trabajadoras,
        'cantidad_practicantes': cantidad_practicantes,
        'costo_trabajadoras': costo_trabajadoras,
        'costo_practicantes': costo_practicantes,
        'arriendo_diario': int(arriendo_diario),
        'gastos_fijos': gastos_fijos,
        'gastos_fijos_total': gastos_fijos_total,
        'costo_operacion': int(costo_operacion)
    }
    
    # Obtener fecha y hora de Bogotá
    fecha_hora_bogota = obtener_fecha_hora_bogota()
    
    return templates.TemplateResponse("resultado.html", {
        "request": request, 
        "datos": datos,
        "fecha_hora_bogota": fecha_hora_bogota
    })

@router.post("/calcular-equilibrio", response_class=HTMLResponse)
async def calcular_punto_equilibrio(
    request: Request,
    cantidad_trabajadoras: int = Form(...),
    cantidad_practicantes: int = Form(...),
    precio_unidad: float = Form(...),
    unidades_fabricadas: int = Form(0)
):
    # Datos base (mismo cálculo que en costo de operación)
    arriendo = 750000
    arriendo_diario = arriendo / 30

    salario = {
        'operaria': 64000,
        'aprendiz': 30000
    }

    gastos_fijos = {
        'gasolina': 10000,
        'hilos': 10000,
        'luz': 5000,
        'maquinas': 10000
    }

    # Cálculo del costo fijo total
    costo_trabajadoras = cantidad_trabajadoras * salario['operaria']
    costo_practicantes = cantidad_practicantes * salario['aprendiz']
    gastos_fijos_total = sum(gastos_fijos.values())
    
    costo_fijo_total = (costo_trabajadoras + 
                       costo_practicantes + 
                       gastos_fijos_total + 
                       arriendo_diario)

    
    if precio_unidad <= 0:
        punto_equilibrio = float('inf')  # No es posible alcanzar equilibrio
    else:
        punto_equilibrio = costo_fijo_total / precio_unidad

    ingresos_equilibrio = punto_equilibrio * precio_unidad

    # Cálculo de ganancia real del día (si se ingresaron unidades fabricadas)
    ganancia_real = None
    ingresos_reales = None
    utilidad_neta = None
    
    if unidades_fabricadas > 0:
        ingresos_reales = unidades_fabricadas * precio_unidad
        utilidad_neta = ingresos_reales - costo_fijo_total
        ganancia_real = utilidad_neta

    # Datos para el template
    datos = {
        'cantidad_trabajadoras': cantidad_trabajadoras,
        'cantidad_practicantes': cantidad_practicantes,
        'costo_trabajadoras': costo_trabajadoras,
        'costo_practicantes': costo_practicantes,
        'arriendo_diario': int(arriendo_diario),
        'gastos_fijos_total': gastos_fijos_total,
        'costo_fijo_total': int(costo_fijo_total),
        'precio_unidad': precio_unidad,
        'punto_equilibrio': punto_equilibrio,
        'ingresos_equilibrio': int(ingresos_equilibrio) if punto_equilibrio != float('inf') else 0,
        'unidades_fabricadas': unidades_fabricadas,
        'ganancia_real': ganancia_real,
        'ingresos_reales': ingresos_reales,
        'utilidad_neta': utilidad_neta
    }
    
    # Obtener fecha y hora de Bogotá
    fecha_hora_bogota = obtener_fecha_hora_bogota()
    
    return templates.TemplateResponse("resultado_equilibrio.html", {
        "request": request, 
        "datos": datos,
        "fecha_hora_bogota": fecha_hora_bogota
    })

@router.get("/cost_operation")
def get_cost_operation(cantidad_trabajadoras: int, cantidad_practicantes: int):
    arriendo = 750000
    arriendo_x_dia = arriendo / 30

    salario = {
        'operaria': 64000,
        'aprendiz': 30000
    }

    gastos_fijos = {
        'gasolina': 10000,
        'hilos': 10000,
        'luz': 5000,
        'maquinas': 10000
    }

    costo_operacion = (cantidad_trabajadoras * salario['operaria'] + 
                      cantidad_practicantes * salario['aprendiz'] + 
                      gastos_fijos['gasolina'] + 
                      gastos_fijos['hilos'] + 
                      gastos_fijos['luz'] + 
                      gastos_fijos['maquinas'] + 
                      arriendo_x_dia)
    
    return {"costo_operacion": costo_operacion}

@router.get("/breakeven_point")
def get_breakeven_point(precio_producto: float, costo_variable_unitario: float, costo_fijo_total: float):
    if precio_producto <= costo_variable_unitario:
        return {"error": "El precio del producto debe ser mayor que el costo variable unitario."}
    
    punto_equilibrio = costo_fijo_total / (precio_producto - costo_variable_unitario)
    
    return {"punto_equilibrio": punto_equilibrio}
