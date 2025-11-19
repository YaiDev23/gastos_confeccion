from fastapi import APIRouter, Request, Form
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from datetime import datetime

from app.api.schemas.gastos_schema import GastoSchema
import pytz

templates = Jinja2Templates(directory="app/templates")

router = APIRouter()
gastos_fijos = GastoSchema.gastos_fijos
arriendo = GastoSchema.arriendo

def obtener_fecha_hora_bogota():
    """Obtiene la fecha y hora actual en zona horaria de Bogotá"""
    bogota_tz = pytz.timezone('America/Bogota')
    ahora = datetime.now(bogota_tz)
    return ahora.strftime("%d/%m/%Y - %I:%M:%S %p")

@router.get("/", response_class=HTMLResponse)
async def mostrar_menu(request: Request):
    return templates.TemplateResponse("menu.html", {"request": request})

@router.get("/produccion", response_class=HTMLResponse)
async def mostrar_produccion(request: Request):
    return templates.TemplateResponse("produccion.html", {"request": request})

@router.post("/calcular-produccion", response_class=HTMLResponse)
async def calcular_produccion(request: Request):
    form = await request.form()
    produccion_por_color = []
    total_unidades = 0
    
    # Determinar cuántos colores hay en el formulario
    color_count = len([k for k in form.keys() if k.startswith('color_')])
    
    # Inicializar totales por talla
    totales_por_talla = {
        "18-24": 0, "24-36": 0, "36-48": 0,
        "2": 0, "4": 0, "6": 0, "8": 0, "10": 0, "12": 0, "14": 0,
        "16": 0, "18": 0
    }
    
    for i in range(1, color_count + 1):
        color = form.get(f'color_{i}')
        if not color:
            continue
        
        def safe_int(value):
            try:
                return int(value)
            except (TypeError, ValueError):
                return 0
            
        tallas_color = {
            "18-24": safe_int(form.get(f'talla_18_24_{i}')),
            "24-36": safe_int(form.get(f'talla_24_36_{i}')),
            "36-48": safe_int(form.get(f'talla_36_48_{i}')),
            "2": safe_int(form.get(f'talla_2_{i}')),
            "4": safe_int(form.get(f'talla_4_{i}')),
            "6": safe_int(form.get(f'talla_6_{i}')),
            "8": safe_int(form.get(f'talla_8_{i}')),
            "10": safe_int(form.get(f'talla_10_{i}')),
            "12": safe_int(form.get(f'talla_12_{i}')),
            "14": safe_int(form.get(f'talla_14_{i}')),
            "16": safe_int(form.get(f'talla_16_{i}')),
            "18": safe_int(form.get(f'talla_18_{i}'))
        }
        
        # Actualizar totales por talla
        for talla, cantidad in tallas_color.items():
            totales_por_talla[talla] += cantidad
        
        total_color = sum(tallas_color.values())
        total_unidades += total_color
        
        produccion_por_color.append({
            'nombre': color,
            'tallas': tallas_color,
            'total': total_color
        })
    
    datos = {
        'produccion_por_color': produccion_por_color,
        'total_unidades': total_unidades,
        'totales_por_talla': totales_por_talla
    }
    
    fecha_hora_bogota = obtener_fecha_hora_bogota()
    
    return templates.TemplateResponse("resultado_produccion.html", {
        "request": request,
        "datos": datos,
        "fecha_hora_bogota": fecha_hora_bogota
    })

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
    cantidad_trabajadoras_prestaciones: int = Form(...),
    cantidad_practicantes: int = Form(...)
):
    # Datos base
    
    arriendo_diario = arriendo / 30
    
    from app.api.schemas.operator_schema import OperatorSchema
    salario = OperatorSchema.operaria['salario']
    salario_prestaciones = OperatorSchema.operaria_prestaciones['salario']
    salario_aprendiz = OperatorSchema.aprendiz['salario']
    
    

    # Cálculos
    costo_trabajadoras = cantidad_trabajadoras * salario
    costo_trabajadoras_prestaciones = cantidad_trabajadoras_prestaciones * salario_prestaciones
    costo_practicantes = cantidad_practicantes * salario_aprendiz
    gastos_fijos_total = sum(gastos_fijos.values())
    
    costo_operacion = (costo_trabajadoras + 
                      costo_trabajadoras_prestaciones +
                      costo_practicantes + 
                      gastos_fijos_total + 
                      arriendo_diario)
    
    # Datos para el template
    datos = {
        'cantidad_trabajadoras': cantidad_trabajadoras,
        'cantidad_trabajadoras_prestaciones': cantidad_trabajadoras_prestaciones,
        'cantidad_practicantes': cantidad_practicantes,
        'costo_trabajadoras': costo_trabajadoras,
        'costo_trabajadoras_prestaciones': costo_trabajadoras_prestaciones,
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
    cantidad_trabajadoras_prestaciones: int = Form(...),
    cantidad_practicantes: int = Form(...),
    precio_unidad: float = Form(...),
    unidades_fabricadas: int = Form(0)
):
    # Datos base (mismo cálculo que en costo de operación)
    arriendo_diario = arriendo / 30

    from api.schemas.operator_schema import OperatorSchema
    salario = OperatorSchema.operaria['salario']
    salario_prestaciones = OperatorSchema.operaria_prestaciones['salario']
    salario_aprendiz = OperatorSchema.aprendiz['salario']

    # Cálculo del costo fijo total
    costo_trabajadoras = cantidad_trabajadoras * salario
    costo_trabajadoras_prestaciones = cantidad_trabajadoras_prestaciones * salario_prestaciones
    costo_practicantes = cantidad_practicantes * salario_aprendiz
    gastos_fijos_total = sum(gastos_fijos.values())
    
    costo_fijo_total = (costo_trabajadoras + 
                       costo_trabajadoras_prestaciones +
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
        'cantidad_trabajadoras_prestaciones': cantidad_trabajadoras_prestaciones,
        'cantidad_practicantes': cantidad_practicantes,
        'costo_trabajadoras': costo_trabajadoras,
        'costo_trabajadoras_prestaciones': costo_trabajadoras_prestaciones,
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
def get_cost_operation(cantidad_trabajadoras: int, cantidad_trabajadoras_prestaciones: int, cantidad_practicantes: int):
    arriendo_x_dia = arriendo / 30

    from api.schemas.operator_schema import OperatorSchema
    salario = OperatorSchema.operaria['salario']
    salario_prestaciones = OperatorSchema.operaria_prestaciones['salario']
    salario_aprendiz = OperatorSchema.aprendiz['salario']

    costo_operacion = (cantidad_trabajadoras * salario + 
                      cantidad_trabajadoras_prestaciones * salario_prestaciones +
                      cantidad_practicantes * salario_aprendiz + 
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

@router.get("/justicia-pago", response_class=HTMLResponse)
async def mostrar_justicia_pago(request: Request):
    return templates.TemplateResponse("justicia_pago.html", {"request": request})

@router.post("/calcular-justicia-pago", response_class=HTMLResponse)
async def calcular_justicia_pago(
    request: Request,
    tiempo_unitario: float = Form(...),
    cantidad: int = Form(...),
    pago_lote: float = Form(...),
    tarifa_minuto: float = Form(...)
):
    # Cálculos según la fórmula proporcionada
    tiempo_total = tiempo_unitario * cantidad
    costo_real = tiempo_total * tarifa_minuto
    
    # Evitar división por cero
    if costo_real > 0:
        porcentaje_justicia = (pago_lote / costo_real) * 100
    else:
        porcentaje_justicia = 0
    
    # Datos para el template
    datos = {
        'tiempo_unitario': tiempo_unitario,
        'cantidad': cantidad,
        'pago_lote': pago_lote,
        'tarifa_minuto': tarifa_minuto,
        'tiempo_total': tiempo_total,
        'costo_real': costo_real,
        'porcentaje_justicia': porcentaje_justicia
    }
    
    # Obtener fecha y hora de Bogotá
    fecha_hora_bogota = obtener_fecha_hora_bogota()
    
    return templates.TemplateResponse("resultado_justicia_pago.html", {
        "request": request,
        "datos": datos,
        "fecha_hora_bogota": fecha_hora_bogota
    })
