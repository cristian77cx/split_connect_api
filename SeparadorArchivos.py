import os
import pandas as pd

class ProcesadorArchivosSimple:
    FORMATOS_VALIDOS = ['.csv', '.xlsx', '.xls']
    FILAS_POR_ARCHIVO = 30

    def __init__(self, ruta_archivo, carpeta_destino):
        self.ruta_archivo = ruta_archivo
        self.carpeta_destino = carpeta_destino
        self.dataframe = None

    def validar_formato(self):
        _, ext = os.path.splitext(self.ruta_archivo)
        return ext.lower() in self.FORMATOS_VALIDOS

    def cargar_archivo(self):
        if not self.validar_formato():
            print("Error: Formato de archivo no válido. Se aceptan .csv, .xlsx, .xls.") # Corrected comma
            return False
        
        try:
            if self.ruta_archivo.lower().endswith('.csv'):
                self.dataframe = pd.read_csv(self.ruta_archivo)
            else:
                self.dataframe = pd.read_excel(self.ruta_archivo)
            
            print(f"Archivo cargado exitosamente con {len(self.dataframe)} filas y {len(self.dataframe.columns)} columnas.")
            return True
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
            return False

    def dividir_y_guardar(self):
        if self.dataframe is None or self.dataframe.empty:
            print("No hay datos para dividir.")
            return

        os.makedirs(self.carpeta_destino, exist_ok=True)

        total_filas = len(self.dataframe)
        print(f"Dividiendo {total_filas} filas en bloques de {self.FILAS_POR_ARCHIVO}...")

        # Dividir en partes de 30 filas
        for i in range(0, total_filas, self.FILAS_POR_ARCHIVO):
            parte = self.dataframe.iloc[i:i + self.FILAS_POR_ARCHIVO]
            archivo_salida = os.path.join(self.carpeta_destino, f"REQUEST_BODY_{i // self.FILAS_POR_ARCHIVO + 1}.json") # Changed to .json extension
            
            # *** CAMBIO CLAVE AQUI ***
            # Guarda la parte como JSON con orientación de registros (list of objects)
            parte.to_json(archivo_salida, orient='records', indent=4) 
            
            print(f"Archivo guardado: {archivo_salida}")

    def procesar(self):
        if self.cargar_archivo():
            self.dividir_y_guardar()
        else:
            print("No se pudo procesar el archivo.")

if __name__ == "__main__":
    # Configurar las rutas
    ruta_archivo = r"C:\\Users\\Aprendiz sena\\Desktop\\cuenta sbancarias.xlsx"  # Cambia por tu archivo
    carpeta_destino = "C:\\Users\\Aprendiz sena\\Desktop\\uploads"  # Cambia por tu carpeta destino

    # Crear y ejecutar el procesador
    procesador = ProcesadorArchivosSimple(ruta_archivo, carpeta_destino)
    procesador.procesar()