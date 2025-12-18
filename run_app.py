"""
GEOLEARNIA Desktop - Launcher
"""
import os
import sys
import webbrowser
import time
from threading import Thread

def open_browser():
    """Abrir navegador después de 5 segundos"""
    time.sleep(5)
    webbrowser.open('http://127.0.0.1:5000')

if __name__ == '__main__':
    # Cambiar al directorio del script
    if getattr(sys, 'frozen', False):
        os.chdir(os.path.dirname(sys.executable))
    else:
        os.chdir(os.path.dirname(__file__))
    
    # Abrir navegador en segundo plano
    Thread(target=open_browser, daemon=True).start()
    
    # Ejecutar Flask (esto importa y ejecuta app.py)
    import app
