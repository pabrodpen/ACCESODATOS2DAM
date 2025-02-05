#DataManager → Para gestionar datos en JSON y CSV.

import json
import csv
import logging
import os
from copy import deepcopy

# Configuración de logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("log_datos.log"), logging.StreamHandler()],
)

class DataManager:
    def __init__(self, ruta_archivo, tipo_archivo="json"):
        self.ruta_archivo = ruta_archivo
        self.tipo_archivo = tipo_archivo
        self.transaccion_activa = False
        self.copia_datos = None

        if os.path.exists(ruta_archivo):
            self.datos = self._leer_archivo()
            logging.info(f"Archivo {tipo_archivo.upper()} cargado correctamente.")
        else:
            self.datos = []
            self._guardar_archivo()

    def _leer_archivo(self):
        if self.tipo_archivo == "json":
            with open(self.ruta_archivo, "r") as archivo:
                return json.load(archivo)
        elif self.tipo_archivo == "csv":
            with open(self.ruta_archivo, mode="r") as archivo:
                return list(csv.DictReader(archivo))
        else:
            raise ValueError("Tipo de archivo no soportado.")

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
        logging.info(f"Archivo {self.tipo_archivo.upper()} guardado.")

    def iniciar_transaccion(self):
        self.transaccion_activa = True
        self.copia_datos = deepcopy(self.datos)
        logging.info("Transacción iniciada.")

    def confirmar_transaccion(self):
        self.transaccion_activa = False
        self.copia_datos = None
        self._guardar_archivo()
        logging.info("Transacción confirmada.")

    def revertir_transaccion(self):
        self.datos = self.copia_datos
        self.transaccion_activa = False
        self.copia_datos = None
        logging.warning("Transacción revertida.")

# Uso del DataManager
if __name__ == "__main__":
    data_manager = DataManager("plantas.json", "json")
    data_manager.iniciar_transaccion()
    data_manager.datos.append({"nombre": "Rosa", "familia": "Rosaceae", "clima": "Templado"})
    data_manager.confirmar_transaccion()
#DatabaseManager → Para conectarse a una base de datos MySQL.

import mysql.connector

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.connection = mysql.connector.connect(host=host, user=user, password=password, database=database)
        self.cursor = self.connection.cursor()

    def crear_tabla(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS Plantas (
                id INT AUTO_INCREMENT PRIMARY KEY,
                nombre VARCHAR(255),
                familia VARCHAR(255),
                clima VARCHAR(255)
            )
        """)
        self.connection.commit()

    def insertar_planta(self, nombre, familia, clima):
        self.cursor.execute("INSERT INTO Plantas (nombre, familia, clima) VALUES (%s, %s, %s)", (nombre, familia, clima))
        self.connection.commit()

# Uso de DatabaseManager
db_manager = DatabaseManager("localhost", "root", "usuario", "1dam")
db_manager.crear_tabla()
db_manager.insertar_planta("Cactus", "Cactaceae", "Árido")

#DatabaseManagerORM → Uso de Peewee ORM para bases de datos relacionales.
from peewee import *

db = MySQLDatabase("1dam", user="root", password="usuario", host="localhost", port=3306)

class BaseModel(Model):
    class Meta:
        database = db

class Planta(BaseModel):
    nombre = CharField()
    familia = CharField()
    clima = CharField()

db.connect()
db.create_tables([Planta])

# Insertar una planta con ORM
Planta.create(nombre="Orquídea", familia="Orchidaceae", clima="Tropical")


#DatabaseManagerDocumental → Para bases de datos MongoDB.

from pymongo import MongoClient

client = MongoClient("mongodb://localhost:27017")
db = client["plantas_db"]
coleccion = db["plantas"]

# Insertar un documento
coleccion.insert_one({"nombre": "Bambú", "familia": "Poaceae", "clima": "Templado"})

# Consultar documentos
for planta in coleccion.find():
    print(planta)

#DatabaseManagerObject → Para bases de datos ZODB (orientadas a objetos).

import transaction
from ZODB import DB, FileStorage
from persistent import Persistent

class Planta(Persistent):
    def __init__(self, nombre, familia, clima):
        self.nombre = nombre
        self.familia = familia
        self.clima = clima

storage = FileStorage.FileStorage("plantas.fs")
db = DB(storage)
connection = db.open()
root = connection.root()

if "plantas" not in root:
    root["plantas"] = {}

# Insertar un objeto persistente
transaction.begin()
root["plantas"]["1"] = Planta("Pino", "Pinaceae", "Frío")
transaction.commit()

# Leer objetos almacenados
for key, planta in root["plantas"].items():
    print(f"{key}: {planta.nombre}, {planta.familia}, {planta.clima}")


