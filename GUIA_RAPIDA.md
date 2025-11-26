# Guía Rápida - Simulador de Cultivo de Algas

## Inicio Rápido

### 1. Instalación (Primera vez)

```bash
# Crear entorno virtual
python3 -m venv venv

# Activar entorno virtual
# En Linux/Mac:
source venv/bin/activate
# En Windows:
venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser
```

### 2. Iniciar el Servidor

```bash
# Activar entorno virtual (si no está activado)
source venv/bin/activate  # Linux/Mac
# o
venv\Scripts\activate  # Windows

# Iniciar servidor
python manage.py runserver
```

Abrir en el navegador: http://127.0.0.1:8000/

## Credenciales de Acceso

**Usuario por defecto:**
- Usuario: `admin`
- Contraseña: `admin123`

## Uso del Sistema

### Crear una Simulación

1. **Iniciar sesión** con tus credenciales
2. Hacer clic en **"Nueva Simulación"**
3. **Completar el formulario:**
   - Tipo de Alga: Seleccionar (Entera, Pellet o Micronizada)
   - Toneladas Deseadas: Ej. 10
   - Fecha Objetivo: Seleccionar fecha futura
   - Notas: (Opcional)
4. Hacer clic en **"Calcular Simulación"**

### Ver Resultados

El sistema calculará automáticamente:
- ✅ **Toneladas a Plantar**: Cantidad necesaria considerando pérdidas
- ✅ **Fecha de Inicio**: Cuándo debe comenzar el cultivo
- ✅ **Días de Cultivo**: Tiempo necesario para el cultivo

### Exportar a PDF

1. Abrir una simulación
2. Hacer clic en **"Descargar Reporte PDF"**
3. El archivo se descargará automáticamente

## Panel de Administración

Acceder a: http://127.0.0.1:8000/admin/

### Gestionar Tipos de Algas

1. Iniciar sesión en el admin
2. Ir a **"Tipos de Algas"**
3. Hacer clic en **"Agregar Tipo de Alga"**
4. Completar:
   - Nombre: Ej. "Alga Entera"
   - Descripción: Descripción del tipo
   - Tiempo de cultivo (días): Ej. 90
   - Porcentaje de pérdida (%): Ej. 20
5. Guardar

### Ver Todas las Simulaciones

1. En el admin, ir a **"Simulaciones"**
2. Ver lista completa de todas las simulaciones
3. Filtrar por tipo de alga, fecha, usuario, etc.

## Estructura de Carpetas

```
proyecto_django_algas/
├── manage.py              # Comando principal
├── simulador_algas/       # Configuración
├── simulacion/            # Aplicación principal
│   ├── models.py         # Modelos (TipoAlga, Simulacion)
│   ├── views.py          # Vistas (lógica)
│   ├── forms.py          # Formularios
│   ├── urls.py           # URLs
│   ├── admin.py          # Configuración admin
│   └── templates/        # Plantillas HTML
├── db.sqlite3            # Base de datos
├── requirements.txt      # Dependencias
└── README.md            # Documentación completa
```

## Comandos Útiles

```bash
# Iniciar servidor
python manage.py runserver

# Crear migraciones
python manage.py makemigrations

# Aplicar migraciones
python manage.py migrate

# Crear superusuario
python manage.py createsuperuser

# Abrir shell de Django
python manage.py shell

# Cambiar contraseña de usuario
python manage.py changepassword admin
```

## Fórmulas de Cálculo

### Toneladas a Plantar
```
Toneladas a Plantar = Toneladas Deseadas × (1 + Porcentaje Pérdida / 100)
```

**Ejemplo:**
- Deseadas: 10 t
- Pérdida: 20%
- **Resultado: 12 t**

### Fecha de Inicio
```
Fecha Inicio = Fecha Objetivo - Días de Cultivo
```

**Ejemplo:**
- Objetivo: 15/03/2025
- Cultivo: 90 días
- **Resultado: 15/12/2024**

## Solución Rápida de Problemas

| Problema | Solución |
|----------|----------|
| "No module named 'django'" | `pip install django` |
| "No module named 'reportlab'" | `pip install reportlab` |
| Base de datos no existe | `python manage.py migrate` |
| Olvidé contraseña | `python manage.py changepassword admin` |
| Puerto en uso | `python manage.py runserver 8080` |

## Tipos de Algas Predefinidos

| Tipo | Tiempo Cultivo | Pérdida |
|------|----------------|---------|
| Alga Entera | 90 días | 20% |
| Alga Pellet | 90 días | 25% |
| Alga Micronizada | 90 días | 30% |

## Contacto y Soporte

Para consultas o problemas, revisar la documentación completa en `README.md`.


