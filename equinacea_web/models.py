from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, AbstractBaseUser, BaseUserManager, PermissionsMixin, Group, Permission
from django.contrib.auth.hashers import check_password

# class CustomUserManager(BaseUserManager):
# 	def create_user(self, mail, password = None, **extra_fields):
# 		if not mail:
# 			raise ValueError('El usuario debe tener un mail')
# 		mail_normalizado = self.normalize_email(mail)
# 		user = self.model(mail=mail_normalizado, **extra_fields)
# 		user.set_password(password)
# 		user.save(using = self._db)
# 		return user
	
# 	def create_superuser(self, mail, password = None, **extra_fields):
# 		extra_fields.setdefault('is_staff', True)
# 		extra_fields.setdefault('is_superuser', True)
# 		if extra_fields.get('is_staff') is not True:
# 			raise ValueError('El superusuario debe tener is_staff = True')
# 		if extra_fields.get('is_superuser') is not True:
# 			raise ValueError('El superusuario debe tener is_superuser = True')
# 		return self.create_user(mail, password, **extra_fields)

class Usuarios(models.Model):
	ID_usuario = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_usuario')
	nombre = models.CharField(max_length=45, db_column = 'nombre')
	apellido = models.CharField(max_length=45, db_column = 'apellido')
	mail = models.CharField(max_length=45, unique=True, db_column = 'mail')
	telefono = models.CharField(max_length=45, db_column = 'telefono')
	password = models.CharField(max_length=72, db_column = 'password')

	class Meta:
		db_table = 'usuarios'
	def __str__(self):
		return self.nombre + ' ' + self.apellido


# class CustomUser(AbstractBaseUser, PermissionsMixin):
# 	ID_usuario = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_usuario')
# 	nombre = models.CharField(max_length=45, db_column = 'nombre')
# 	apellido = models.CharField(max_length=45, db_column = 'apellido')
# 	mail = models.CharField(max_length=45, unique=True, db_column = 'mail')
# 	telefono = models.CharField(max_length=45, db_column = 'telefono')
# 	password = models.CharField(max_length=45, db_column = 'password')

# 	objects = CustomUserManager()
# 	USERNAME_FIELD = 'mail'

# 	is_staff = models.BooleanField(default=False)
# 	is_active = models.BooleanField(default=True)

# 	groups = models.ManyToManyField(Group, related_name='custom_users')
# 	user_permissions = models.ManyToManyField(Permission, related_name='custom_users')

# # 	# class Meta:
# 	# 	db_table = 'usuarios'
		
# 	def check_password(self, raw_password):
# 		return check_password(raw_password, self.password)
	
# 	def __str__(self):
# 		return self.nombre + ' ' + self.apellido


	


class Turnos(models.Model):
	ID_turno = models.AutoField(primary_key=True, db_column = 'ID_turno')
	paciente = models.ForeignKey('Pacientes', on_delete=models.CASCADE, db_column = 'paciente')
	tipo = models.ForeignKey('TipoCita', on_delete=models.CASCADE, db_column = 'tipo')
	especialidad = models.ForeignKey('Especialidades', on_delete=models.CASCADE, db_column = 'especialidad')
	estado = models.CharField(max_length=45, db_column = 'estado')
	fecha_reserva = models.DateField(db_column = 'fecha_reserva')
	fecha_turnos = models.DateField(db_column = 'fecha_turnos')	
	class Meta:
		db_table = 'turnos'

class Historial(models.Model):
	paciente = models.OneToOneField('Pacientes', on_delete=models.CASCADE, db_column = 'paciente', primary_key=True)
	situacion = models.CharField(max_length=200, db_column = 'situacion', default = ' ')
	observaciones = models.CharField(max_length=200, db_column = 'observaciones', default = ' ')
	fecha_modificacion = models.DateField(db_column = 'fecha_modificacion', default = timezone.now)
	class Meta:
		db_table = 'historial'	

class Pacientes(models.Model):
	ID_paciente = models.OneToOneField('Usuarios', on_delete=models.CASCADE, db_column='ID_paciente', primary_key=True)	
	class Meta:
		db_table = 'pacientes'

class Especialidades(models.Model):
	ID_especialidad = models.AutoField(primary_key=True, db_column = 'ID_especialidad')
	especialidad = models.CharField(max_length=45, db_column = 'especialidad')
	class Meta:
		db_table = 'especialidades'

	def __str__(self):
		return self.especialidad

class Doctores(models.Model):
	ID_doctor = models.OneToOneField('Usuarios', on_delete=models.CASCADE, db_column='ID_doctor', primary_key=True)	
	especialidad = models.ForeignKey('Especialidades', on_delete=models.CASCADE, db_column = 'especialidad')
	disponibilidad = models.BooleanField(db_column = 'disponibilidad', default = True)
	class Meta:
		db_table = 'doctores'

	def __str__(self):
		return self.ID_doctor.nombre + ' ' + self.ID_doctor.apellido

class TipoCita(models.Model):
	ID_tipo = models.AutoField(primary_key=True, db_column = 'ID_tipo')
	tipo = models.CharField(max_length=45, db_column = 'tipo')
	class Meta:
		db_table = 'tipos_cita'

	def __str__(self):
		return self.tipo

class Cajeros(models.Model):
	ID_cajero = models.OneToOneField('Usuarios', on_delete=models.CASCADE, db_column='ID_cajero', primary_key=True)
	class Meta:
		db_table = 'cajeros'

class Administradores(models.Model):
	ID_administrador = models.OneToOneField('Usuarios', on_delete=models.CASCADE, db_column='ID_administrador', primary_key=True)
	class Meta:
		db_table = 'administrador'

