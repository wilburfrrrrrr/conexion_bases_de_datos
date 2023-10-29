from django.shortcuts import  render, redirect
from django.utils import timezone
from datetime import timedelta 
from equinacea_web import models, forms, decorators, auth, utils



def paneles(request, usuario):
	id = request.session.get('user_id')
	if models.Doctores.objects.filter(ID_doctor = id).exists():
		return redirect('doctores')
	if models.Cajeros.objects.filter(ID_cajero = id).exists():
		return redirect('cajeros')
	if models.Pacientes.objects.filter(ID_paciente = id).exists():
		return redirect('pacientes')
	else:
		return redirect('admin')

def inicio(request):
	return render(request, 'inicio.html')

def login_usuario(request):
	if request.method == 'POST':
		form = forms.login_form(request.POST)
		if form.is_valid():
			try:
				email = form.cleaned_data['mail']
				password = form.cleaned_data['password']
				usuario = auth.autenticar(request, mail=email, password=password)
				if usuario is not None:
					utils.iniciar_sesion(request, usuario)
					print(f"{request.session.get('user_id')}")
					return paneles(request, usuario)
			except Exception as e:
				print(e)
				form.add_error('mail', 'El usuario no existe o la contraseña es incorrecta')
	else:
		form = forms.login_form()
	return render(request, 'login.html', {'form': form})

def logout_usuario(request):
	if 'user_id' in request.session:
		del request.session['user_id']
	return redirect('inicio')

@decorators.cajero_required
def cajeros(request):
	id_sesion = request.session.get('user_id')
	cajero = models.Usuarios.objects.get(ID_usuario = id_sesion)
	turnos = models.Turnos.objects.values(
		'ID_turno',
		'paciente',
		'paciente__ID_paciente__nombre',
		'paciente__ID_paciente__apellido',
		'tipo__tipo',
		'especialidad__especialidad',
		'estado',
		'fecha_reserva',
		'fecha_turnos'
	).filter(estado = 'PENDIENTE')

	contexto = {
		'cajero': cajero,
		'turnos': turnos
	}
	return render(request, 'cajeros.html', contexto)

@decorators.doctor_required
def doctores(request):
	user_id = request.session.get('user_id')
	doctor_actual = models.Usuarios.objects.get(ID_usuario = user_id)
	doctor_id = doctor_actual.ID_usuario
	doctor = models.Usuarios.objects.get(ID_usuario = doctor_id)

	citas = models.Citas.objects.filter(doctor = doctor_id).values(
		'ID_cita',
		'paciente',
		'paciente__ID_paciente__nombre',
		'paciente__ID_paciente__apellido',
		'tipo__tipo',
		'fecha'
	)

	contexto = {
		'doctor': doctor,
		'citas': citas,
	}
	return render(request, 'doctores.html', contexto)

@decorators.paciente_required
def pacientes(request):
	user_id = request.session.get('user_id')
	paciente = models.Usuarios.objects.get(ID_usuario = user_id)
	paciente_id = paciente.ID_usuario
	paciente = models.Usuarios.objects.get(ID_usuario = paciente_id)
	
	historial = models.Historial.objects.filter(paciente = paciente.ID_usuario).values(
		'paciente__ID_paciente__nombre',
		'paciente__ID_paciente__apellido',
		'situacion',
		'observaciones',
		'fecha_modificacion'
	)
	citas = models.Citas.objects.filter(paciente = paciente_id).values(
		'ID_cita',
		'doctor',
		'doctor__ID_doctor__nombre',
		'doctor__ID_doctor__apellido',
		'tipo__tipo',
		'fecha'
	)

	contexto = {
		'paciente': paciente,
		'historial': historial,
		'citas': citas,
	}
	return render(request, 'pacientes.html', contexto)

