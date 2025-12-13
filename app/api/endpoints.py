from fastapi import APIRouter, Request, Form, HTTPException, status
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, JSONResponse, FileResponse
from datetime import datetime
import io
import json

from app.api.schemas.gastos_schema import GastoSchema
from app.db.connection import get_db
from app.service.worker_service import crear_trabajador, listar_trabajadores, obtener_trabajador, actualizar_trabajador, eliminar_trabajador
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

@router.post("/calcular-produccion", response_class=HTMLResponse)
async def calcular_produccion(request: Request):
    form = await request.form()
    produccion_por_lote = []
    total_unidades = 0
    total_venta = 0
    
    # Determinar cuántos lotes hay en el formulario
    lote_count = len([k for k in form.keys() if k.startswith('tipo_lote_')])
    
    # Inicializar totales por talla
    totales_por_talla = {
        "18-24": 0, "24-36": 0, "36-48": 0,
        "2": 0, "4": 0, "6": 0, "8": 0, "10": 0, "12": 0, "14": 0,
        "16": 0, "18": 0
    }
    
    def safe_int(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 0
    
    def safe_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0
    
    for i in range(1, lote_count + 1):
        tipo_lote = form.get(f'tipo_lote_{i}')
        color = form.get(f'color_{i}')
        precio = safe_float(form.get(f'precio_{i}', 0))
        
        if not tipo_lote or not color:
            continue
            
        tallas_lote = {
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
        for talla, cantidad in tallas_lote.items():
            totales_por_talla[talla] += cantidad
        
        total_lote = sum(tallas_lote.values())
        total_unidades += total_lote
        valor_lote = total_lote * precio if precio > 0 else 0
        total_venta += valor_lote
        
        produccion_por_lote.append({
            'tipo_lote': tipo_lote,
            'color': color,
            'etiqueta': f"{tipo_lote} {color}",
            'tallas': tallas_lote,
            'total': total_lote,
            'precio': precio,
            'valor_total': valor_lote
        })
    
    # Ordenar por tipo de lote y luego por color
    produccion_por_lote.sort(key=lambda x: (x['tipo_lote'].lower(), x['color'].lower()))
    
    datos = {
        'produccion_por_lote': produccion_por_lote,
        'total_unidades': total_unidades,
        'totales_por_talla': totales_por_talla,
        'total_venta': total_venta
    }
    
    fecha_hora_bogota = obtener_fecha_hora_bogota()
    
    return templates.TemplateResponse("resultado_produccion.html", {
        "request": request,
        "datos": datos,
        "fecha_hora_bogota": fecha_hora_bogota
    })

@router.post("/descargar-produccion-pdf")
async def descargar_produccion_pdf(request: Request):
    """
    Genera y descarga un PDF del reporte de producción
    """
    try:
        from reportlab.lib.pagesizes import landscape, A4
        from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
        from reportlab.lib.units import inch
        from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
        from reportlab.lib import colors
        
        # Obtener los datos del formulario enviado
        form_data = await request.json()
        datos = form_data.get('datos', {})
        fecha_hora = form_data.get('fecha_hora', '')
        
        # Crear el PDF en memoria
        pdf_buffer = io.BytesIO()
        doc = SimpleDocTemplate(pdf_buffer, pagesize=landscape(A4), topMargin=0.5*inch, bottomMargin=0.5*inch)
        
        # Elementos del documento
        elements = []
        
        # Título
        styles = getSampleStyleSheet()
        title_style = ParagraphStyle(
            'CustomTitle',
            parent=styles['Heading1'],
            fontSize=18,
            textColor=colors.HexColor('#667eea'),
            spaceAfter=10,
            alignment=1  # Centro
        )
        elements.append(Paragraph('📊 Reporte de Producción', title_style))
        elements.append(Spacer(1, 0.3*inch))
        
        # Información general
        info_style = ParagraphStyle(
            'Info',
            parent=styles['Normal'],
            fontSize=10,
            textColor=colors.grey
        )
        elements.append(Paragraph(f'Fecha y hora: {fecha_hora}', info_style))
        elements.append(Paragraph(f'Total de unidades: <b>{datos.get("total_unidades", 0)}</b>', info_style))
        elements.append(Spacer(1, 0.2*inch))
        
        # Crear tabla
        table_data = [['Tipo de Lote', 'Color', '18-24', '24-36', '36-48', '2', '4', '6', '8', '10', '12', '14', '16', '18', 'Total']]
        
        # Agregar datos de producción
        produccion = datos.get('produccion_por_lote', [])
        for lote in produccion:
            row = [
                lote.get('tipo_lote', ''),
                lote.get('color', ''),
                str(lote.get('tallas', {}).get('18-24', 0)),
                str(lote.get('tallas', {}).get('24-36', 0)),
                str(lote.get('tallas', {}).get('36-48', 0)),
                str(lote.get('tallas', {}).get('2', 0)),
                str(lote.get('tallas', {}).get('4', 0)),
                str(lote.get('tallas', {}).get('6', 0)),
                str(lote.get('tallas', {}).get('8', 0)),
                str(lote.get('tallas', {}).get('10', 0)),
                str(lote.get('tallas', {}).get('12', 0)),
                str(lote.get('tallas', {}).get('14', 0)),
                str(lote.get('tallas', {}).get('16', 0)),
                str(lote.get('tallas', {}).get('18', 0)),
                str(lote.get('total', 0))
            ]
            table_data.append(row)
        
        # Fila de totales
        totales = datos.get('totales_por_talla', {})
        totales_row = ['Total por Talla', '', 
                      str(totales.get('18-24', 0)),
                      str(totales.get('24-36', 0)),
                      str(totales.get('36-48', 0)),
                      str(totales.get('2', 0)),
                      str(totales.get('4', 0)),
                      str(totales.get('6', 0)),
                      str(totales.get('8', 0)),
                      str(totales.get('10', 0)),
                      str(totales.get('12', 0)),
                      str(totales.get('14', 0)),
                      str(totales.get('16', 0)),
                      str(totales.get('18', 0)),
                      str(datos.get('total_unidades', 0))]
        table_data.append(totales_row)
        
        # Crear tabla
        table = Table(table_data, colWidths=[1*inch]*15)
        table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#667eea')),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 9),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, -1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ('FONTSIZE', (0, 1), (-1, -1), 8),
            ('ROWBACKGROUNDS', (0, 1), (-1, -2), [colors.white, colors.lightgrey])
        ]))
        
        elements.append(table)
        
        # Construir PDF
        doc.build(elements)
        
        # Retornar el PDF
        pdf_buffer.seek(0)
        return FileResponse(
            iter([pdf_buffer.getvalue()]),
            media_type="application/pdf",
            headers={"Content-Disposition": "attachment; filename=Reporte_Produccion.pdf"}
        )
    
    except ImportError:
        # Si no está disponible reportlab, retornar error
        raise HTTPException(
            status_code=400,
            detail="Librería reportlab no disponible. Usa la descarga desde el navegador."
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error al generar PDF: {str(e)}"
        )

