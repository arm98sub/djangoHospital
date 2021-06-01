from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic import TemplateView, DeleteView
from django.views.generic.edit import FormMixin
from .models import Articulo, Venta, DetalleVenta
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from .forms import QuantityForm
from django.db.models import When

class Lista(LoginRequiredMixin, ListView):
    template_name = 'articuo_list.html'
    model = Articulo
    form_class = QuantityForm
    paginate_by = 5





def eliminarArt(request, pk):
    primarykey = int(pk)
    obj = get_object_or_404(Articulo, id=primarykey)
    obj.delete()
    return redirect('articulos:lista')



def comprar(request, pk):
    articulo = get_object_or_404(Articulo, pk=pk)
    if articulo.stock > 0: 
        cantidad_articulos = int(request.POST.get('cantidad_articulos'))
        
        if cantidad_articulos <= articulo.stock and cantidad_articulos > -1:
            articulo.stock = articulo.stock - cantidad_articulos
            articulo.save()
            id = str(pk)
            request.session['total'] = request.session['total'] + (float(articulo.precio)*cantidad_articulos)
            request.session['cuantos'] = request.session['cuantos'] + cantidad_articulos
            if id in request.session['articulos']:
                request.session['articulos'][id]['cantidad'] = request.session['articulos'][id]['cantidad'] + cantidad_articulos
            else:
                request.session['articulos'][id] = {'precio':float(articulo.precio),'cantidad':cantidad_articulos}
        
    return redirect('articulos:lista')


class Carrito(LoginRequiredMixin, ListView):
    model = Articulo
    extra_context = {'carrito':True}

    def get_queryset(self):
        ids = list(self.request.session['articulos'])
        all_articles = Articulo.objects.filter(id__in = ids)
        return all_articles



def cancelarCompra(request):
    keys = list(request.session['articulos'].keys())
    for pk in keys:
        articulo_temp = get_object_or_404(Articulo, pk=pk)
        id = str(pk)
        articulo_temp.stock += request.session['articulos'][id]['cantidad']
        articulo_temp.save()
    request.session['cuantos'] = 0
    request.session['total'] = 0.0
    request.session['articulos'] = {}
    return redirect('articulos:lista')

def confirmarCompra(request):
    cantidad = request.session['cuantos']
    total = request.session['total']
    detalle_venta = DetalleVenta(cantidad=cantidad, total=total)
    detalle_venta.save()
    venta = Venta(detalle_venta=detalle_venta)
    venta.save()
    request.session['cuantos'] = 0
    request.session['total'] = 0.0
    request.session['articulos'] = {}
    return redirect('articulos:lista')
