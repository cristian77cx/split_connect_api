import os
import json
import mysql.connector
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

# Función para conectar a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Agrega tu contraseña si tienes
        database="api_test"
    )

# Clase para manejar eventos del sistema de archivos
class FileHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return

        archivo = event.src_path
        if archivo.endswith('.json'):
            print(f"Nuevo archivo detectado: {archivo}")
            try:
                with open(archivo, 'r') as f:
                    data = json.load(f)

                if not isinstance(data, list):
                    print(f"Error: El archivo {archivo} no contiene una lista de objetos JSON.")
                    return

                connection = get_db_connection()
                cursor = connection.cursor()

                for obj in data:
                    sql = """
                    INSERT INTO Table_request_body (
                        typeDocument, subAccountId, firstName, lastName,
                        bankAccountNumber, bankAccountType, bankName, bankCode
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    """
                    cursor.execute(sql, (
                        obj.get("typeDocument"),
                        obj.get("subAccountId"),
                        obj.get("firstName"),
                        obj.get("lastName"),
                        obj.get("bankAccountNumber"),
                        obj.get("bankAccountType"),
                        obj.get("bankName"),
                        obj.get("bankCode")
                    ))

                connection.commit()
                print(f"Datos del archivo {archivo} insertados exitosamente en la base de datos.")

            except Exception as e:
                print(f"Error al procesar {archivo}: {e}")

            finally:
                if cursor:
                    cursor.close()
                if connection:
                    connection.close()

# Función para monitorear el directorio
def monitor_directorio(directorio):
    if not os.path.exists(directorio):
        print(f"El directorio {directorio} no existe.")
        return

    event_handler = FileHandler()
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
monitor_directorio(directorio)

