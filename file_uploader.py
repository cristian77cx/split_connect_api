import os
import requests
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class FileHandler(FileSystemEventHandler):
    def __init__(self, url_api):
        self.url_api = url_api

    def on_created(self, event):
        if event.is_directory:
            return

        archivo = event.src_path
        if archivo.endswith('.json'):
            print(f"Nuevo archivo detectado: {archivo}")
            try:
                with open(archivo, 'rb') as f:
                    respuesta = requests.post(self.url_api, files={'file': (os.path.basename(archivo), f)})
                if respuesta.status_code == 200:
                    print(f"Archivo {os.path.basename(archivo)} enviado exitosamente: {respuesta.json()}")
                else:
                    print(f"Error al enviar {os.path.basename(archivo)}: {respuesta.status_code} - {respuesta.text}")
            except Exception as e:
                print(f"Error al procesar {os.path.basename(archivo)}: {e}")

def monitor_directorio(directorio, url_api):
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe.")
        return

    event_handler = FileHandler(url_api)
    observer = Observer()
    observer.schedule(event_handler, path=directorio, recursive=False)
    observer.start()

    print(f"Monitoreando el directorio: {directorio}")
    try:
        while True:
            pass  # Mantener el programa corriendo
    except KeyboardInterrupt:
        observer.stop()
    observer.join()

# Configuración
directorio = "C:\\Users\\Aprendiz sena\\Desktop\\uploads"
url_api = "http://127.0.0.1:8080/upload"

monitor_directorio(directorio, url_api)
