from equinacea_web.models import Usuarios
from equinacea_web.utils import verifica_password


def autenticar(request, mail, password):
	try:
		usuario = Usuarios.objects.get(mail=mail)
		if verifica_password(password, usuario.password):

			return usuario
	except Usuarios.DoesNotExist:
		return None