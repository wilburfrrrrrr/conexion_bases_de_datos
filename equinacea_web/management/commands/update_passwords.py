from django.core.management.base import BaseCommand
from equinacea_web.models import Usuarios
from equinacea_web.utils import hash_password
class Command(BaseCommand):
	help = 'Update passwords'
	def handle(self, *args, **options):
		usuarios = Usuarios.objects.all()
		for usuario in usuarios:
			if not usuario.password.startswith("$2b$"):
				usuario.password = hash_password(usuario.password)
				usuario.save()
		self.stdout.write(self.style.SUCCESS('Contraseñas actualizadas'))