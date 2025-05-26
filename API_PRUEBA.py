from flask import Flask, request, jsonify
import mysql.connector
from werkzeug.utils import secure_filename
import os
import json

app = Flask(__name__)

# Configuración de subida de archivos
UPLOAD_FOLDER = './uploads'
ALLOWED_EXTENSIONS = {'json'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Crear carpeta de subida si no existe
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Función para verificar extensiones permitidas
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Conexión a la base de datos
def get_db_connection():
    return mysql.connector.connect(
        host="localhost",
        user="root",
        password="",  # Agrega tu contraseña si tienes
        database="api_test"
    )

# Ruta para subir archivos
@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files: 
        return jsonify({"error": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        try:
            with open(filepath, 'r') as f:
                data = json.load(f)

            if not isinstance(data, list):
                return jsonify({"error": "El archivo debe contener una lista de objetos JSON"}), 400

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
            return jsonify({"message": "Datos insertados exitosamente"}), 200

        except Exception as e:
            return jsonify({"error": f"Error al procesar el archivo: {str(e)}"}), 500
        finally:
            cursor.close()
            connection.close()

    return jsonify({"error": "Tipo de archivo no permitido"}), 400

# Ejecutar servidor
if __name__ == '__main__':
   app.run(port=8080, debug=True, use_reloader=False)


