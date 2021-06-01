from django.urls import path
from .views import Login, Nuevo, Perfil, ActivarCuenta, ListaUsuario, AgregarAdministradores, AgregarUsuarios, EliminarDeAdministradores, EliminarDeUsuarios
from django.contrib.auth.views import LogoutView


app_name = 'usuarios'

urlpatterns = [
    path('login/', Login.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('nuevo/', Nuevo.as_view(), name='nuevo'),
    path('perfil/', Perfil.as_view(), name='perfil'),
    
    path('usuarios_list/', ListaUsuario.as_view(), name='lista'),
    
    path('agregarAdmin/<int:id>', AgregarAdministradores.as_view(), name='agregarAdmin'),
    path('EliminarDeAdmin/<int:id>', EliminarDeAdministradores.as_view(), name='EliminarDeAdmin'),

    path('agregarUsuario/<int:id>', AgregarUsuarios.as_view(), name='agregarUsuario'),
    path('EliminarDeUsuarios/<int:id>', EliminarDeUsuarios.as_view(), name='EliminarDeUsuarios'),

    path('activar/<slug:uidb64>/<slug:token>', ActivarCuenta.as_view(), name= 'activar'),

]
