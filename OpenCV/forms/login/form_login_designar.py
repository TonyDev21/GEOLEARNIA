import tkinter as tk       
from tkinter import ttk
   # esta libreria seran para las configuraciones
import util.generic as utl        # traemos nuestra utilerias

# -----

class FormLoginDesigner:  # nuestro constructor o clase
    
    
    def verificar(self):  # metodo de verificacion 
       pass

    def userRegister(self): #  metodo de verificacion
        pass

                      
    def __init__(self):        # creamos la ventana
        self.ventana = tk.Tk()                             
        self.ventana.title('Inicio de sesion') # el titulo
        self.ventana.geometry('800x500')      # el tamaño
        self.ventana.config(bg='#fcfcfc')     # el color
        self.ventana.resizable(width=0, height=0)    # que no se pueda modificar par maximizar
        utl.centrar_ventana(self.ventana,800,500) # el calculo para centrar hacia la ventana
        
        logo =utl.leer_imagen("./imagenes/lobo.jpg", (200, 200))  # creamos nuestro logo para traerlo al panel
        # frame_logo
        frame_logo = tk.Frame(self.ventana, bd=0, width=300, relief=tk.SOLID, padx=10, pady=10,bg='#3a7ff6')
        # que no tenga bordes  y tenga estos espacios 
        frame_logo.pack(side="left",expand=tk.YES,fill=tk.BOTH)
        # creamos un bloque de espacio
        label = tk.Label( frame_logo, image=logo,bg='#3a7ff6' )
        # colocamos  el logo y se muestre en el frame
        label.place(x=0,y=0,relwidth=1, relheight=1)

        # que abarque todo el frame de ancho y largo

        #-----------------------------------------------------------------------------------------
        
        #frame_form
        frame_form = tk.Frame(self.ventana, bd=0, relief=tk.SOLID, bg='#fcfcfc') # para el color del lado derecho
        frame_form.pack(side="right",expand=tk.YES,fill=tk.BOTH) 
        #frame_form
        
        #-----------------------------------------------------------------------------------------
        
        #frame_form_top      # nuestro titulo
        frame_form_top = tk.Frame(frame_form,height = 50, bd=0, relief=tk.SOLID,bg='black') # con borde y color negro
        frame_form_top.pack(side="top",fill=tk.X) # que se espanda en el area de x
        title = tk.Label(frame_form_top, text="Inicio de sesion",font=('Times', 30), fg="#666a88",bg='#fcfcfc',pady=50)
        # el nombre de inicio de sesion 
        title.pack(expand=tk.YES,fill=tk.BOTH)  # que se expanda en todo el espacio
        #end frame_form_top

        #-----------------------------------------------------------------------------------------

        #frame_form_fill     # el frame de abajo
        frame_form_fill = tk.Frame(frame_form,height = 50,  bd=0, relief=tk.SOLID,bg='#fcfcfc')
        frame_form_fill.pack(side="bottom",expand=tk.YES,fill=tk.BOTH) 

        etiqueta_usuario = tk.Label(frame_form_fill, text="Usuario", font=('Times', 14) ,fg="#666a88",bg='#fcfcfc', anchor="w")
        # usuario , tipografia , color de fondo y posicionar al punto cardinal al este
        etiqueta_usuario.pack(fill=tk.X, padx=20,pady=5)
        # nuestra colocacion de area
        self.usuario = ttk.Entry(frame_form_fill, font=('Times', 14))
        # que se apilen los bloques
        self.usuario.pack(fill=tk.X, padx=20,pady=10)

        etiqueta_password = tk.Label(frame_form_fill, text="Contraseña", font=('Times', 14),fg="#666a88",bg='#fcfcfc' , anchor="w")
        # lo mismo que arriba 
        etiqueta_password.pack(fill=tk.X, padx=20,pady=5)

        self.password = ttk.Entry(frame_form_fill, font=('Times', 14))
        self.password.pack(fill=tk.X, padx=20,pady=10)
        self.password.config(show="*")
        # todo lo que escribamos se muestre en *

        inicio = tk.Button(frame_form_fill,text="Iniciar sesion",font=('Times', 15),bg='#3a7ff6', bd=0,fg="#fff",command=self.verificar)
       # nuestro boton, el texto, tamaño  
        inicio.pack(fill=tk.X, padx=20,pady=20)        
       

        inicio.bind("<Return>", (lambda event: self.verificar()))
     # detectamos el click y con lambda que se dispare el evento pre cargada 
    
        #end frame_form_fill
           
        inicio = tk.Button(frame_form_fill,text="Registrar usuario",font=(
           'Times', 15),bg='#fcfcfc', bd=0,fg="#3a7ff6",command=self.userRegister)
       # nuestro boton, el texto, tamaño  
        inicio.pack(fill=tk.X, padx=20,pady=20)        

        inicio.bind("<Return>", (lambda event: self.userRegister()))
        #-----------------------------------------------------------------------------------------

        self.ventana.mainloop() # para que se muestre la ventana