@router.get("/costo-operacion", response_class=HTMLResponse)
async def mostrar_formulario(request: Request):
    return templates.TemplateResponse("calcular_ costo_operacion.html", {"request": request})

@router.get("/punto-equilibrio", response_class=HTMLResponse)
async def mostrar_punto_equilibrio(request: Request):
    return templates.TemplateResponse("punto_equilibrio.html", {"request": request})

@router.post("/calcular-costo-operacion", response_class=HTMLResponse)
#calculo de costo de operacion
async def calcular_costo(request: Request):
    """
    Calcula el costo de operación consultando ÚNICAMENTE los trabajadores de la base de datos.
    Las cantidades y salarios se calculan automáticamente basados en los trabajadores activos.
    """
    db = get_db()
    if db is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "No se pudo conectar a la base de datos"
        })
    
    try:
        # Obtener trabajadores de la base de datos
        resultado_trabajadores = listar_trabajadores(db)
        
        if not resultado_trabajadores["success"]:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Error al obtener trabajadores"
            })
        
        trabajadores = resultado_trabajadores["data"]
        
        # Contar trabajadores por cargo
        operarias = [t for t in trabajadores if t['cargo'].lower() == 'operaria']
        aprendices = [t for t in trabajadores if t['cargo'].lower() == 'aprendiz']
        
        # Obtener cantidades reales de trabajadores
        cantidad_trabajadoras = len(operarias)
        cantidad_trabajadoras_prestaciones = 0  # Se asume que todas las operarias tienen prestaciones
        cantidad_practicantes = len(aprendices)
        
        # Calcular salarios promedio por cargo
        salario_operaria = sum(t['salario'] for t in operarias) / len(operarias) if operarias else 56000
        salario_operaria_prestaciones = sum(t['salario'] for t in operarias) / len(operarias) if operarias else 56000
        salario_aprendiz = sum(t['salario'] for t in aprendices) / len(aprendices) if aprendices else 30000
        
        # Datos base
        arriendo_diario = arriendo / 30
        
        # Cálculos
        costo_trabajadoras = cantidad_trabajadoras * salario_operaria
        costo_trabajadoras_prestaciones = cantidad_trabajadoras_prestaciones * salario_operaria_prestaciones
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
            'operarias': operarias,
            'aprendices': aprendices,
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
        
        return templates.TemplateResponse("resultado_costo_operacion.html", {
            "request": request, 
            "datos": datos,
            "fecha_hora_bogota": fecha_hora_bogota
        })
    finally:
        from app.db.connection import close_connection
        close_connection(db)

