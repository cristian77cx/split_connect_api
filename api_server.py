import json
from http.server import BaseHTTPRequestHandler, HTTPServer
import mysql.connector

# Conexión a la base de datos
def conectar_base_datos():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Si tienes contraseña, ponla aquí
        database="api_test"
    )

# Servidor HTTP
class APIHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Verificar si la ruta es "/insert"
        if self.path == "/insert":
            content_length = int(self.headers['Content-Length'])  # Tamaño del cuerpo de la solicitud
            post_data = self.rfile.read(content_length)  # Leer los datos enviados
            try:
                # Convertir datos JSON a un diccionario
                data = json.loads(post_data)
                if isinstance(data, list):  # Validar que sea un array de objetos
                    for item in data:
                        # Validar las llaves esperadas
                        keys = ["key1", "key2", "key3"]
                        for key in list(item.keys()):
                            if key not in keys:
                                del item[key]  # Eliminar llaves no deseadas

                        # Insertar en la base de datos
                        connection = conectar_base_datos()
                        cursor = connection.cursor()
                        insertar_dato = """
                        INSERT INTO Table_request_body (key1, key2, key3)
                        VALUES (%s, %s, %s)
                        """
                        valores = (item.get("key1"), item.get("key2"), item.get("key3"))
                        cursor.execute(insertar_dato, valores)
                        connection.commit()
                        cursor.close()
                        connection.close()

                    # Respuesta exitosa
                    self.send_response(200)
                    self.send_header("Content-Type", "application/json")
                    self.end_headers()
                    self.wfile.write(json.dumps({"message": "Datos insertados exitosamente"}).encode())
                else:
                    raise ValueError("El cuerpo de la solicitud debe ser un array de objetos.")
            except Exception as e:
                # Responder con error
                self.send_response(400)
                self.send_header("Content-Type", "application/json")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode())
        else:
            # Ruta no encontrada
            self.send_response(404)
            self.end_headers()

# Configuración del servidor
def run(server_class=HTTPServer, handler_class=APIHandler, port=8080):
    server_address = ('', port)
    httpd = server_class(server_address, handler_class)
    print(f"Servidor corriendo en el puerto {port}...")
    httpd.serve_forever()

if __name__ == "__main__":
    run()
