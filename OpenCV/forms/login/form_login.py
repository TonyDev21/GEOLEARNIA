import tkinter as tk       
from tkinter import ttk, messagebox 
from tkinter.font import BOLD    # esta libreria seran para las configuraciones
import util.generic as utl        # traemos nuestra utilerias
from forms.master.form_master import MasterPanel  # traemos el masterpanel  
from forms.login.form_login_designar import FormLoginDesigner
from persistence.repository.auth_user_repository import AuthUserRepository
from persistence.model import Auth_User # importamos el modulo
import util.enoding_decoding as end_dec # nuestra utileria de incriptar y desc
# -----

class FormLogin(FormLoginDesigner):  # nuestro constructor o clase mas la hederacion
    
    def __init__(self):
        self.auth_repository = AuthUserRepository()
        super().__init__()
        # inicamos nuestro tu constructo para la conexion

    def verificar(self):  # metodo de verificacion 
         user_db: Auth_User = self.auth_repository.getUserByUserName(
            self.usuario.get())
         # traeme el usuario autenticado
         if(self.isUser(user_db)):
            self.isPassword(self.password.get(), user_db)
            # si existe verificamos



 # para verificar el usuario
    def isUser(self, user: Auth_User):
        status: bool = True
        if(user == None):
            status = False
            messagebox.showerror(
                message="El usuario no existe por favor registrese", title="Mensaje",parent=self.ventana)            
        return status 
    
 # para verificar la contraseña
    def isPassword(self, password: str, user: Auth_User):
        # que pase el pasword y usuario para ver si existe la contraseña
        b_password = end_dec.decrypt(user.password)
        if(password == b_password):
            self.ventana.destroy()
            MasterPanel()
        else:
            messagebox.showerror(
                message="La contraseña no es correcta", title="Mensaje")


