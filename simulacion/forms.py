from django import forms
from .models import Simulacion, TipoAlga

class SimulacionForm(forms.ModelForm):
    """
    Formulario para crear una nueva simulación.
    Los usuarios ingresan las toneladas deseadas y la fecha objetivo.
    """
    class Meta:
        model = Simulacion
        fields = ['tipo_alga', 'toneladas_deseadas', 'fecha_objetivo', 'notas']
        widgets = {
            'tipo_alga': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }),
            'toneladas_deseadas': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ej: 10.5',
                'step': '0.01',
                'min': '0.01',
                'required': True
            }),
            'fecha_objetivo': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                'required': True
            }),
            'notas': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Notas adicionales (opcional)'
            }),
        }
        labels = {
            'tipo_alga': 'Tipo de Alga',
            'toneladas_deseadas': 'Toneladas Deseadas',
            'fecha_objetivo': 'Fecha Objetivo de Entrega',
            'notas': 'Notas Adicionales'
        }
        help_texts = {
            'toneladas_deseadas': 'Cantidad de toneladas que desea obtener al final',
            'fecha_objetivo': 'Fecha en la que necesita tener las algas listas',
        }

    def clean_toneladas_deseadas(self):
        """
        Validar que las toneladas sean un número positivo.
        """
        toneladas = self.cleaned_data.get('toneladas_deseadas')
        if toneladas and toneladas <= 0:
            raise forms.ValidationError('Las toneladas deben ser un número positivo.')
        return toneladas

    def clean_fecha_objetivo(self):
        """
        Validar que la fecha objetivo sea futura.
        """
        from datetime import date
        fecha = self.cleaned_data.get('fecha_objetivo')
        if fecha and fecha < date.today():
            raise forms.ValidationError('La fecha objetivo debe ser futura.')
        return fecha