@decorators.doctor_required
def cita(request, id_cita):
	cita = models.Citas.objects.get(ID_cita = id_cita)
	id_paciente = cita.paciente.ID_paciente.ID_usuario
	id_doctor = cita.doctor.ID_doctor.ID_usuario

	paciente = models.Usuarios.objects.get(ID_usuario = id_paciente)
	doctor = models.Usuarios.objects.get(ID_usuario = id_doctor)
	historial = models.Historial.objects.get(paciente = id_paciente)
	
	if request.method == 'POST':
		historial_form = forms.actualizar_historial(request.POST)
		if historial_form.is_valid():
			historial.situacion = historial_form.cleaned_data['situacion']
			historial.observaciones = historial_form.cleaned_data['observaciones']
			historial.fecha_modificacion = timezone.now()
			historial.save()
			turno_eliminado = models.CitasEliminados(
				ID_cita = cita.ID_cita,
				ID_paciente = paciente.ID_usuario,
				nombre_paciente = paciente.nombre,
				apellido_paciente = paciente.apellido,
				ID_doctor = doctor.ID_usuario,
				nombre_doctor = doctor.nombre,
				apellido_doctor = doctor.apellido,
				tipo = cita.tipo.tipo,
				fecha = cita.fecha,
				fecha_eliminado = timezone.now()
			)
			turno_eliminado.save()
			cita.delete()
			return redirect('doctores')
	else:
		historial_form = forms.actualizar_historial()
	contexto = {
		'cita': cita,
		'paciente': paciente,
		'doctor': doctor,
		'historial': historial,
		'historial_form': historial_form
	}
	return render(request, 'cita.html', contexto)

@decorators.admin_required
def admin(request):
	user_id = request.session.get('user_id')
	admin = models.Usuarios.objects.get(ID_usuario = user_id)
	admin_id = admin.ID_usuario
	admin = models.Usuarios.objects.get(ID_usuario = admin_id)
	return render (request, 'admin.html', {'admin': admin})

@decorators.admin_required
def admin_cajeros(request):
	cajeros = models.Usuarios.objects.filter(ID_usuario__in = models.Cajeros.objects.values('ID_cajero')).values(
		'ID_usuario', 
		'nombre', 
		'apellido', 
		'mail', 
		'telefono')
	return render(request, 'admin_cajeros.html', {'cajeros': cajeros})

@decorators.admin_required
def admin_doctores(request):
	doctores = models.Usuarios.objects.values(
		'ID_usuario', 
		'nombre', 
		'apellido', 
		'mail', 
		'telefono', 
		'doctores__especialidad__especialidad').filter(doctores__isnull = False)
	return render(request, 'admin_doctores.html', {'doctores': doctores})

@decorators.admin_required
def admin_pacientes(request):
	pacientes = models.Usuarios.objects.values(
		'ID_usuario',
		'nombre',
		'apellido',
		'mail',
		'telefono',
		'pacientes__historial__situacion',
		'pacientes__historial__observaciones',
		'pacientes__historial__fecha_modificacion'
		).filter(pacientes__historial__isnull = False)
	return render(request, 'admin_pacientes.html', {'pacientes': pacientes})

@decorators.admin_required
def registro_admin(request):
	if request.method == 'POST':
		register_form = forms.registro_usuarios(request.POST)
		if register_form.is_valid():
			password = register_form.cleaned_data['password']
			hashed_password = utils.hash_password(password)
			nuevo_usuario = models.Usuarios(
				ID_usuario = register_form.cleaned_data['ID_usuario'],
				nombre = register_form.cleaned_data['nombre'],
				apellido = register_form.cleaned_data['apellido'],
				mail = register_form.cleaned_data['mail'],
				telefono = register_form.cleaned_data['telefono'],
				password = hashed_password
			)
			nuevo_usuario.save()
			nuevo_admin = models.Administradores(ID_administrador = nuevo_usuario)
			nuevo_admin.save()
			return redirect('admin')
	else:
		register_form = forms.registro_usuarios()
	return render(request, 'registro_admin.html', {'register_form': register_form})

@decorators.admin_required
def registro_cajeros(request):
	if request.method == 'POST':
		register_form = forms.registro_usuarios(request.POST)
		if register_form.is_valid():
			password = register_form.cleaned_data['password']
			hashed_password = utils.hash_password(password)
			nuevo_usuario = models.Usuarios(
				ID_usuario = register_form.cleaned_data['ID_usuario'],
				nombre = register_form.cleaned_data['nombre'],
				apellido = register_form.cleaned_data['apellido'],
				mail = register_form.cleaned_data['mail'],
				telefono = register_form.cleaned_data['telefono'],
				password = hashed_password
			)
			nuevo_usuario.save()
			nuevo_cajero = models.Cajeros(ID_cajero = nuevo_usuario)
			nuevo_cajero.save()
			return redirect('admin')
	else:
		register_form = forms.registro_usuarios()
	return render(request, 'registro_cajeros.html', {'register_form': register_form})


