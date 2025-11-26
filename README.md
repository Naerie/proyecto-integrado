# Simulador de Cultivo de Algas

Sistema de simulación de escenarios productivos para un centro de cultivo de algas ubicado en Caldera, Chile.

## Descripción del Proyecto

Este sistema permite calcular cuántas algas se necesitan plantar para obtener una cantidad específica de toneladas en una fecha determinada, considerando los porcentajes de pérdida durante el cultivo y los tiempos de maduración de cada tipo de alga.

### Funcionalidades Principales

- **Gestión de Tipos de Algas**: Administrar diferentes tipos de algas (Entera, Pellet, Micronizada) con sus parámetros específicos
- **Simulación de Producción**: Calcular automáticamente:
  - Toneladas a plantar considerando pérdidas
  - Fecha de inicio de cultivo
  - Días de cultivo necesarios
- **Exportación a PDF**: Generar reportes profesionales con todos los detalles de la simulación
- **Sistema de Autenticación**: Control de acceso con usuarios y roles
- **Panel de Administración**: Gestionar parámetros del sistema

## Tecnologías Utilizadas

- **Backend**: Django 5.2.8
- **Base de Datos**: SQLite (por defecto)
- **Frontend**: Bootstrap 5.3, HTML5, CSS3
- **Generación de PDF**: ReportLab
- **Iconos**: Font Awesome 6.4

## Requisitos del Sistema

- Python 3.11 o superior
- pip (gestor de paquetes de Python)
- Navegador web moderno (Chrome, Firefox, Edge, Safari)

## Instalación

### 1. Entrar en la carpeta por consola

```bash
cd proyecto_django_algas
```

### 2. Crear y activar el entorno virtual

**En Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

**En Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Instalar las dependencias

```bash
pip install -r requirements.txt
```

Si no existe el archivo `requirements.txt`, instalar manualmente:
```bash
pip install django reportlab pillow
```

### 4. Aplicar las migraciones de la base de datos

```bash
python manage.py migrate
```

### 5. Crear un superusuario (administrador)

```bash
python manage.py createsuperuser
```

Ingrese los datos solicitados:
- Usuario: `admin` (o el que prefiera)
- Email: `admin@algas.cl`
- Contraseña: (la que prefiera, mínimo 8 caracteres)

### 6. Cargar datos de ejemplo (opcional)

```bash
python manage.py shell
```

Luego ejecutar:
```python
from simulacion.models import TipoAlga

TipoAlga.objects.create(
    nombre="Alga Entera",
    descripcion="Alga en su estado natural, sin procesar",
    tiempo_cultivo_dias=90,
    porcentaje_perdida=20.00
)

TipoAlga.objects.create(
    nombre="Alga Pellet",
    descripcion="Alga procesada en formato de pellets comprimidos",
    tiempo_cultivo_dias=90,
    porcentaje_perdida=25.00
)

TipoAlga.objects.create(
    nombre="Alga Micronizada",
    descripcion="Alga procesada y micronizada para uso como suplemento alimenticio",
    tiempo_cultivo_dias=90,
    porcentaje_perdida=30.00
)

exit()
```

### 7. Iniciar el servidor de desarrollo

```bash
python manage.py runserver
```

El sistema estará disponible en: http://127.0.0.1:8000/

## Uso del Sistema

### Acceso al Sistema

1. **Página Principal**: http://127.0.0.1:8000/
2. **Iniciar Sesión**: http://127.0.0.1:8000/accounts/login/
3. **Panel de Administración**: http://127.0.0.1:8000/admin/

### Credenciales de Acceso

**Usuario por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

### Crear una Simulación

1. Iniciar sesión en el sistema
2. Hacer clic en "Nueva Simulación"
3. Completar el formulario:
   - Seleccionar el tipo de alga
   - Ingresar las toneladas deseadas
   - Seleccionar la fecha objetivo
   - Agregar notas adicionales (opcional)
4. Hacer clic en "Calcular Simulación"
5. Ver los resultados calculados automáticamente

### Ver Simulaciones

- Acceder a "Mis Simulaciones" para ver todas las simulaciones creadas
- Hacer clic en "Ver Detalles" para ver información completa
- Descargar el reporte en PDF haciendo clic en "Descargar PDF"

### Panel de Administración

El administrador puede:
- Gestionar tipos de algas (agregar, editar, eliminar)
- Configurar parámetros de simulación
- Ver todas las simulaciones de todos los usuarios
- Gestionar usuarios del sistema

## Estructura del Proyecto

