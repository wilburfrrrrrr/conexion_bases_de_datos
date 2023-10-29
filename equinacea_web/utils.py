import bcrypt

def hash_password(password):
	hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
	return hashed_password.decode('utf-8')

def verifica_password(password, hashed_password):
	return bcrypt.checkpw(password.encode('utf-8'), hashed_password.encode('utf-8'))

def iniciar_sesion(request, usuario):
	request.session['user_id'] = usuario.ID_usuario
	print("Sesion iniciada con el usuario: " + str(usuario.ID_usuario))

def unhash_password(hashed_password):
	return hashed_password.decode('utf-8')