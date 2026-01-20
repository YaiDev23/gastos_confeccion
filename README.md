# 📊 Sistema de Gestión de Costos de Confección

Un sistema web completo para gestionar costos operacionales, producción, entregas y asistencia de trabajadores en una empresa de confección.

---

## 🎨 Tema de Colores (Regla 70-20-10)

- **70%** - `#0B1023` (Azul oscuro - Color principal)
- **20%** - `#E3DFFF` (Púrpura claro - Color secundario)
- **10%** - `#000000` (Negro - Acentos)

---

## 🚀 Características Principales

### 1. **Autenticación y Usuarios**
- Login seguro con validación de credenciales
- Control de roles (Admin, Operario, Supervisor)
- Gestión de usuarios y permisos
- Sesiones persistentes

### 2. **Gestión de Entregas de Corte**
- Registro de entregas de productos
- Seguimiento por taller/responsable
- Búsqueda y filtrado avanzado
- Edición y eliminación de entregas
- Vista detallada de cada entrega

### 3. **Cálculos y Análisis**
- **Costo de Operación**: Calcula costos basados en cantidad de trabajadores
- **Punto de Equilibrio**: Análisis financiero de rentabilidad
- **Justicia de Pago**: Cálculo equitativo de salarios
- **Producción**: Seguimiento de unidades producidas

### 4. **Gestión de Talleres**
- Registro y edición de talleres
- Listado completo con detalles
- Vinculación con entregas

---

## 📂 Estructura del Proyecto

```
gastos_confeccion/
├── app/
│   ├── api/                    # Endpoints y rutas
│   │   ├── auth_endpoints.py           # Autenticación
│   │   ├── delivery_endpoints.py       # Entregas (CRUD)
│   │   ├── endpoints.py                # Cálculos
│   │   ├── endpoints_assistence.py     # Asistencia
│   │   ├── factory_endpoints.py        # Talleres (CRUD)
│   │   ├── templates_endpoints.py      # Renderizado de vistas
│   │   ├── worker_endpoints.py         # Trabajadores (CRUD)
│   │   └── schemas/                    # Validación de datos
│   ├── db/                     # Base de datos
│   │   ├── connection.py               # Conexión DB
│   │   └── models/                     # Modelos SQLAlchemy
│   ├── service/                # Lógica de negocio
│   │   ├── assistence_service.py
│   │   ├── delivery_service.py
│   │   ├── factory_service.py
│   │   ├── user_service.py
│   │   └── worker_service.py
│   ├── static/                 # Archivos estáticos
│   │   ├── css/                        # Estilos CSS
│   │   └── img/                        # Imágenes
│   └── templates/              # Plantillas HTML
│       ├── delivery/                   # Vistas de entregas
│       ├── assistence/                 # Vistas de asistencia
│       └── *.html                      # Vistas generales
├── main.py                     # Punto de entrada
├── docker-compose.yml          # Configuración Docker
└── requierements.txt           # Dependencias
```

---

## 🖥️ Ventanas y Funciones

### **1. Login** (`/` - login.html)
**Descripción**: Autenticación de usuarios en el sistema
- ✅ Validación de usuario y contraseña
- ✅ Almacenamiento de sesión
- ✅ Mensajes de error
- ✅ Redirección al menú principal

**Usuarios de prueba**: Configurado en la base de datos

---

### **2. Menú Principal** (`/menu` - menu.html)
**Descripción**: Panel principal con acceso a todas las funcionalidades
- 📦 Entregas de corte
- 📊 Cálculos (Costo, Equilibrio, Justicia de Pago)
- 👥 Gestión de trabajadores
- 🏭 Gestión de talleres
- ⏱️ Control de asistencia
- 📈 Producción

---

## 📦 MÓDULO DE ENTREGAS

### **3. Registrar Entrega** (`/entrega_corte` - agregar_entrega.html)
**Descripción**: Formulario para registrar nuevas entregas de corte
- ✅ Selección de taller/responsable (búsqueda)
- ✅ Fecha de entrega
- ✅ Número de lote
- ✅ Tipo de producto
- ✅ Color del producto
- ✅ Tabla de cantidades por talla (6-12, 12-18, 18-24, 24-36, 36-48, 2-18)
- ✅ Observaciones
- ✅ Validaciones en tiempo real