@decorators.admin_required
def registro_doctores(request):
	if request.method == 'POST':
		register_form = forms.registro_doctores(request.POST)
		if register_form.is_valid():
			password = register_form.cleaned_data['password']
			hashed_password = utils.hash_password(password)
			nuevo_usuario = models.Usuarios(
				ID_usuario = register_form.cleaned_data['ID_usuario'],
				nombre = register_form.cleaned_data['nombre'],
				apellido = register_form.cleaned_data['apellido'],
				mail = register_form.cleaned_data['mail'],
				telefono = register_form.cleaned_data['telefono'],
				password = hashed_password
			)
			nuevo_usuario.save()
			nuevo_doctor = models.Doctores(
				ID_doctor = nuevo_usuario,
				especialidad = register_form.cleaned_data['especialidad']
			)
			nuevo_doctor.save()
			return redirect('admin')
	else:
		register_form = forms.registro_doctores()
	return render(request, 'registro_doctores.html', {'register_form': register_form})

def registro_pacientes(request):
	if request.method == 'POST':
		register_form = forms.registro_usuarios(request.POST)
		if register_form.is_valid():
			password = register_form.cleaned_data['password']
			hashed_password = utils.hash_password(password)
			nuevo_usuario = models.Usuarios(
				ID_usuario = register_form.cleaned_data['ID_usuario'],
				nombre = register_form.cleaned_data['nombre'],
				apellido = register_form.cleaned_data['apellido'],
				mail = register_form.cleaned_data['mail'],
				telefono = register_form.cleaned_data['telefono'],
				password = hashed_password
			)
			nuevo_usuario.save()
			nuevo_paciente = models.Pacientes(ID_paciente = nuevo_usuario)
			historial_paciente = models.Historial(paciente = nuevo_paciente)
			nuevo_paciente.save()
			historial_paciente.save()
			utils.iniciar_sesion(request, nuevo_usuario)
			return redirect('pacientes')
	else:
		register_form = forms.registro_usuarios()
	return render(request, 'registro_pacientes.html', {'register_form': register_form})

@decorators.cajero_required
def registro_citas(request, id_turno):
	turno = models.Turnos.objects.get(ID_turno = id_turno)
	paciente = models.Pacientes.objects.get(ID_paciente = turno.paciente)
	if request.method == 'POST':
		register_form = forms.registro_citas(data = request.POST, especialidad = turno.especialidad)
		print(f"post")
		if register_form.is_valid():
			print(f"valido")
			nueva_cita = models.Citas(
				paciente = paciente,
				doctor = register_form.cleaned_data['doctor'],
				tipo = turno.tipo,
				fecha = register_form.cleaned_data['fecha']
			)
			nueva_cita.save()
			print(f"cita_guardada")
			turno.estado = 'RESERVADO'
			turno.save()
			print(f"turno actualizado")
			return redirect('cajeros')
	else:
		register_form = forms.registro_citas(especialidad = turno.especialidad)
	return render(request, 'registro_citas.html', {'register_form': register_form})

@decorators.paciente_required
def registro_turnos(request):
	paciente_id = request.session.get('user_id')
	if request.method == 'POST':
		register_form = forms.registro_turnos(request.POST)
		if register_form.is_valid():
			nuevo_turno = models.Turnos(
				paciente = models.Pacientes.objects.get(ID_paciente = paciente_id),
				tipo = register_form.cleaned_data['tipo'],
				especialidad = register_form.cleaned_data['especialidad'],
				estado = 'PENDIENTE',
				fecha_reserva = timezone.now(),
				fecha_turnos = timezone.now() + timedelta(days = 7)
			)
			nuevo_turno.save()
			return redirect('pacientes')
	else:
		register_form = forms.registro_turnos()
	return render(request, 'registro_turnos.html', {'register_form': register_form})

@decorators.admin_required
def cajeros_archivados(request):
	cajeros_eliminados = models.CajerosEliminados.objects.all()
	return render(request, 'cajeros_archivados.html', {'cajeros_eliminados': cajeros_eliminados})

@decorators.admin_required
def doctores_archivados(request):
	doctores_eliminados = models.DoctoresEliminados.objects.all()
	return render(request, 'doctores_archivados.html', {'doctores_eliminados': doctores_eliminados})

@decorators.admin_required
def pacientes_archivados(request):
	pacientes_eliminados = models.PacientesEliminados.objects.all()
	return render(request, 'pacientes_archivados.html', {'pacientes_eliminados': pacientes_eliminados})

@decorators.admin_required
def citas_archivadas(request):
	citas_eliminadas = models.CitasEliminados.objects.all()
	return render(request, 'citas_archivadas.html', {'citas_eliminadas': citas_eliminadas})

@decorators.admin_required
def turnos_archivados(request):
	turnos_eliminados = models.TurnosEliminados.objects.all()
	return render(request, 'turnos_archivados.html', {'turnos_eliminados': turnos_eliminados})	