@router.post("/calcular-equilibrio", response_class=HTMLResponse)
async def calcular_punto_equilibrio(
    request: Request,
    precio_unidad: float = Form(...),
    unidades_fabricadas: int = Form(0)
):
    """
    Calcula el punto de equilibrio consultando ÚNICAMENTE los salarios de la base de datos.
    Las cantidades se reciben del formulario pero los salarios vienen SIEMPRE de la DB.
    """
    db = get_db()
    if db is None:
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error": "No se pudo conectar a la base de datos"
        })
    
    try:
        # Obtener trabajadores de la base de datos
        resultado_trabajadores = listar_trabajadores(db)
        
        if not resultado_trabajadores["success"]:
            return templates.TemplateResponse("error.html", {
                "request": request,
                "error": "Error al obtener trabajadores"
            })
        
        trabajadores = resultado_trabajadores["data"]
        
        # Contar trabajadores por cargo
        operarias = [t for t in trabajadores if t['cargo'].lower() == 'operaria']
        aprendices = [t for t in trabajadores if t['cargo'].lower() == 'aprendiz']
        
        # Obtener cantidades reales de trabajadores
        cantidad_trabajadoras = len(operarias)
        cantidad_trabajadoras_prestaciones = 0  # Se asume que todas las operarias tienen prestaciones
        cantidad_practicantes = len(aprendices)
        
        # Calcular salarios promedio por cargo
        salario_operaria = sum(t['salario'] for t in operarias) / len(operarias) if operarias else 56000
        salario_operaria_prestaciones = sum(t['salario'] for t in operarias) / len(operarias) if operarias else 56000
        salario_aprendiz = sum(t['salario'] for t in aprendices) / len(aprendices) if aprendices else 30000
        
        # Datos base
        arriendo_diario = arriendo / 30

        # Cálculo del costo fijo total
        costo_trabajadoras = cantidad_trabajadoras * salario_operaria
        costo_trabajadoras_prestaciones = cantidad_trabajadoras_prestaciones * salario_operaria_prestaciones
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
            'operarias': operarias,
            'aprendices': aprendices,
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
    finally:
        from app.db.connection import close_connection
        close_connection(db)

@router.get("/cost_operation")
async def get_cost_operation(cantidad_trabajadoras: int, cantidad_trabajadoras_prestaciones: int, cantidad_practicantes: int):
    """
    Obtiene el costo de operación consultando ÚNICAMENTE los salarios de la base de datos.
    Los salarios SIEMPRE vienen de la DB, nunca del formulario.
    """
    db = get_db()
    if db is None:
        return JSONResponse(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            content={"error": "No se pudo conectar a la base de datos"}
        )
    
    try:
        # Obtener trabajadores de la base de datos
        resultado_trabajadores = listar_trabajadores(db)
        
        if not resultado_trabajadores["success"]:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content={"error": "Error al obtener trabajadores"}
            )
        
        trabajadores = resultado_trabajadores["data"]
        
        # Obtener salarios ÚNICAMENTE de la base de datos
        # Calcular promedio de salarios por cargo
        operarias = [t for t in trabajadores if t['cargo'].lower() == 'operaria']
        aprendices = [t for t in trabajadores if t['cargo'].lower() == 'aprendiz']
        
        # Calcular promedio de salarios por cargo
        salario_operaria = sum(t['salario'] for t in operarias) / len(operarias) if operarias else 56000
        salario_operaria_prestaciones = sum(t['salario'] for t in operarias) / len(operarias) if operarias else 56000
        salario_aprendiz = sum(t['salario'] for t in aprendices) / len(aprendices) if aprendices else 30000
        
        arriendo_x_dia = arriendo / 30

        costo_operacion = (cantidad_trabajadoras * salario_operaria + 
                          cantidad_trabajadoras_prestaciones * salario_operaria_prestaciones +
                          cantidad_practicantes * salario_aprendiz + 
                          gastos_fijos['hilos'] + 
                          gastos_fijos['luz'] + 
                          gastos_fijos['maquinas'] + 
                          arriendo_x_dia)
        
        return JSONResponse(content={"costo_operacion": costo_operacion})
    finally:
        from app.db.connection import close_connection
        close_connection(db)

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


