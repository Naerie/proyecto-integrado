from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
from .models import Simulacion, TipoAlga
from .forms import SimulacionForm
from datetime import date

# Vista principal - Página de inicio
def inicio(request):
    """
    Página de inicio del simulador.
    Muestra información general y enlaces a las funcionalidades.
    """
    context = {
        'titulo': 'Simulador de Cultivo de Algas',
        'descripcion': 'Sistema de simulación para calcular producción de algas'
    }
    return render(request, 'simulacion/inicio.html', context)


# Vista para listar todas las simulaciones
@login_required
def lista_simulaciones(request):
    """
    Muestra todas las simulaciones realizadas por el usuario actual.
    """
    simulaciones = Simulacion.objects.filter(usuario=request.user).order_by('-creado_en')
    context = {
        'simulaciones': simulaciones,
        'titulo': 'Mis Simulaciones'
    }
    return render(request, 'simulacion/lista_simulaciones.html', context)


# Vista para crear una nueva simulación
@login_required
def nueva_simulacion(request):
    """
    Formulario para crear una nueva simulación.
    Calcula automáticamente los resultados al guardar.
    """
    if request.method == 'POST':
        form = SimulacionForm(request.POST)
        if form.is_valid():
            # Crear la simulación pero no guardarla aún
            simulacion = form.save(commit=False)
            simulacion.usuario = request.user
            
            # Calcular los resultados de la simulación
            simulacion.calcular_simulacion()
            
            # Guardar la simulación con los resultados
            simulacion.save()
            
            messages.success(request, '¡Simulación creada exitosamente!')
            return redirect('detalle_simulacion', pk=simulacion.pk)
    else:
        form = SimulacionForm()
    
    context = {
        'form': form,
        'titulo': 'Nueva Simulación'
    }
    return render(request, 'simulacion/nueva_simulacion.html', context)


# Vista para ver el detalle de una simulación
@login_required
def detalle_simulacion(request, pk):
    """
    Muestra los detalles completos de una simulación específica.
    Incluye todos los cálculos y resultados.
    """
    simulacion = get_object_or_404(Simulacion, pk=pk, usuario=request.user)
    
    # Calcular días hasta la fecha objetivo
    dias_hasta_objetivo = (simulacion.fecha_objetivo - date.today()).days
    
    # Calcular días hasta inicio de cultivo
    dias_hasta_inicio = (simulacion.fecha_inicio_cultivo - date.today()).days
    
    context = {
        'simulacion': simulacion,
        'dias_hasta_objetivo': dias_hasta_objetivo,
        'dias_hasta_inicio': dias_hasta_inicio,
        'titulo': f'Simulación #{simulacion.id}'
    }
    return render(request, 'simulacion/detalle_simulacion.html', context)


# Vista para eliminar una simulación
@login_required
def eliminar_simulacion(request, pk):
    """
    Elimina una simulación específica.
    """
    simulacion = get_object_or_404(Simulacion, pk=pk, usuario=request.user)
    
    if request.method == 'POST':
        simulacion.delete()
        messages.success(request, 'Simulación eliminada correctamente.')
        return redirect('lista_simulaciones')
    
    context = {
        'simulacion': simulacion,
        'titulo': 'Eliminar Simulación'
    }
    return render(request, 'simulacion/eliminar_simulacion.html', context)


