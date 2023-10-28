from django.http import HttpResponseForbidden
from django.shortcuts import redirect
from .models import Usuarios, Administradores, Pacientes, Doctores, Cajeros


# def usuario_required(function):
# 	def wrap(request, *args, **kwargs):
# 		try:
# 			usuario = Usuarios.objects.get(mail=request.session['mail'])
# 			return function(request, *args, **kwargs)
# 		except:
# 			return HttpResponseForbidden("Prohibido: No has iniciado sesion")
# 	return wrap

def admin_required(function):
	def wrap(request, *args, **kwargs):
		try:
			usuario = Usuarios.objects.get(ID_usuario=request.session['user_id'])
			admin = Administradores.objects.get(ID_administrador=usuario.ID_usuario)
			return function(request, *args, **kwargs)
		except Exception as e:
			print(f"{request.session.get('user_id')}")
			print(e)
			return redirect('inicio')
	return wrap

def doctor_required(function):
	def wrap(request, *args, **kwargs):
		try:
			usuario = Usuarios.objects.get(ID_usuario=request.session['user_id'])
			doctor = Doctores.objects.get(ID_doctor=usuario.ID_usuario)
			return function(request, *args, **kwargs)
		except Exception as e:
			print(f"{request.session.get('user_id')}")
			print(e)
			return redirect('inicio')
	return wrap

def cajero_required(function):
	def wrap(request, *args, **kwargs):
		try:
			usuario = Usuarios.objects.get(ID_usuario=request.session['user_id'])
			cajero = Cajeros.objects.get(ID_cajero=usuario.ID_usuario)
			return function(request, *args, **kwargs)
		except Exception as e:
			print(f"{request.session.get('user_id')}")
			print(e)
			return redirect('inicio')
	return wrap

def paciente_required(function):
	def wrap(request, *args, **kwargs):
		try:
			usuario = Usuarios.objects.get(ID_usuario=request.session['user_id'])
			paciente = Pacientes.objects.get(ID_paciente=usuario.ID_usuario)
			return function(request, *args, **kwargs)
		except Exception as e:
			print(f"{request.session.get('user_id')}")
			print(e)
			return redirect('inicio')
	return wrap