**API Endpoint**: `POST /api/deliveries`

---

### **4. Consultar Entregas** (`/consultar_entrega` - consultar_entrega.html)
**Descripción**: Vista de todas las entregas registradas (Solo Admin)
- 🔍 Búsqueda por responsable, lote, tipo, color
- 📊 Filtros y ordenamiento
- 📋 Tabla con detalles
- ✏️ Editar entrega
- 🗑️ Eliminar entrega
- 👁️ Ver detalles completos en modal

**API Endpoints**:
- `GET /api/deliveries` - Obtener todas
- `GET /api/deliveries/{id}` - Obtener por ID
- `PUT /api/deliveries/{id}` - Actualizar
- `DELETE /api/deliveries/{id}` - Eliminar

---

### **5. Menú de Entregas** (`/menu_entrega` - menu_entrega.html)
**Descripción**: Submenu con opciones de entregas
- ➕ Registrar entrega
- 📋 Ver entregas (solo admin)
- 📊 Reportes (en desarrollo)

---

### **6. Agregar Taller** (`/agregar-taller` - delivery/agregar_taller.html)
**Descripción**: Registro de nuevos talleres responsables
- ✅ Nombre del propietario
- ✅ Información sobre el proceso
- ✅ Validaciones

**API Endpoint**: `POST /api/factory`

---

### **7. Lista de Talleres** (`/factories` - delivery/lista_talleres.html)
**Descripción**: Visualización de todos los talleres registrados
- 📊 Tabla con ID y propietario
- ✏️ Editar taller
- 🗑️ Eliminar taller
- ➕ Agregar nuevo taller
- 📈 Total de talleres registrados

**API Endpoints**:
- `GET /api/factories` - Obtener todas
- `DELETE /api/factories/{id}` - Eliminar

---

## 📊 MÓDULO DE CÁLCULOS

### **8. Producción** (`/produccion` - produccion.html)
**Descripción**: Cálculo y análisis de producción
- 📊 Ingreso de cantidad producida
- 📈 Cálculo de rendimiento
- 📥 Descarga de PDF

**API Endpoint**: `POST /calcular-produccion`

---

### **9. Costo de Operación** (`/costo-operacion` - calcular_costo_operacion.html)
**Descripción**: Calcula costos operacionales basado en cantidad de trabajadores
- 👥 Cantidad de trabajadoras
- 👥 Cantidad de trabajadoras con prestaciones
- 👥 Cantidad de practicantes
- 💰 Desglose de costos (arriendo, servicios, salarios, etc.)
- 📈 Costo unitario por prenda

**Campos calculados**:
- Salario básico trabajadora
- Salario con prestaciones
- Costo de practicante
- Costo fijo total
- Costo variable
- Costo unitario

**API Endpoint**: `POST /calcular-costo-operacion`

---

### **10. Punto de Equilibrio** (`/punto-equilibrio` - punto_equilibrio.html)
**Descripción**: Análisis del punto de equilibrio financiero
- 💵 Precio del producto
- 💰 Costo variable unitario
- 💸 Costo fijo total
- 📊 Unidades necesarias para equilibrio
- 💹 Análisis de rentabilidad

**Fórmula**: Punto de equilibrio = Costo fijo / (Precio - Costo variable)

**API Endpoint**: `POST /calcular-equilibrio`

---

### **11. Justicia de Pago** (`/justicia-pago` - justicia_pago.html)
**Descripción**: Cálculo equitativo de salarios para trabajadores
- 👥 Cantidad de trabajadores
- 💰 Monto total a distribuir
- 📈 Distribución proporcional
- 💵 Monto por trabajador

**API Endpoint**: `POST /calcular-justicia-pago`

---

## 👥 MÓDULO DE TRABAJADORES

### **12. Agregar Trabajador** (`/agregar-trabajador` - agregar_trabajador.html)
**Descripción**: Registro de nuevos trabajadores
- ✅ Nombre completo
- ✅ Cargo/Puesto
- ✅ Salario
- ✅ Validaciones