# Vista para exportar simulación a PDF
@login_required
def exportar_pdf(request, pk):
    """
    Exporta una simulación a formato PDF.
    Genera un reporte completo con todos los datos y cálculos.
    """
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib.units import inch
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
    from reportlab.lib import colors
    from reportlab.lib.enums import TA_CENTER
    from io import BytesIO
    
    simulacion = get_object_or_404(Simulacion, pk=pk, usuario=request.user)
    
    # Crear el PDF en memoria
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elementos = []
    
    # Estilos
    estilos = getSampleStyleSheet()
    estilo_titulo = ParagraphStyle(
        'CustomTitle',
        parent=estilos['Heading1'],
        fontSize=24,
        textColor=colors.HexColor('#2c3e50'),
        spaceAfter=30,
        alignment=TA_CENTER
    )
    estilo_subtitulo = ParagraphStyle(
        'CustomSubtitle',
        parent=estilos['Heading2'],
        fontSize=16,
        textColor=colors.HexColor('#34495e'),
        spaceAfter=12,
        spaceBefore=12
    )
    estilo_normal = estilos['Normal']
    
    # Título
    elementos.append(Paragraph('Reporte de Simulación de Cultivo de Algas', estilo_titulo))
    elementos.append(Spacer(1, 0.3*inch))
    
    # Información general
    elementos.append(Paragraph('Información General', estilo_subtitulo))
    datos_generales = [
        ['ID de Simulación:', str(simulacion.id)],
        ['Usuario:', simulacion.usuario.username],
        ['Fecha de Creación:', simulacion.creado_en.strftime('%d/%m/%Y %H:%M')],
        ['Tipo de Alga:', simulacion.tipo_alga.nombre],
    ]
    tabla_general = Table(datos_generales, colWidths=[3*inch, 3*inch])
    tabla_general.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elementos.append(tabla_general)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Datos de entrada
    elementos.append(Paragraph('Datos de Entrada', estilo_subtitulo))
    datos_entrada = [
        ['Toneladas Deseadas:', f"{simulacion.toneladas_deseadas} t"],
        ['Fecha Objetivo:', simulacion.fecha_objetivo.strftime('%d/%m/%Y')],
    ]
    tabla_entrada = Table(datos_entrada, colWidths=[3*inch, 3*inch])
    tabla_entrada.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#ecf0f1')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elementos.append(tabla_entrada)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Resultados calculados
    elementos.append(Paragraph('Resultados de la Simulación', estilo_subtitulo))
    datos_resultados = [
        ['Toneladas a Plantar:', f"{simulacion.toneladas_a_plantar} t"],
        ['Fecha Inicio de Cultivo:', simulacion.fecha_inicio_cultivo.strftime('%d/%m/%Y')],
        ['Días de Cultivo:', f"{simulacion.dias_cultivo} días"],
        ['Porcentaje de Pérdida:', f"{simulacion.tipo_alga.porcentaje_perdida}%"],
    ]
    tabla_resultados = Table(datos_resultados, colWidths=[3*inch, 3*inch])
    tabla_resultados.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#e8f5e9')),
        ('TEXTCOLOR', (0, 0), (-1, -1), colors.black),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (0, -1), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, -1), 11),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 12),
        ('GRID', (0, 0), (-1, -1), 1, colors.grey)
    ]))
    elementos.append(tabla_resultados)
    elementos.append(Spacer(1, 0.3*inch))
    
    # Notas
    if simulacion.notas:
        elementos.append(Paragraph('Notas Adicionales', estilo_subtitulo))
        elementos.append(Paragraph(simulacion.notas, estilo_normal))
        elementos.append(Spacer(1, 0.3*inch))
    
    # Explicación de cálculos
    elementos.append(Paragraph('Explicación de Cálculos', estilo_subtitulo))
    explicacion = f"""
    <b>Cálculo de Toneladas a Plantar:</b><br/>
    Para compensar las pérdidas del {simulacion.tipo_alga.porcentaje_perdida}% durante el cultivo,
    se debe plantar {simulacion.toneladas_a_plantar} toneladas para obtener {simulacion.toneladas_deseadas} toneladas finales.<br/><br/>
    <b>Fórmula:</b> Toneladas a Plantar = Toneladas Deseadas × (1 + Porcentaje Pérdida / 100)<br/><br/>
    <b>Cálculo de Fecha de Inicio:</b><br/>
    Considerando que el cultivo de {simulacion.tipo_alga.nombre} requiere {simulacion.dias_cultivo} días,
    se debe iniciar el cultivo el {simulacion.fecha_inicio_cultivo.strftime('%d/%m/%Y')} para cumplir con la fecha objetivo.
    """
    elementos.append(Paragraph(explicacion, estilo_normal))
    
    # Construir el PDF
    doc.build(elementos)
    
    # Obtener el PDF del buffer
    pdf = buffer.getvalue()
    buffer.close()
    
    # Crear la respuesta HTTP
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="simulacion_{simulacion.id}.pdf"'
    response.write(pdf)
    
    return response