```
proyecto_django_algas/
├── manage.py                          # Comando principal de Django
├── simulador_algas/                   # Configuración del proyecto
│   ├── settings.py                    # Configuración general
│   ├── urls.py                        # URLs principales
│   └── wsgi.py                        # Configuración WSGI
├── simulacion/                        # Aplicación principal
│   ├── models.py                      # Modelos de base de datos
│   ├── views.py                       # Vistas (lógica de negocio)
│   ├── forms.py                       # Formularios
│   ├── urls.py                        # URLs de la aplicación
│   ├── admin.py                       # Configuración del admin
│   ├── templates/                     # Plantillas HTML
│   │   ├── simulacion/
│   │   │   ├── base.html             # Plantilla base
│   │   │   ├── inicio.html           # Página de inicio
│   │   │   ├── nueva_simulacion.html # Formulario de simulación
│   │   │   ├── lista_simulaciones.html
│   │   │   ├── detalle_simulacion.html
│   │   │   └── eliminar_simulacion.html
│   │   └── registration/
│   │       └── login.html            # Página de login
│   └── migrations/                    # Migraciones de base de datos
├── db.sqlite3                         # Base de datos SQLite
├── venv/                              # Entorno virtual (no incluir en git)
└── README.md                          # Este archivo
```

## Modelos de Datos

### TipoAlga
- `nombre`: Nombre del tipo de alga
- `descripcion`: Descripción del tipo
- `tiempo_cultivo_dias`: Días necesarios para el cultivo
- `porcentaje_perdida`: Porcentaje de pérdida durante el cultivo

### Simulacion
- `usuario`: Usuario que creó la simulación
- `tipo_alga`: Tipo de alga seleccionado
- `toneladas_deseadas`: Cantidad deseada (entrada)
- `fecha_objetivo`: Fecha objetivo de entrega (entrada)
- `toneladas_a_plantar`: Cantidad a plantar (calculado)
- `fecha_inicio_cultivo`: Fecha de inicio (calculado)
- `dias_cultivo`: Días de cultivo (calculado)
- `notas`: Notas adicionales

### ParametroSimulacion
- `nombre`: Nombre del parámetro
- `estacion`: Estación del año
- `factor_ajuste`: Factor de ajuste
- `descripcion`: Descripción
- `activo`: Estado del parámetro

## Lógica de Cálculo

### Cálculo de Toneladas a Plantar

```
Toneladas a Plantar = Toneladas Deseadas × (1 + Porcentaje Pérdida / 100)
```

**Ejemplo:**
- Toneladas deseadas: 10 t
- Porcentaje de pérdida: 20%
- Resultado: 10 × (1 + 20/100) = 10 × 1.2 = 12 toneladas a plantar

### Cálculo de Fecha de Inicio

```
Fecha Inicio = Fecha Objetivo - Días de Cultivo
```

**Ejemplo:**
- Fecha objetivo: 15/03/2025
- Días de cultivo: 90 días
- Resultado: Inicio el 15/12/2024

## Personalización

### Modificar Tipos de Algas

Acceder al panel de administración y editar los tipos de algas existentes o crear nuevos con diferentes parámetros.

### Cambiar Colores y Estilos

Editar el archivo `simulacion/templates/simulacion/base.html` en la sección `<style>`:

```css
:root {
    --color-primario: #2c3e50;     /* Color principal */
    --color-secundario: #3498db;   /* Color secundario */
    --color-acento: #27ae60;       /* Color de acento */
    --color-fondo: #ecf0f1;        /* Color de fondo */
}
```

### Agregar Nuevos Campos

1. Modificar el modelo en `simulacion/models.py`
2. Crear la migración: `python manage.py makemigrations`
3. Aplicar la migración: `python manage.py migrate`
4. Actualizar formularios, vistas y templates según sea necesario

## Solución de Problemas

### Error: "No module named 'django'"
```bash
pip install django
```

### Error: "No module named 'reportlab'"
```bash
pip install reportlab
```

### La base de datos no existe
```bash
python manage.py migrate
```

### Olvidé la contraseña del administrador
```bash
python manage.py changepassword admin
```

### El servidor no inicia
- Verificar que el puerto 8000 no esté en uso
- Usar otro puerto: `python manage.py runserver 8080`

## Créditos

Proyecto desarrollado como parte de la asignatura de Proyecto Integrado e Ingenieria de software en Inacap copiapó

## Licencia

Este proyecto es de uso educativo y está disponible para fines académicos.