class Citas(models.Model):
	ID_cita = models.AutoField(primary_key=True, db_column = 'ID_cita')
	paciente = models.ForeignKey('Pacientes', on_delete=models.CASCADE, db_column = 'paciente')
	doctor = models.ForeignKey('Doctores', on_delete=models.CASCADE, db_column = 'doctor')
	tipo = models.ForeignKey('TipoCita', on_delete=models.CASCADE, db_column = 'tipo')
	fecha = models.DateField(db_column = 'fecha', default = timezone.now)
	class Meta:
		db_table = 'citas'

class UsuariosEliminados(models.Model):
	ID_usuario = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_usuario')
	nombre = models.CharField(max_length=45, db_column = 'nombre')
	apellido = models.CharField(max_length=45, db_column = 'apellido')
	mail = models.CharField(max_length=45, db_column = 'mail')
	telefono = models.CharField(max_length=45, db_column = 'telefono')
	password = models.CharField(max_length=45, db_column = 'pass')
	fecha_eliminado = models.DateField()
	class Meta:
		db_table = 'usuarios_eliminados'

class TurnosEliminados(models.Model):
	ID_turno = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_turno')
	ID_usuario = models.IntegerField(db_column = 'ID_usuario')
	nombre = models.CharField(max_length=45, db_column = 'nombre')
	apellido = models.CharField(max_length=45, db_column = 'apellido')
	tipo = models.CharField(max_length=45, db_column = 'tipo')
	especialidad = models.CharField(max_length=45, db_column = 'especialidad')
	estado = models.CharField(max_length=45, db_column = 'estado')
	fecha_reserva = models.DateField(db_column = 'fecha_reserva')
	fecha_turnos = models.DateField(db_column = 'fecha_turnos')
	fecha_eliminado = models.DateField(db_column = 'fecha_eliminado')
	class Meta:
		db_table = 'turnos_eliminados'

class PacientesEliminados(models.Model):
	ID_usuario = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_usuario')
	nombre = models.CharField(max_length=45, db_column = 'nombre')
	apellido = models.CharField(max_length=45, db_column = 'apellido')
	mail = models.CharField(max_length=45, db_column = 'mail')
	telefono = models.CharField(max_length=45, db_column = 'telefono')
	situacion = models.CharField(max_length=200, db_column = 'situacion')
	observaciones = models.CharField(max_length=200, db_column = 'observaciones')
	fecha_modificacion = models.DateField(db_column = 'fecha_modificacion')
	fecha_eliminado = models.DateField(db_column = 'fecha_eliminado')
	class Meta:
		db_table = 'pacientes_eliminados'

class EspecialidadesEliminados(models.Model):
	ID_especialidad = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_especialidad')
	especialidad = models.CharField(max_length=45, db_column = 'especialidad')
	fecha_eliminado = models.DateField(db_column = 'fecha_eliminado')
	class Meta:
		db_table = 'especialidades_eliminados'


class DoctoresEliminados(models.Model):
	ID_usuario = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_usuario')
	nombre = models.CharField(max_length=45, db_column = 'nombre')
	apellido = models.CharField(max_length=45, db_column = 'apellido')
	mail = models.CharField(max_length=45, db_column = 'mail')
	telefono = models.CharField(max_length=45, db_column = 'telefono')
	especialidad = models.CharField(max_length=45, db_column = 'especialidad')
	fecha_eliminado = models.DateField(db_column = 'fecha_eliminado')
	class Meta:
		db_table = 'doctores_eliminados'

class TipoCitaEliminados(models.Model):
	ID_tipo = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_tipo')
	tipo = models.CharField(max_length=45, db_column = 'tipo')
	fecha_eliminado = models.DateField(db_column = 'fecha_eliminado')	
	class Meta:
		db_table = 'tipos_citas_eliminados'

class CitasEliminados(models.Model):
	ID_cita = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_cita')
	ID_paciente = models.IntegerField(db_column = 'ID_paciente')
	nombre_paciente = models.CharField(max_length=45, db_column = 'nombre_paciente')
	apellido_paciente = models.CharField(max_length=45, db_column = 'apellido_paciente')
	ID_doctor = models.IntegerField(db_column = 'ID_doctor')
	nombre_doctor = models.CharField(max_length=45, db_column = 'nombre_doctor')	
	apellido_doctor = models.CharField(max_length=45, db_column = 'apellido_doctor')
	tipo = models.CharField(max_length=45, db_column = 'tipo')
	fecha_eliminado = models.DateField(db_column = 'fecha_eliminado')
	fecha = models.DateField(db_column = 'fecha', default = timezone.now)
	class Meta:
		db_table = 'citas_eliminados'

class CajerosEliminados(models.Model):
	ID_usuario = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_usuario')
	nombre = models.CharField(max_length=45, db_column = 'nombre')
	apellido = models.CharField(max_length=45, db_column = 'apellido')
	mail = models.CharField(max_length=45, db_column = 'mail')
	telefono = models.CharField(max_length=45, db_column = 'telefono')
	fecha_eliminado = models.DateField(db_column = 'fecha_eliminado')
	class Meta:
		db_table = 'cajeros_eliminados'

class AdministradoresEliminados(models.Model):
	ID_usuario = models.IntegerField(primary_key=True, unique=True, db_column = 'ID_usuario')
	nombre = models.CharField(max_length=45, db_column = 'nombre')
	apellido = models.CharField(max_length=45, db_column = 'apellido')
	mail = models.CharField(max_length=45, db_column = 'mail')
	telefono = models.CharField(max_length=45, db_column = 'telefono')
	fecha_eliminado = models.DateField(db_column = 'fecha_eliminado')
	class Meta:
		db_table = 'administradores_eliminados'