@decorators.admin_required
def eliminar_usuario(request, id_usuario):
	usuario = models.Usuarios.objects.get(ID_usuario = id_usuario)
	usuario_archivado = models.UsuariosEliminados(
		ID_usuario = usuario.ID_usuario,
		nombre = usuario.nombre,
		apellido = usuario.apellido,
		mail = usuario.mail,
		telefono = usuario.telefono,
		password = usuario.password,
		fecha_eliminado = timezone.now()
		)
	usuario_archivado.save()
	usuario.delete()

@decorators.admin_required
def archivar_cajero(request, id_cajero):
	cajero = models.Usuarios.objects.get(ID_usuario = id_cajero)
	cajero_archivado = models.CajerosEliminados(
		ID_usuario = cajero.ID_usuario,
		nombre = cajero.nombre,
		apellido = cajero.apellido,
		mail = cajero.mail,
		telefono = cajero.telefono,
		fecha_eliminado = timezone.now()
		)
	cajero_archivado.save()
	eliminar_usuario(request, id_cajero)
	return redirect('admin_cajeros')

@decorators.admin_required
def archivar_doctor(request, id_doctor):
	doctor = models.Usuarios.objects.get(ID_usuario = id_doctor)
	doctor_archivado = models.DoctoresEliminados(
		ID_usuario = doctor.ID_usuario,
		nombre = doctor.nombre,
		apellido = doctor.apellido,
		mail = doctor.mail,
		telefono = doctor.telefono,
		especialidad = doctor.doctores.especialidad.especialidad,
		fecha_eliminado = timezone.now()
		)
	doctor_archivado.save()
	eliminar_usuario(request, id_doctor)
	return redirect('admin_doctores')

@decorators.admin_required
def archivar_paciente(request, id_paciente):
	paciente = models.Usuarios.objects.get(ID_usuario = id_paciente)
	paciente_archivado = models.PacientesEliminados(
		ID_paciente = paciente.ID_usuario,
		nombre = paciente.nombre,
		apellido = paciente.apellido,
		mail = paciente.mail,
		telefono = paciente.telefono,
		situacion = paciente.pacientes.historial.situacion,
		observaciones = paciente.pacientes.historial.observaciones,
		fecha_modificacion = paciente.pacientes.historial.fecha_modificacion,
		fecha_eliminado = timezone.now()
		)
	paciente_archivado.save()
	eliminar_usuario(request, id_paciente)
	return redirect('admin')

@decorators.admin_required
def archivar_cita(request, id_cita):
	cita = models.Citas.objects.get(ID_cita = id_cita)
	cita_archivada = models.CitasEliminados(
		ID_cita = cita.ID_cita,
		ID_paciente = cita.paciente.ID_paciente.ID_usuario,
		nombre_paciente = cita.paciente.ID_paciente.nombre,
		apellido_paciente = cita.paciente.ID_paciente.apellido,
		ID_doctor = cita.doctor.ID_doctor.ID_usuario,
		nombre_doctor = cita.doctor.ID_doctor.nombre,
		apellido_doctor = cita.doctor.ID_doctor.apellido,
		tipo = cita.tipo.tipo,
		fecha = cita.fecha,
		fecha_eliminado = timezone.now()
		)
	cita_archivada.save()
	cita.delete()
	return redirect('doctores')

@decorators.cajero_required
def archivar_turno(request, id_turno):
	turno = models.Turnos.objects.get(ID_turno = id_turno)
	print(f"turno: {turno.ID_turno}")
	turno_archivado = models.TurnosEliminados(
		ID_turno = turno.ID_turno,
		ID_usuario = turno.paciente.ID_paciente.ID_usuario,
		nombre = turno.paciente.ID_paciente.nombre,
		apellido = turno.paciente.ID_paciente.apellido,
		tipo = turno.tipo.tipo,
		especialidad = turno.especialidad.especialidad,
		estado = turno.estado,
		fecha_reserva = turno.fecha_reserva,
		fecha_turnos = turno.fecha_turnos,
		fecha_eliminado = timezone.now()
		)
	turno_archivado.save()
	print(f"turno eliminado")
	turno.delete()
	return redirect('cajeros')

@decorators.admin_required
def actualizar_disponibilidad(request, id_doctor):
	doctor = models.Doctores.objects.get(ID_doctor = id_doctor)
	if doctor.disponibilidad:
		doctor.disponibilidad = False
	else:
		doctor.disponibilidad = True
	doctor.save()
	return redirect('admin_doctores')


