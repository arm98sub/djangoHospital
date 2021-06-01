from django.shortcuts import render, redirect
from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.forms import AuthenticationForm
from .forms import UsuarioForm, PerfilForm
from .models import Usuario
from django.urls import reverse_lazy
from django.contrib.messages.views import SuccessMessageMixin
from django.core.mail import EmailMessage
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text
from .token import token_activacion
from django.views.generic import TemplateView
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission, Group
from django.contrib import messages
from django.views.generic.list import ListView
from django.contrib.auth.mixins import PermissionRequiredMixin, LoginRequiredMixin, AccessMixin

class ListaUsuario(ListView):
	template_name = 'usuario_list.html'
	model = Usuario
	paginate_by = 10




class Login(LoginView):
	template_name = 'login.html'
	form_class = AuthenticationForm


	def get_success_url(self):

		self.request.session['cuantos'] = 0
		self.request.session['total'] = 0.0
		self.request.session['articulos'] = {}

		return super().get_success_url()



class Nuevo(CreateView):
	template_name = 'nuevo.html'
	model = Usuario
	form_class = UsuarioForm
	
    #success_url = reverse_lazy('usuarios:login')

	def form_valid(self, form):

		user = form.save(commit=False)
		user.is_active = False
		user.save()

		dominio = get_current_site(self.request)
		mensaje = render_to_string('confirmar_cuenta.html',
			{
			'user':user,
			'dominio':dominio,
			'uid': urlsafe_base64_encode(force_bytes(user.id)),
			'token': token_activacion.make_token(user)
			}
		)
		email = EmailMessage(
			'Activar cuenta',
			mensaje,
			to=[user.email]
		)
		email.content_subtype = "html"
		email.send()
		mensaje = 'Hemos enviado un enlace de activacion a tu correo electronico'
		return render(self.request, 'login.html',{'mensaje':mensaje})





class Perfil(SuccessMessageMixin, UpdateView):
	template_name = 'perfil.html'
	model = Usuario
	form_class = PerfilForm
	success_url = reverse_lazy('usuarios:perfil')
	success_message = "El usuario %(first_name)s se actualizó con éxito"

	def get_object(self, queryset=None):
		pk = self.request.user.pk
		obj = Usuario.objects.get(pk=pk)
		return obj

	# def get_success_url(self):
	# 	pk = self.kwargs.get(self.pk_url_kwarg)
	# 	url = reverse_lazy('usuarios:perfil', kwargs={'pk': pk})
	# 	return url




class ActivarCuenta(TemplateView):
	
	def get(self, request, *args, **kwargs):
        
        #context = self.get_context_data(**kwargs)

		try:
			uid = urlsafe_base64_decode(force_text(kwargs['uidb64']))
			token = kwargs['token']
			user = Usuario.objects.get(pk=uid)
		except(TypeError, ValueError, Usuario.DoesNotExist):
			user = None

		if user is not None and token_activacion.check_token(user, token):
			user.is_active = True
			user.save()
			messages.success(self.request, 'Cuenta activada, ingresa tus datos de login')
		else:
			messages.error(self.request, 'Token invalido, contacta con el administrador')
			

		return redirect('usuarios:login')



class AgregarAdministradores(TemplateView):

	def get(self, request, *args, **kwargs):

		id = kwargs['id']
		usuario = Usuario.objects.get(pk=id)
		grupos = usuario.groups.all()

		if grupos.filter(name = 'administrador').exists():

			messages.error(self.request, 'El usuario ya existe en el grupo de administradores.')

		else:

			messages.success(self.request, 'El usuario se actualizó con éxito ahora es administrador.')
			usuario.groups.add(Group.objects.get(pk=1))
			
		return redirect('usuarios:lista')


class AgregarUsuarios(TemplateView):

	def get(self, request, *args, **kwargs):

		id = kwargs['id']
		usuario = Usuario.objects.get(pk=id)
		grupos = usuario.groups.all()

		if grupos.filter(name = 'usuarios').exists():
			
			messages.error(self.request, 'El usuario ya existe en el grupo de usuarios.')

		else:

			messages.success(self.request, 'El usuario se actualizó con éxito ahora es un usuario.')
			usuario.groups.add(Group.objects.get(pk=2))
			
		return redirect('usuarios:lista')



class EliminarDeAdministradores(TemplateView):

	def get(self, request, *args, **kwargs):

		id = kwargs['id']
		usuario = Usuario.objects.get(pk=id)
		grupos = usuario.groups.all()

		if grupos.filter(name = 'administrador').exists():
			
			if len(grupos) == 1:
				messages.error(self.request, 'El usuario no puede ser eliminado del grupo ya que solo cuenta con un grupo.')

			else:

				usuario.groups.remove(Group.objects.get(pk=1))	
				messages.success(self.request, 'El usuario ya no es parte de los administradores.')
				

		else:

			messages.error(self.request, 'El usuario no es administrador.')
			
		return redirect('usuarios:lista')



class EliminarDeUsuarios(TemplateView):

	def get(self, request, *args, **kwargs):

		id = kwargs['id']
		usuario = Usuario.objects.get(pk=id)
		grupos = usuario.groups.all()

		if grupos.filter(name = 'usuarios').exists():

			if len(grupos) == 1:
				messages.error(self.request, 'El usuario no puede ser eliminado del grupo ya que solo cuenta con un grupo.')
			else:
				usuario.groups.remove(Group.objects.get(pk=2))	
				messages.success(self.request, 'El usuario ya no es parte de los usuarios.')
			
		else:

			messages.error(self.request, 'El usuario no froma parte del grupo usuarios.')
			
		return redirect('usuarios:lista')
