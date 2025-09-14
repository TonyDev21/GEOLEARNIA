from cryptography.fernet import  Fernet #utileria para incriptar y descriptar nuestras contraseñas

def encrypted(password:str):    # nuestra variable tipo string
    f = Fernet(b'FINEHtwMUOxgvyYM9fOvpXcQHYDDZKb3-NkPWTrZN5g=') # para incriptar nuestra contraseña
    b_password = bytes(password, 'ascii')  # el pasword convertir en valores de bytes 
    encrypted_password = f.encrypt(b_password)
    return encrypted_password.decode('ascii') # guardes los resultados y retornamos ed caracteres ascii

def decrypt(password:str):      
    f = Fernet(b'FINEHtwMUOxgvyYM9fOvpXcQHYDDZKb3-NkPWTrZN5g=')
    b_password = bytes(password, 'ascii') 
    b_password_decrypt = f.decrypt(b_password) # que los desencripte 
    return b_password_decrypt.decode('ascii') # que los convierta a valores ascii