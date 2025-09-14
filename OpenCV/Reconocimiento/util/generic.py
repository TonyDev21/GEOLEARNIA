from PIL import ImageTk, Image   #-- import el uso de piloU

def leer_imagen(path, size): # se crea una funcion  de crear imagen el cual con el path es la ruta y el size en que parte
     return ImageTk.PhotoImage(Image.open(path).resize(size, Image.ADAPTIVE))
 # para REGRESAR O RETORNAR UNA IMAGEN 

def centrar_ventana(ventana,aplicacion_ancho,aplicacion_largo):   # esta funcion es para el centrado de ventanas y la calculamos por el x y Y 
    pantall_ancho = ventana.winfo_screenwidth()
    pantall_largo = ventana.winfo_screenheight()
    x = int((pantall_ancho/2) - (aplicacion_ancho/2))
    y = int((pantall_largo/2) - (aplicacion_largo/2))
    return ventana.geometry(f"{aplicacion_ancho}x{aplicacion_largo}+{x}+{y}")



