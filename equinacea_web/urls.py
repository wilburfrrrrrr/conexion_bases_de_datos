"""
URL configuration for equinacea_web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from equinacea_web import views

urlpatterns = [
    path('djadmin/', admin.site.urls),
	path('', views.inicio, name='inicio'),
	path('log_in/', views.login_usuario, name='login_usuario'),
	path('log_out/', views.logout_usuario, name='logout_usuario'),
	path('registro_p/', views.registro_pacientes, name='registro_pacientes'),#
	path('cajeros/', views.cajeros, name='cajeros'),#
	path('cajeros/<int:id_turno>/registro_cita/', views.registro_citas, name='registro_citas'),#
	path('doctores/', views.doctores, name='doctores'),#
	path('pacientes/', views.pacientes, name='pacientes'),#
	path('pacientes/registro_turnos/', views.registro_turnos, name='registro_turnos'),#
	path('doctores/<int:id_cita>/cita/', views.cita, name='cita'),
	path('admin/', views.admin, name='admin'),#
	path('admin/admin_c/', views.admin_cajeros, name='admin_cajeros'),#
	path('admin/admin_d/', views.admin_doctores, name='admin_doctores'),#
	path('admin/admin_p/', views.admin_pacientes, name='admin_pacientes'),#
	path('admin/c_archivados/', views.cajeros_archivados, name='cajeros_archivados'),#
	path('admin/d_archivados/', views.doctores_archivados, name='doctores_archivados'),#
	path('admin/p_archivados/', views.pacientes_archivados, name='pacientes_archivados'),#
	path('admin/ci_archivadas/', views.citas_archivadas, name='citas_archivadas'),#
	path('admin/t_archivados/', views.turnos_archivados, name='turnos_archivados'),#
	path('admin/admin_c/registro_c/', views.registro_cajeros, name='registro_cajeros'),#
	path('admin/admin_d/registro_d/', views.registro_doctores, name='registro_doctores'),#
	path('admin/admin_r/registro_a/', views.registro_admin, name='registro_admin'),#
	path('registro_p/', views.registro_pacientes, name='registro_pacientes'),#	
	path('admin/admin_c/<int:id_cajero>/eliminar', views.archivar_cajero, name='archivar_cajero'),
	path('admin/admin_d/<int:id_doctor>/eliminar', views.archivar_doctor, name='archivar_doctor'),
	path('admin/admin_d/<int:id_doctor>/actualizar', views.actualizar_disponibilidad, name='actualizar_disponibilidad'),
	path('admin/admin_p/<int:id_paciente>/eliminar', views.archivar_paciente, name='archivar_paciente'),
	path('doctores/<int:id_cita>/eliminar', views.archivar_cita, name='archivar_cita'),
	path('cajeros/<int:id_turno>/eliminar', views.archivar_turno, name='archivar_turno'),
	

	# eliminar usuario: paciente, doctor, cajero, administrador
	# eliminar citas
	# eliminar turnos
	# actualizar usuario: paciente, doctor, cajero, administrador
	
]	
