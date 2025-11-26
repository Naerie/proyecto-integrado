from django.db import models
from django.contrib.auth.models import User

# Modelo para los tipos de algas que se cultivan
class TipoAlga(models.Model):
    """
    Representa los diferentes tipos de algas que se pueden cultivar.
    Ejemplos: Entera, Pellet, Micronizada
    """
    nombre = models.CharField(max_length=100, verbose_name="Nombre del tipo de alga")
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    tiempo_cultivo_dias = models.IntegerField(
        verbose_name="Tiempo de cultivo (días)",
        help_text="Días necesarios para que el alga madure"
    )
    porcentaje_perdida = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Porcentaje de pérdida (%)",
        help_text="Porcentaje de pérdida durante el cultivo (ej: 20 para 20%)"
    )
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Tipo de Alga"
        verbose_name_plural = "Tipos de Algas"
        ordering = ['nombre']

    def __str__(self):
        return self.nombre


# Modelo para los parámetros de simulación
class ParametroSimulacion(models.Model):
    """
    Almacena parámetros generales que afectan la simulación.
    Por ejemplo: factores climáticos, estacionales, etc.
    """
    ESTACION_CHOICES = [
        ('verano', 'Verano'),
        ('otono', 'Otoño'),
        ('invierno', 'Invierno'),
        ('primavera', 'Primavera'),
    ]
    
    nombre = models.CharField(max_length=200, verbose_name="Nombre del parámetro")
    estacion = models.CharField(
        max_length=20,
        choices=ESTACION_CHOICES,
        blank=True,
        null=True,
        verbose_name="Estación del año"
    )
    factor_ajuste = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=1.0,
        verbose_name="Factor de ajuste",
        help_text="Multiplicador para ajustar tiempos/pérdidas (1.0 = sin cambio)"
    )
    descripcion = models.TextField(blank=True, verbose_name="Descripción")
    activo = models.BooleanField(default=True, verbose_name="Activo")
    creado_en = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Parámetro de Simulación"
        verbose_name_plural = "Parámetros de Simulación"
        ordering = ['-creado_en']

    def __str__(self):
        return self.nombre


# Modelo para guardar las simulaciones realizadas
class Simulacion(models.Model):
    """
    Guarda cada simulación realizada por los usuarios.
    Incluye los datos de entrada y los resultados calculados.
    """
    usuario = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name="Usuario",
        related_name="simulaciones"
    )
    tipo_alga = models.ForeignKey(
        TipoAlga,
        on_delete=models.CASCADE,
        verbose_name="Tipo de alga"
    )
    
    # Datos de entrada
    toneladas_deseadas = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Toneladas deseadas"
    )
    fecha_objetivo = models.DateField(
        verbose_name="Fecha objetivo de entrega"
    )
    
    # Resultados calculados
    toneladas_a_plantar = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name="Toneladas a plantar",
        help_text="Cantidad que se debe plantar considerando las pérdidas"
    )
    fecha_inicio_cultivo = models.DateField(
        verbose_name="Fecha de inicio de cultivo"
    )
    dias_cultivo = models.IntegerField(
        verbose_name="Días de cultivo necesarios"
    )
    
    # Metadatos
    notas = models.TextField(
        blank=True,
        verbose_name="Notas adicionales"
    )
    creado_en = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de creación")
    
    class Meta:
        verbose_name = "Simulación"
        verbose_name_plural = "Simulaciones"
        ordering = ['-creado_en']

    def __str__(self):
        return f"Simulación {self.id} - {self.tipo_alga.nombre} - {self.toneladas_deseadas}t"

    def calcular_simulacion(self):
        """
        Método para calcular los resultados de la simulación.
        Considera el porcentaje de pérdida y el tiempo de cultivo.
        """
        # Calcular toneladas a plantar considerando pérdidas
        # Si se pierde un 20%, necesitamos plantar más para compensar
        factor_perdida = 1 + (self.tipo_alga.porcentaje_perdida / 100)
        self.toneladas_a_plantar = self.toneladas_deseadas * factor_perdida
        
        # Calcular días de cultivo
        self.dias_cultivo = self.tipo_alga.tiempo_cultivo_dias
        
        # Calcular fecha de inicio restando los días de cultivo a la fecha objetivo
        from datetime import timedelta
        self.fecha_inicio_cultivo = self.fecha_objetivo - timedelta(days=self.dias_cultivo)
        
        return {
            'toneladas_a_plantar': self.toneladas_a_plantar,
            'fecha_inicio_cultivo': self.fecha_inicio_cultivo,
            'dias_cultivo': self.dias_cultivo,
            'porcentaje_perdida': self.tipo_alga.porcentaje_perdida
        }
