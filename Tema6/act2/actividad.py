import json
import csv
import logging
import os
from copy import deepcopy

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.FileHandler("log_datos.log"),
        logging.StreamHandler(),
    ],
)

class DataManager:
    def __init__(self, ruta_archivo, tipo_archivo="json"):
        self.ruta_archivo = ruta_archivo
        self.tipo_archivo = tipo_archivo
        self.version = 1
        self.transaccion_activa = False
        self.copia_datos = None

        if os.path.exists(ruta_archivo):
            self.datos = self._leer_archivo()
            logging.info(f"Archivo {tipo_archivo.upper()} cargado con éxito. Versión actual: {self.version}")
        else:
            self.datos = []
            self._guardar_archivo()

    def _leer_archivo(self):
        if self.tipo_archivo == "json":
            with open(self.ruta_archivo, "r") as archivo:
                return json.load(archivo)
        elif self.tipo_archivo == "csv":
            datos = []
            with open(self.ruta_archivo, mode="r") as archivo:
                lector = csv.DictReader(archivo)
                for fila in lector:
                    datos.append(fila)
            return datos
        else:
            raise ValueError("Tipo de archivo no soportado. Use 'json' o 'csv'.")

    def _guardar_archivo(self):
        if self.tipo_archivo == "json":
            with open(self.ruta_archivo, "w") as archivo:
                json.dump(self.datos, archivo, indent=4)
        elif self.tipo_archivo == "csv":
            if self.datos:
                with open(self.ruta_archivo, mode="w", newline="") as archivo:
                    escritor = csv.DictWriter(archivo, fieldnames=self.datos[0].keys())
                    escritor.writeheader()
                    escritor.writerows(self.datos)
        logging.info(f"Archivo {self.tipo_archivo.upper()} guardado. Versión actual: {self.version}")

    def iniciar_transaccion(self):
        if self.transaccion_activa:
            raise Exception("Ya hay una transacción activa.")
        self.transaccion_activa = True
        self.copia_datos = deepcopy(self.datos)
        logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        if not self.transaccion_activa:
            raise Exception("No hay una transacción activa para confirmar.")
        self.version += 1
        self.transaccion_activa = False
        self.copia_datos = None
        self._guardar_archivo()
        logging.info("Transacción confirmada y cambios guardados.")

    def revertir_transaccion(self):
        if not self.transaccion_activa:
            raise Exception("No hay una transacción activa para revertir.")
        self.datos = self.copia_datos
        self.transaccion_activa = False
        self.copia_datos = None
        logging.warning("Transacción revertida. Los cambios no se guardaron.")

    def leer_dato(self, clave, valor):
        return [dato for dato in self.datos if dato.get(clave) == valor]

    def escribir_dato(self, nuevo_dato):
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de realizar cambios.")
        self.datos.append(nuevo_dato)
        logging.info(f"Dato agregado: {nuevo_dato}")

    def eliminar_dato(self, clave, valor):
        if not self.transaccion_activa:
            raise Exception("Debe iniciar una transacción antes de realizar cambios.")
        self.datos = [dato for dato in self.datos if dato.get(clave) != valor]
        logging.info(f"Datos con {clave}={valor} eliminados.")

# Código principal
if __name__ == "__main__":
    # Crear instancia de DataManager para JSON
    data_manager = DataManager("plantas.json", "json")

    # Operación: Crear
    print("Iniciando operación: Crear...")
    data_manager.iniciar_transaccion()
    data_manager.escribir_dato({
        "nombre": "Rosa",
        "familia": "Rosaceae",
        "clima": "Templado",
        "tipo_suelo": "Arcilloso"
    })
    data_manager.escribir_dato({
        "nombre": "Cactus",
        "familia": "Cactaceae",
        "clima": "Árido",
        "tipo_suelo": "Arenoso"
    })
    data_manager.confirmar_transaccion()

    # Operación: Leer
    print("\nIniciando operación: Leer...")
    resultados = data_manager.leer_dato("nombre", "Rosa")
    print("Resultados:", resultados)

    # Operación: Actualizar
    print("\nIniciando operación: Actualizar...")
    data_manager.iniciar_transaccion()
    for planta in data_manager.datos:
        if planta["nombre"] == "Rosa":
            planta["clima"] = "Cálido"
    data_manager.confirmar_transaccion()

    # Operación: Eliminar
    print("\nIniciando operación: Eliminar...")
    data_manager.iniciar_transaccion()
    data_manager.eliminar_dato("nombre", "Cactus")
    data_manager.confirmar_transaccion()