**API Endpoint**: `POST /api/workers`

---

### **13. Lista de Trabajadores** (`/trabajadores` - lista_trabajadores.html)
**Descripción**: Vista de todos los trabajadores
- 📊 Tabla con detalles
- ✏️ Editar trabajador
- 🗑️ Eliminar trabajador
- 🔍 Búsqueda

**API Endpoint**: `GET /api/workers`

---

### **14. Editar Trabajador** (`/editar-trabajador` - editar_trabajador.html)
**Descripción**: Modificación de datos de trabajador
- ✏️ Editar información
- 💾 Guardar cambios

**API Endpoint**: `PUT /api/workers/{id}`

---

## ⏱️ MÓDULO DE ASISTENCIA

### **15. Marcar Asistencia** (`/asistencia` - assistence/marcar_asistencia.html)
**Descripción**: Control de asistencia y horarios
- ⏰ Marcación de entrada
- ⏰ Marcación de salida
- 📊 Resumen de asistencia
- 📈 Reporte por empleado

**API Endpoints**:
- `POST /assistence/llegada` - Marcar entrada
- `POST /assistence/salida` - Marcar salida
- `GET /assistence/resumen` - Obtener resumen

---

## 🔐 Sistema de Roles y Permisos

### **Roles Disponibles**:
- **Admin**: Acceso a todas las funciones
- **Supervisor**: Acceso limitado a reportes
- **Operario**: Acceso solo a entrada/salida

### **Control de Acceso**:
Se valida mediante `RolePermissions` en `utils/permissions.py`

---

## 🛠️ Tecnologías Utilizadas

- **Backend**: FastAPI
- **Base de Datos**: MySQL + SQLAlchemy ORM
- **Frontend**: Jinja2 Templates, HTML5, CSS3, JavaScript
- **Autenticación**: Sessions + SessionStorage
- **Generación de PDF**: ReportLab, WeasyPrint
- **Contenedorización**: Docker, Docker Compose

---

## 📦 Dependencias Principales

```
fastapi          - Framework web
jinja2          - Motor de plantillas
sqlalchemy      - ORM para BD
pymysql         - Driver MySQL
uvicorn         - Servidor ASGI
python-dotenv   - Variables de entorno
reportlab       - Generación de PDF
weasyprint      - Conversión HTML a PDF
```

---

## 🚀 Instalación y Ejecución

### **Requisitos**:
- Python 3.8+
- MySQL 5.7+
- Docker (opcional)

### **Sin Docker**:
```bash
# Crear entorno virtual
python -m venv .venv
source .venv/bin/activate

# Instalar dependencias
pip install -r requierements.txt

# Ejecutar servidor
python main.py
```

### **Con Docker**:
```bash
docker-compose up -d
```

El servidor estará disponible en: `http://localhost:8001`

---

## 📊 Flujo de Navegación

```
Login
  ↓
Menú Principal
  ├── Entregas → Registrar → Consultar → Editar/Eliminar
  ├── Cálculos → Producción/Costo/Equilibrio/Justicia
  ├── Trabajadores → Agregar → Listar → Editar
  ├── Talleres → Agregar → Listar
  └── Asistencia → Marcar entrada/salida → Resumen
```

---

## 🎨 Diseño de Interfaz

- **Tema**: Moderno y profesional
- **Responsive**: Adaptado a dispositivos móviles
- **Accesibilidad**: Contraste de colores optimizado
- **Paleta de colores**: 70-20-10 (Azul oscuro, Púrpura claro, Negro)

---

## 📝 Notas Importantes

- ✅ Todas las ventanas utilizan la paleta de colores consistente
- ✅ Los formularios incluyen validaciones en cliente y servidor
- ✅ Las tablas son responsivas y permiten búsqueda/filtrado
- ✅ Los modales muestran detalles completos de registros
- ✅ Los cálculos se procesan en el servidor para precisión

---

## 👨‍💻 Autor

Proyecto desarrollado con FastAPI y JavaScript vanilla.

---

## 📄 Licencia

Proyecto privado - 2025
