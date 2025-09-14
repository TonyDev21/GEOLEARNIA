import tkinter as tk
from tkinter.font import BOLD # esta libreria seran para las configuraciones
import util.generic as utl # traemos nuestra utilerias

class MasterPanel:  # generamos una clase para tener un conector
    
                                      
    def __init__(self):         # creara nuestra ventana
        self.ventana = tk.Tk()                             
        self.ventana.title('Master panel')  # el nombre del titulo de la ventana
        w, h = self.ventana.winfo_screenwidth(), self.ventana.winfo_screenheight()        # buscar el ancho y alto de nuestra ventana                            
        self.ventana.geometry("%dx%d+0+0" % (w, h)) # aqui hacemos un formateo de tuplas 
        self.ventana.config(bg='#fcfcfc')  # el tipo de fondo que quiero
        self.ventana.resizable(width=0, height=0)  # no le permitimos redimensionar
        
        logo =utl.leer_imagen("./imagenes/lobo.jpg", (200, 200)) # nuestro logo y sus píxeles
                        
        label = tk.Label( self.ventana, image=logo,bg='#3a7ff6' ) # colocar nuestra imagen y nuestra etiqueta en tamaño completo
        label.place(x=0,y=0,relwidth=1, relheight=1) # nos ayuda a centrar
        
        self.ventana.mainloop() # este metodo es para que se mantega abierta