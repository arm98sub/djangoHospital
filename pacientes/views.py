from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic import TemplateView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Paciente, Municipio, Estado
from .forms import PacienteForm
from django.urls import reverse_lazy
from django.http import JsonResponse
from django.db.models import Count
from django_weasyprint import WeasyTemplateResponseMixin
from django.conf import settings
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, AccessMixin





class Lista(PermissionRequiredMixin, ListView):
    #En este lugar se puede paginar dependiendo de cuantos datos se requieren de la lista y en base a ese numero filtrar.
    #Ejemplo si queremos que apartir de 10 registro cree otra pagina en el atributo paginate_by ponemos 10.
    paginate_by = 10
    model = Paciente
    permission_required = 'usuarios.permiso_administradores'


def filtrar (request, pk):
    
    datos = Paciente.objects.filter(tipo_sangre = 'A+')

    print(str(datos))


    pass
    





class Nuevo(PermissionRequiredMixin, CreateView):
    model = Paciente
    form_class = PacienteForm
    success_url = reverse_lazy('pacientes:lista')
    permission_required = 'usuarios.permiso_administradores'

class Editar(PermissionRequiredMixin ,UpdateView):
    model = Paciente
    form_class = PacienteForm
    extra_context = {'editar':True}
    permission_required = 'usuarios.permiso_administradores'
    success_url = reverse_lazy('pacientes:lista')

class Eliminar(PermissionRequiredMixin, DeleteView):
    model = Paciente
    success_url = reverse_lazy('pacientes:lista')
    permission_required = 'usuarios.permiso_administradores'
    


def buscar_municipio(request):
    id_estado = request.POST.get('id',None)
    if id_estado:
        municipios = Municipio.objects.filter(estado_id=id_estado)
        data = [{'id':mun.id,'nombre':mun.nombre} for mun in  municipios]
        return JsonResponse(data, safe=False)
    return JsonResponse({'error':'Parámetro inválido'}, safe=False)


class Grafica(TemplateView):
    template_name = 'pacientes/grafica.html'
    def get(self, request, *args, **kwargs):
        paci_municipio = Paciente.objects.all().values('municipio').annotate(cuantos=Count('municipio'))
        municipios = Municipio.objects.all()
        datos = []
        for municipio in municipios:
            cuantos = 0
            for pm in paci_municipio:
                if pm['municipio'] == municipio.id:
                    cuantos = pm['cuantos']
                    break  
            datos.append({'name':municipio.nombre, 'data':[cuantos]})
        self.extra_context = {'datos':datos}
        context = self.get_context_data(**kwargs)
        return self.render_to_response(context)


class VistaPdf(ListView):
    model = Paciente
    template_name = 'pacientes/pacientes_pdf.html'

class ListaPacientePdf(WeasyTemplateResponseMixin, VistaPdf):
    passpdf_stylesheets = [
        settings.STATICFILES_DIRS[0] + 'css/boostrap.min.css',
    ]
    pdf_attachment = False
    pdf_filename = 'paciente.pdf'
    