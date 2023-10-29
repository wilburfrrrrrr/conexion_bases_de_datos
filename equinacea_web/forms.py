from typing import Any
from django import forms
from equinacea_web import models
from datetime import datetime
from django.utils import timezone
from django.contrib.auth.forms import AuthenticationForm
from django.core.validators import validate_email
# forms.ModelForm

class login_form(forms.Form):
	mail = forms.CharField(label='Correo', max_length=45, widget=forms.TextInput(attrs={'class': 'form-control'}), validators = [validate_email])
	password = forms.CharField(label='Contraseña', max_length=45, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	# class Meta:
	# 	model = models.Usuarios
	# 	fields = ['mail', 'password']

class registro_usuarios(forms.ModelForm):
	ID_usuario = forms.IntegerField(label='ID', widget=forms.TextInput(attrs={'class': 'form-control'}))
	nombre = forms.CharField(label='Nombre', max_length=45, widget=forms.TextInput(attrs={'class': 'form-control'}))
	apellido = forms.CharField(label='Apellido', max_length=45, widget=forms.TextInput(attrs={'class': 'form-control'}))
	mail = forms.CharField(label='Correo', max_length=45, widget=forms.TextInput(attrs={'class': 'form-control'}), validators = [validate_email])
	telefono = forms.CharField(label='Telefono', max_length=45, widget=forms.TextInput(attrs={'class': 'form-control'}))
	password = forms.CharField(label='Contraseña', max_length=45, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	confirma_password = forms.CharField(label='Confirmar contraseña', max_length=45, widget=forms.PasswordInput(attrs={'class': 'form-control'}))
	
	class Meta:
		model = models.Usuarios
		fields = ['ID_usuario', 'nombre', 'apellido', 'mail', 'telefono', 'password']

	def clean(self):
		cleaned_data = super(registro_usuarios, self).clean()
		password = cleaned_data.get("password")
		confirma_password = cleaned_data.get("confirma_password")
		if password != confirma_password:
			raise forms.ValidationError(
				"Las contraseñas no coinciden"
			)
	
	def clean_password(self):
		password = self.cleaned_data.get("password")
		if len(password) < 8:
			raise forms.ValidationError("La contraseña debe tener al menos 8 caracteres")
		return password

	def clean_telefono(self):
		telefono = self.cleaned_data.get("telefono")
		if len(telefono) != 10:
			raise forms.ValidationError("El número de teléfono debe tener 10 caracteres")
		return telefono
	
	def clean_ID_usuario(self):
		ID_usuario = self.cleaned_data.get("ID_usuario")
		if int(ID_usuario) > 2147483647 or int(ID_usuario) < 0:
			raise forms.ValidationError("El número de identificación no es válido")
		return ID_usuario


class registro_doctores(registro_usuarios):
	especialidad = forms.ModelChoiceField(queryset=models.Especialidades.objects.all(), empty_label="Seleccione una especialidad")

	
class registro_citas(forms.ModelForm):
	def __init__(self, especialidad, *args, **kwargs):
		super(registro_citas, self).__init__(*args, **kwargs)
		self.fields['doctor'].queryset = models.Doctores.objects.filter(especialidad=especialidad, disponibilidad=True)

	doctor = forms.ModelChoiceField(queryset=models.Doctores.objects.all(), empty_label="Seleccione un doctor")
	fecha = forms.DateField(label='Fecha', widget=forms.SelectDateWidget())
	
	def clean_fecha(self):
		fecha = self.cleaned_data.get("fecha")	
		if fecha < timezone.now().date():
			raise forms.ValidationError("Fecha inválida")
		return fecha
	
	class Meta:
		model = models.Citas
		fields = ['doctor', 'fecha']

class registro_turnos(forms.ModelForm):
	tipo = forms.ModelChoiceField(queryset=models.TipoCita.objects.all(), empty_label="Seleccione un tipo")
	especialidad = forms.ModelChoiceField(queryset=models.Especialidades.objects.all(), empty_label="Seleccione una especialidad")
	class Meta:
		model = models.Turnos
		fields = ['tipo', 'especialidad']
		

class actualizar_historial(forms.ModelForm):
	situacion = forms.CharField(label='Situación', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
	observaciones = forms.CharField(label='Observaciones', max_length=200, widget=forms.TextInput(attrs={'class': 'form-control'}))
	class Meta:	
		model = models.Historial
		fields = ['situacion', 'observaciones']



# from django import forms
# from .models import YourModel  # Import your model


