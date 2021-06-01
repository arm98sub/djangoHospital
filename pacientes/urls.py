from django.urls import path
from .views import Lista, Nuevo, Eliminar, Editar, buscar_municipio, Grafica, ListaPacientePdf, filtrar

app_name = 'pacientes'

urlpatterns = [
    path('lista/', Lista.as_view(), name='lista'),
    
    path('grafica/', Grafica.as_view(), name='pacientes_grafica'),
    path('pdf/',ListaPacientePdf.as_view(), name='pdf'),

    path('nuevo/', Nuevo.as_view(), name='nuevo'),
    path('editar/<int:pk>', Editar.as_view(), name='editar'),
    path('eliminar/<int:pk>', Eliminar.as_view(), name='eliminar'),
    path('busca-municipio/', buscar_municipio, name='buscar_municipio'),

    path('filtrar/<int:pk>', filtrar, name='filtrar'),

]
