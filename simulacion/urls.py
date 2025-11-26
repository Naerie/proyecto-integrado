from django.urls import path
from . import views

urlpatterns = [
    # Página de inicio
    path('', views.inicio, name='inicio'),
    
    # Simulaciones
    path('simulaciones/', views.lista_simulaciones, name='lista_simulaciones'),
    path('simulaciones/nueva/', views.nueva_simulacion, name='nueva_simulacion'),
    path('simulaciones/<int:pk>/', views.detalle_simulacion, name='detalle_simulacion'),
    path('simulaciones/<int:pk>/eliminar/', views.eliminar_simulacion, name='eliminar_simulacion'),
    path('simulaciones/<int:pk>/pdf/', views.exportar_pdf, name='exportar_pdf'),
]
