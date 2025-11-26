from django.contrib import admin
from .models import TipoAlga, ParametroSimulacion, Simulacion

# Configuración del admin para TipoAlga
@admin.register(TipoAlga)
class TipoAlgaAdmin(admin.ModelAdmin):
    """
    Panel de administración para gestionar los tipos de algas.
    """
    list_display = ('nombre', 'tiempo_cultivo_dias', 'porcentaje_perdida', 'creado_en')
    list_filter = ('creado_en',)
    search_fields = ('nombre', 'descripcion')
    ordering = ('nombre',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion')
        }),
        ('Parámetros de Cultivo', {
            'fields': ('tiempo_cultivo_dias', 'porcentaje_perdida')
        }),
    )


# Configuración del admin para ParametroSimulacion
@admin.register(ParametroSimulacion)
class ParametroSimulacionAdmin(admin.ModelAdmin):
    """
    Panel de administración para gestionar parámetros de simulación.
    """
    list_display = ('nombre', 'estacion', 'factor_ajuste', 'activo', 'creado_en')
    list_filter = ('estacion', 'activo', 'creado_en')
    search_fields = ('nombre', 'descripcion')
    ordering = ('-creado_en',)
    
    fieldsets = (
        ('Información Básica', {
            'fields': ('nombre', 'descripcion', 'activo')
        }),
        ('Configuración', {
            'fields': ('estacion', 'factor_ajuste')
        }),
    )


# Configuración del admin para Simulacion
@admin.register(Simulacion)
class SimulacionAdmin(admin.ModelAdmin):
    """
    Panel de administración para ver y gestionar simulaciones.
    """
    list_display = (
        'id',
        'usuario',
        'tipo_alga',
        'toneladas_deseadas',
        'fecha_objetivo',
        'toneladas_a_plantar',
        'creado_en'
    )
    list_filter = ('tipo_alga', 'creado_en', 'fecha_objetivo')
    search_fields = ('usuario__username', 'tipo_alga__nombre', 'notas')
    ordering = ('-creado_en',)
    readonly_fields = ('creado_en',)
    
    fieldsets = (
        ('Usuario', {
            'fields': ('usuario',)
        }),
        ('Datos de Entrada', {
            'fields': ('tipo_alga', 'toneladas_deseadas', 'fecha_objetivo')
        }),
        ('Resultados Calculados', {
            'fields': ('toneladas_a_plantar', 'fecha_inicio_cultivo', 'dias_cultivo')
        }),
        ('Información Adicional', {
            'fields': ('notas', 'creado_en'),
            'classes': ('collapse',)
        }),
    )
    
    def save_model(self, request, obj, form, change):
        """
        Sobrescribir el método save para calcular automáticamente 
        los resultados de la simulación antes de guardar.
        """
        if not change or any(field in form.changed_data for field in ['toneladas_deseadas', 'fecha_objetivo', 'tipo_alga']):
            obj.calcular_simulacion()
        super().save_model(request, obj, form, change)
