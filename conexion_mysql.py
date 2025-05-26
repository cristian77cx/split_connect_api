import mysql.connector

try:
    # Conectar a la base de datos
    connection = mysql.connector.connect(
        host="localhost",       # Dirección del servidor MySQL
        user="root",            # Usuario de MySQL
        password="",            # Deja vacío si no usas contraseña
        database="api_test"     # Nombre de la base de datos
    )

    # Verificar la conexión
    if connection.is_connected():
        print("¡Conexión exitosa a la base de datos!")

        # Crear un cursor para ejecutar consultas SQL
        cursor = connection.cursor()

        # Insertar un dato en la tabla
        insertar_dato = """
        INSERT INTO Table_request_body (key1, key2, key3)
        VALUES (%s, %s, %s)
        """
        valores = ("valor1", "valor2", "valor3")
        cursor.execute(insertar_dato, valores)

        # Confirmar cambios
        connection.commit()
        print("¡Dato insertado exitosamente!")

        # Consultar los datos de la tabla
        cursor.execute("SELECT * FROM Table_request_body")
        resultados = cursor.fetchall()
        print("Datos en la tabla:")
        for fila in resultados:
            print(fila)

except mysql.connector.Error as err:
    print(f"Error conectando a la base de datos: {err}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
        print("Conexión cerrada.")

