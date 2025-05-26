import os
import shutil
import pandas as pd
import json

class ProcesadorArchivos:
    FORMATOS_VALIDOS = ['.csv', '.xlsx', '.xls']
    MAX_COLUMNAS = 8

    def __init__(self, ruta_archivo, carpeta_destino):
        self.ruta_archivo = ruta_archivo
        self.carpeta_destino = carpeta_destino
        self.dataframe = None

    def validar_formato(self):
        _, ext = os.path.splitext(self.ruta_archivo)
        return ext.lower() in self.FORMATOS_VALIDOS

    def cargar_archivo(self):
        if not self.validar_formato():
            print(f"Error: Formato no válido. Se aceptan: {self.FORMATOS_VALIDOS}")
            return False

        try:
            if self.ruta_archivo.lower().endswith('.csv'):
                # Primero leemos el archivo como texto para analizar su estructura
                with open(self.ruta_archivo, 'r') as f:
                    first_line = f.readline().strip()

                # Determinamos el separador y si hay comillas
                if ';' in first_line:
                    sep = ';'
                elif ',' in first_line:
                    sep = ','
                else:
                    sep = None

                # Leemos el CSV con los parámetros adecuados
                self.dataframe = pd.read_csv(
                    self.ruta_archivo,
                    sep=sep,
                    quotechar='"',
                    skipinitialspace=True,
                    engine='python'
                )

                # Si el CSV tiene una estructura inusual (todos los datos en una columna)
                if len(self.dataframe.columns) == 1:
                    # Intentamos separar los datos
                    col_name = self.dataframe.columns[0]
                    self.dataframe = self.dataframe[col_name].str.split(',', expand=True)

                    # Asignamos los nombres de las columnas si es posible
                    if 'typeDocument' in first_line:
                        headers = first_line.split(sep)
                        headers = [h.strip().replace('"', '') for h in headers]
                        self.dataframe.columns = headers
            else:
                self.dataframe = pd.read_excel(self.ruta_archivo)

            # Limpieza de nombres de columnas
            self.dataframe.columns = [col.strip().replace('"', '') for col in self.dataframe.columns]

            # Convertir todas las columnas a string para consistencia
            self.dataframe = self.dataframe.astype(str)

            if len(self.dataframe.columns) > self.MAX_COLUMNAS:
                print(f"Error: El archivo tiene más de {self.MAX_COLUMNAS} columnas")
                return False

            if self.dataframe.empty:
                print("Error: El archivo está vacío")
                return False

            return True

        except Exception as e:
            print(f"Error al cargar el archivo: {str(e)}")
            return False

    def guardar_archivo(self):
        try:
            os.makedirs(self.carpeta_destino, exist_ok=True)
            nombre_archivo = os.path.basename(self.ruta_archivo)
            destino = os.path.join(self.carpeta_destino, nombre_archivo)

            if os.path.abspath(self.ruta_archivo) != os.path.abspath(destino):
                shutil.copy2(self.ruta_archivo, destino)
                print(f"Archivo guardado exitosamente en: {destino}")
        except Exception as e:
            print(f"Error al guardar el archivo: {str(e)}")

    def exportar_a_json(self):
        if self.dataframe is not None:
            try:
                json_path = os.path.join(self.carpeta_destino, "Request_Body.json")

                # Limpieza adicional de datos antes de exportar
                clean_data = []
                for _, row in self.dataframe.iterrows():
                    clean_row = {}
                    for col, val in row.items():
                        # Eliminar comillas adicionales si existen
                        clean_val = val.strip().replace('"', '')
                        clean_row[col] = clean_val
                    clean_data.append(clean_row)

                # Exportar en formato 'records' para la estructura deseada
                with open(json_path, 'w') as f:
                    json.dump(clean_data, f, indent=4, ensure_ascii=False)

                print(f"JSON generado correctamente en: {json_path}")

                # Mostrar preview del JSON
                with open(json_path, 'r') as f:
                    print("\nEstructura del JSON generado:")
                    print(f.read()[:500])  # Mostrar parte inicial

            except Exception as e:
                print(f"Error al exportar a JSON: {str(e)}")
        else:
            print("No hay datos cargados para exportar.")

    def procesar(self):
        if self.cargar_archivo():
            self.guardar_archivo()
            self.exportar_a_json()
        else:
            print("No se pudo procesar el archivo.")
            
if __name__ == "__main__":
    # Configura tus rutas directamente aquí
    ruta_archivo = r"C:\\Users\\Aprendiz sena\\Desktop\\cuenta sbancarias.xlsx"  # Cambia por tu ruta

    carpeta_destino = "C:\\Users\\Aprendiz sena\\Desktop\\uploads\\Exportador de Json"  # Cambia por tu ruta

    # Ejecutar el procesador
    procesador = ProcesadorArchivos(ruta_archivo, carpeta_destino)
    procesador.procesar()
