from django.contrib import admin
from .models import Articulo, Categoria, Venta, DetalleVenta


admin.site.register(Articulo)
admin.site.register(Categoria)
admin.site.register(Venta)
admin.site.register(DetalleVenta)