# =====================
# ENDPOINTS DE TRABAJADORES
# =====================

@router.post("/api/trabajadores/crear", response_class=JSONResponse)
async def crear_nuevo_trabajador(
    nombre: str = Form(...),
    apellido: str = Form(...),
    cedula: str = Form(...),
    cargo: str = Form(...),
    salario: float = Form(...),
    email: str = Form(None),
    telefono: str = Form(None)
):
    """
    Crea un nuevo trabajador en la base de datos.
    
    Parámetros:
    - nombre: Nombre del trabajador
    - apellido: Apellido del trabajador
    - cedula: Cédula del trabajador (única)
    - cargo: Cargo del trabajador
    - salario: Salario del trabajador
    - email: Email del trabajador (opcional)
    - telefono: Teléfono del trabajador (opcional)
    """
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = crear_trabajador(
            db=db,
            nombre=nombre,
            apellido=apellido,
            cedula=cedula,
            cargo=cargo,
            salario=salario,
            email=email,
            telefono=telefono
        )
        
        if resultado["success"]:
            return JSONResponse(
                status_code=status.HTTP_201_CREATED,
                content=resultado
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_400_BAD_REQUEST,
                content=resultado
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.get("/api/trabajadores", response_class=JSONResponse)
async def obtener_lista_trabajadores():
    """Obtiene la lista de todos los trabajadores activos"""
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = listar_trabajadores(db)
        return JSONResponse(content=resultado)
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.get("/api/trabajadores/{trabajador_id}", response_class=JSONResponse)
async def obtener_info_trabajador(trabajador_id: int):
    """Obtiene la información de un trabajador específico"""
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = obtener_trabajador(db, trabajador_id)
        
        if resultado["success"]:
            return JSONResponse(content=resultado)
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=resultado
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.put("/api/trabajadores/{trabajador_id}", response_class=JSONResponse)
async def actualizar_info_trabajador(
    trabajador_id: int,
    nombre: str = Form(None),
    apellido: str = Form(None),
    email: str = Form(None),
    telefono: str = Form(None),
    cargo: str = Form(None),
    salario: float = Form(None),
    activo: bool = Form(None)
):
    """Actualiza la información de un trabajador"""
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        kwargs = {
            "nombre": nombre,
            "apellido": apellido,
            "email": email,
            "telefono": telefono,
            "cargo": cargo,
            "salario": salario,
            "activo": activo
        }
        
        resultado = actualizar_trabajador(db, trabajador_id, **kwargs)
        
        if resultado["success"]:
            return JSONResponse(content=resultado)
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=resultado
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)


@router.delete("/api/trabajadores/{trabajador_id}", response_class=JSONResponse)
async def eliminar_info_trabajador(trabajador_id: int):
    """Elimina (desactiva) un trabajador"""
    db = get_db()
    if db is None:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail="No se pudo conectar a la base de datos"
        )
    
    try:
        resultado = eliminar_trabajador(db, trabajador_id)
        
        if resultado["success"]:
            return JSONResponse(
                status_code=status.HTTP_200_OK,
                content=resultado
            )
        else:
            return JSONResponse(
                status_code=status.HTTP_404_NOT_FOUND,
                content=resultado
            )
    finally:
        from app.db.connection import close_connection
        close_connection(db)
